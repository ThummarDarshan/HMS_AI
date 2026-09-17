import logging
import requests
from typing import Dict, List, Any, Optional
from ai_assistant.providers.base import MedicationSourceProvider, MedicationDocumentChunk

logger = logging.getLogger(__name__)


class OpenFDAProvider(MedicationSourceProvider):
    """
    OpenFDA Drug Label API Medication Source Provider.
    Queries official FDA structured drug label endpoints.
    """

    @property
    def source_name(self) -> str:
        return "OPENFDA"

    def __init__(self, base_url: str = "https://api.fda.gov/drug/label.json"):
        self.base_url = base_url
        self.session = requests.Session()

    def search_medication(self, query: str) -> List[Dict[str, Any]]:
        """Search openFDA by generic name or brand name"""
        q = query.strip()
        search_query = f'openfda.generic_name:"{q}"+openfda.brand_name:"{q}"'
        params = {"search": search_query, "limit": 3}
        try:
            resp = self.session.get(self.base_url, params=params, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                results = []
                for item in data.get("results", []):
                    openfda_data = item.get("openfda", {})
                    generic_names = openfda_data.get("generic_name", [q])
                    brand_names = openfda_data.get("brand_name", [])
                    results.append({
                        "id": item.get("id"),
                        "generic_name": generic_names[0] if generic_names else q,
                        "brand_names": brand_names,
                        "source": "OPENFDA",
                        "source_url": "https://open.fda.gov/apis/drug/label/",
                    })
                return results
        except Exception as e:
            logger.warning(f"openFDA search error: {e}")
        return []

    def get_medication_details(self, drug_identifier: str) -> List[MedicationDocumentChunk]:
        """Fetch label details from openFDA"""
        q = drug_identifier.strip()
        search_query = f'openfda.generic_name:"{q}"+openfda.brand_name:"{q}"'
        params = {"search": search_query, "limit": 1}
        try:
            resp = self.session.get(self.base_url, params=params, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])
                if not results:
                    return []
                label = results[0]
                openfda_data = label.get("openfda", {})
                generic_name = openfda_data.get("generic_name", [q])[0]
                brand_names = openfda_data.get("brand_name", [])

                section_mapping = [
                    ("INDICATIONS", "Indications and Usage", label.get("indications_and_usage")),
                    ("WARNINGS", "Warnings and Precautions", label.get("warnings_and_cautions") or label.get("warnings")),
                    ("CONTRAINDICATIONS", "Contraindications", label.get("contraindications")),
                    ("ADVERSE_REACTIONS", "Adverse Reactions", label.get("adverse_reactions")),
                    ("DRUG_INTERACTIONS", "Drug Interactions", label.get("drug_interactions")),
                    ("DOSAGE_AND_ADMINISTRATION", "Dosage and Administration", label.get("dosage_and_administration")),
                ]

                chunks = []
                for sec_key, sec_title, sec_content in section_mapping:
                    if sec_content:
                        text = " ".join(sec_content) if isinstance(sec_content, list) else str(sec_content)
                        chunks.append(
                            MedicationDocumentChunk(
                                medication_name=generic_name.title(),
                                generic_name=generic_name.title(),
                                brand_names=brand_names,
                                active_ingredients=[generic_name.title()],
                                section=sec_key,
                                section_title=sec_title,
                                content=text[:2000].strip(),
                                source="OPENFDA",
                                source_url="https://open.fda.gov/apis/drug/label/",
                                document_id=label.get("id"),
                                document_version=label.get("version", "1"),
                                last_updated=label.get("effective_time", "2024-01-01"),
                            )
                        )
                return chunks
        except Exception as e:
            logger.warning(f"openFDA fetch error: {e}")
        return []
