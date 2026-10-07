"""
Universal Clinical Conversation Engine Package
Provides clinical condition configuration, entity extraction,
dynamic one-question-at-a-time conversation control, and evidence-based clinical guidance.
"""

from .condition_registry import (
    CONDITION_REGISTRY,
    get_condition_by_id,
    find_condition_by_text,
    find_all_conditions_by_text,
    register_condition,
)
from .entity_extractor import ClinicalEntityExtractor
from .response_formatter import ClinicalResponseFormatter
from .conversation_engine import UniversalClinicalEngine

__all__ = [
    "CONDITION_REGISTRY",
    "get_condition_by_id",
    "find_condition_by_text",
    "find_all_conditions_by_text",
    "register_condition",
    "ClinicalEntityExtractor",
    "ClinicalResponseFormatter",
    "UniversalClinicalEngine",
]
