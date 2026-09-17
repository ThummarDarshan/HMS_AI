from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class MedicationDocumentChunk:
    medication_name: str
    generic_name: str
    brand_names: List[str] = field(default_factory=list)
    active_ingredients: List[str] = field(default_factory=list)
    section: str = "GENERAL_SUMMARY"  # INDICATIONS, WARNINGS, CONTRAINDICATIONS, ADVERSE_REACTIONS, etc.
    section_title: str = "General Information"
    content: str = ""
    source: str = "CDSCO"  # CDSCO, DAILYMED, OPENFDA, MANUFACTURER
    source_url: str = ""
    document_id: Optional[str] = None
    document_version: Optional[str] = None
    last_updated: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class MedicationSourceProvider(ABC):
    """
    Abstract interface for medication knowledge sources (CDSCO, DailyMed, OpenFDA).
    Ensures decoupled and extensible provider architecture.
    """

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Name of the source e.g. 'CDSCO', 'DAILYMED', 'OPENFDA'"""
        pass

    @abstractmethod
    def search_medication(self, query: str) -> List[Dict[str, Any]]:
        """Search available official documents by drug name or symptom"""
        pass

    @abstractmethod
    def get_medication_details(self, drug_identifier: str) -> List[MedicationDocumentChunk]:
        """Fetch and parse official monograph/label into structured section chunks"""
        pass
