import re
from typing import List
from ai_assistant.providers.base import MedicationDocumentChunk


def clean_medical_text(text: str) -> str:
    """Normalize whitespace and sanitize characters in medical document text"""
    if not text:
        return ""
    # Remove HTML tags if present
    text = re.sub(r"<[^>]+>", " ", text)
    # Normalize multiple whitespace and newlines
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def section_aware_chunk(chunk: MedicationDocumentChunk, max_chunk_chars: int = 1500) -> List[MedicationDocumentChunk]:
    """
    Section-aware chunking: splits long medical sections at sentence boundaries
    while strictly retaining document, source, and section metadata.
    """
    clean_content = clean_medical_text(chunk.content)
    if len(clean_content) <= max_chunk_chars:
        chunk.content = clean_content
        return [chunk]

    # Split into sentence boundaries
    sentences = re.split(r"(?<=[.!?])\s+", clean_content)
    chunks: List[MedicationDocumentChunk] = []
    current_sentences: List[str] = []
    current_length = 0
    sub_index = 1

    for sentence in sentences:
        if current_length + len(sentence) > max_chunk_chars and current_sentences:
            chunk_text = " ".join(current_sentences)
            new_chunk = MedicationDocumentChunk(
                medication_name=chunk.medication_name,
                generic_name=chunk.generic_name,
                brand_names=chunk.brand_names,
                active_ingredients=chunk.active_ingredients,
                section=chunk.section,
                section_title=f"{chunk.section_title} (Part {sub_index})",
                content=chunk_text,
                source=chunk.source,
                source_url=chunk.source_url,
                document_id=chunk.document_id,
                document_version=chunk.document_version,
                last_updated=chunk.last_updated,
                metadata=chunk.metadata,
            )
            chunks.append(new_chunk)
            sub_index += 1
            current_sentences = [sentence]
            current_length = len(sentence)
        else:
            current_sentences.append(sentence)
            current_length += len(sentence)

    if current_sentences:
        chunk_text = " ".join(current_sentences)
        new_chunk = MedicationDocumentChunk(
            medication_name=chunk.medication_name,
            generic_name=chunk.generic_name,
            brand_names=chunk.brand_names,
            active_ingredients=chunk.active_ingredients,
            section=chunk.section,
            section_title=f"{chunk.section_title} (Part {sub_index})" if sub_index > 1 else chunk.section_title,
            content=chunk_text,
            source=chunk.source,
            source_url=chunk.source_url,
            document_id=chunk.document_id,
            document_version=chunk.document_version,
            last_updated=chunk.last_updated,
            metadata=chunk.metadata,
        )
        chunks.append(new_chunk)

    return chunks
