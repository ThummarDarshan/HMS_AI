import logging
import hashlib
from typing import List, Dict, Any, Optional
from ai_assistant.models import MedicationDocument
from ai_assistant.providers.base import MedicationSourceProvider, MedicationDocumentChunk
from ai_assistant.providers.cdsco_provider import CDSCOProvider, OFFICIAL_CDSCO_MONOGRAPHS
from ai_assistant.providers.dailymed_provider import DailyMedProvider, DAILYMED_VERIFIED_MONOGRAPHS
from ai_assistant.providers.openfda_provider import OpenFDAProvider
from ai_assistant.ingestion.chunker import section_aware_chunk

logger = logging.getLogger(__name__)


def generate_pseudo_embedding(text: str, dim: int = 128) -> List[float]:
    """
    Fast, deterministic semantic vector generation for portable vector similarity
    when external embedding API is offline or not configured.
    """
    import math
    text_clean = text.lower().strip()
    words = text_clean.split()
    vector = [0.0] * dim

    for i, word in enumerate(words):
        h = int(hashlib.md5(word.encode("utf-8")).hexdigest(), 16)
        idx = h % dim
        weight = 1.0 / math.sqrt(i + 1)
        vector[idx] += weight

    # Normalize vector to unit length
    norm = math.sqrt(sum(v * v for v in vector)) or 1.0
    return [round(v / norm, 5) for v in vector]


class MedicationIngestionPipeline:
    """
    Ingestion pipeline that coordinates fetching, parsing, chunking,
    and storing authoritative medication documents from CDSCO, DailyMed, and OpenFDA.
    """

    def __init__(self, providers: Optional[List[MedicationSourceProvider]] = None):
        self.providers = providers or [CDSCOProvider(), DailyMedProvider(), OpenFDAProvider()]

    def ingest_drug(self, drug_name: str) -> int:
        """Ingest a specific drug from all configured providers"""
        total_ingested = 0
        for provider in self.providers:
            try:
                chunks = provider.get_medication_details(drug_name)
                for raw_chunk in chunks:
                    sub_chunks = section_aware_chunk(raw_chunk)
                    for chunk in sub_chunks:
                        self._store_chunk(chunk)
                        total_ingested += 1
            except Exception as e:
                logger.error(f"Error ingesting '{drug_name}' from {provider.source_name}: {e}")
        return total_ingested

    def seed_all_verified_monographs(self) -> Dict[str, int]:
        """Ingest all baseline verified CDSCO and DailyMed monographs"""
        stats = {"CDSCO": 0, "DAILYMED": 0}

        # 1. CDSCO
        cdsco = CDSCOProvider()
        for drug_key in OFFICIAL_CDSCO_MONOGRAPHS.keys():
            chunks = cdsco.get_medication_details(drug_key)
            for raw_chunk in chunks:
                for chunk in section_aware_chunk(raw_chunk):
                    self._store_chunk(chunk)
                    stats["CDSCO"] += 1

        # 2. DailyMed
        dailymed = DailyMedProvider()
        for drug_key in DAILYMED_VERIFIED_MONOGRAPHS.keys():
            chunks = dailymed.get_medication_details(drug_key)
            for raw_chunk in chunks:
                for chunk in section_aware_chunk(raw_chunk):
                    self._store_chunk(chunk)
                    stats["DAILYMED"] += 1

        return stats

    def _store_chunk(self, chunk: MedicationDocumentChunk) -> MedicationDocument:
        """Upsert medication chunk into the database"""
        embedding = generate_pseudo_embedding(f"{chunk.medication_name} {chunk.section_title} {chunk.content}")

        doc, created = MedicationDocument.objects.update_or_create(
            generic_name__iexact=chunk.generic_name,
            source=chunk.source,
            section=chunk.section,
            section_title=chunk.section_title,
            defaults={
                "medication_name": chunk.medication_name,
                "generic_name": chunk.generic_name,
                "brand_names": chunk.brand_names,
                "active_ingredients": chunk.active_ingredients,
                "content": chunk.content,
                "source": chunk.source,
                "source_url": chunk.source_url,
                "document_id": chunk.document_id,
                "document_version": chunk.document_version,
                "last_updated": chunk.last_updated,
                "embedding": embedding,
            },
        )
        return doc
