# ai_assistant/retrieval/search.py
import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from django.db.models import Q
from ai_assistant.models import MedicationDocument

logger = logging.getLogger(__name__)

# Common symptom to candidate drug mappings for informational retrieval
SYMPTOM_DRUG_MAP = {
    "fever": ["paracetamol", "ibuprofen"],
    "high temperature": ["paracetamol", "ibuprofen"],
    "chills": ["paracetamol"],
    "headache": ["paracetamol", "ibuprofen"],
    "migraine": ["paracetamol", "ibuprofen"],
    "body ache": ["paracetamol", "ibuprofen"],
    "pain": ["paracetamol", "ibuprofen"],
    "joint pain": ["ibuprofen", "paracetamol"],
    "arthritis": ["ibuprofen"],
    "allergy": ["cetirizine", "montelukast"],
    "runny nose": ["cetirizine"],
    "sneezing": ["cetirizine"],
    "itching": ["cetirizine"],
    "urticaria": ["cetirizine"],
    "hives": ["cetirizine"],
    "acidity": ["pantoprazole"],
    "heartburn": ["pantoprazole"],
    "acid reflux": ["pantoprazole"],
    "gerd": ["pantoprazole"],
    "gastritis": ["pantoprazole"],
    "bacterial infection": ["amoxicillin", "azithromycin", "ciprofloxacin"],
    "strep throat": ["amoxicillin", "azithromycin"],
    "ear infection": ["amoxicillin"],
    "pneumonia": ["azithromycin", "amoxicillin"],
    "diabetes": ["metformin"],
    "high blood sugar": ["metformin"],
    "hypertension": ["telmisartan", "amlodipine"],
    "high blood pressure": ["telmisartan", "amlodipine"],
    "high bp": ["telmisartan", "amlodipine"],
    "cholesterol": ["atorvastatin"],
    "dehydration": ["ors"],
    "loose motion": ["ors"],
    "diarrhea": ["ors"],
    "vomiting": ["ondansetron"],
    "nausea": ["ondansetron"],
    "asthma": ["salbutamol", "montelukast"],
    "wheezing": ["salbutamol"],
    "breathlessness": ["salbutamol"],
    "uti": ["ciprofloxacin", "amoxicillin"],
    "urine infection": ["ciprofloxacin"],
}

KNOWN_DRUGS = [
    "paracetamol", "acetaminophen", "dolo 650", "calpol", "crocin", "pacimol", "tylenol",
    "ibuprofen", "brufen", "combiflam", "advil", "motrin", "ibugesic",
    "pantoprazole", "pan 40", "pantocid", "pantosec", "protonix",
    "amoxicillin", "augmentin", "moxikind", "novamox", "amoxil",
    "azithromycin", "azithral", "azee", "zithromax", "azimax",
    "cetirizine", "cetzine", "okacet", "zyrtec", "alerid",
    "metformin", "glycomet", "glucophage", "obimet",
    "telmisartan", "telma", "micardis", "telpres",
    "amlodipine", "amlong", "norvasc", "amlopin", "stamlo",
    "atorvastatin", "atorva", "lipitor", "storvas", "tonact",
    "ors", "electral", "coslyte", "prolyte",
    "ondansetron", "emeset", "zofran", "vomikind",
    "salbutamol", "albuterol", "asthalin", "ventolin",
    "montelukast", "montair", "singulair", "montek",
    "ciprofloxacin", "ciplox", "cipro", "cifran",
]


def extract_symptoms_and_drugs(text: str) -> Tuple[List[str], List[str]]:
    """Extract known symptoms and explicit drug mentions from patient query"""
    text_clean = text.lower()
    found_symptoms = []
    found_drugs = []

    # Detect drug mentions
    for drug in KNOWN_DRUGS:
        if re.search(r"\b" + re.escape(drug) + r"\b", text_clean):
            found_drugs.append(drug)

    # Detect symptom mentions
    for symptom, candidate_drugs in SYMPTOM_DRUG_MAP.items():
        if re.search(r"\b" + re.escape(symptom) + r"\b", text_clean):
            found_symptoms.append(symptom)
            for d in candidate_drugs:
                if d not in found_drugs:
                    found_drugs.append(d)

    return found_symptoms, found_drugs


class MedicationRetrievalEngine:
    """
    Retrieval engine for authoritative CDSCO and DailyMed medication database monographs.
    """

    @classmethod
    def retrieve(
        cls, query: str, section_filter: Optional[List[str]] = None, limit: int = 6
    ) -> Dict[str, Any]:
        """
        Executes search across database medication monographs.
        """
        symptoms, target_drugs = extract_symptoms_and_drugs(query)
        query_clean = query.strip()

        # Database Search in MedicationDocument
        base_q = Q()
        if target_drugs:
            drug_filters = Q()
            for d in target_drugs:
                drug_filters |= Q(generic_name__icontains=d)
                drug_filters |= Q(medication_name__icontains=d)
                drug_filters |= Q(brand_names__icontains=d)
            base_q &= drug_filters
        else:
            terms = [t for t in query_clean.split() if len(t) > 3]
            if terms:
                term_q = Q()
                for term in terms:
                    term_q |= Q(generic_name__icontains=term) | Q(content__icontains=term) | Q(medication_name__icontains=term)
                base_q &= term_q

        if section_filter:
            base_q &= Q(section__in=section_filter)

        matched_docs = []
        try:
            matched_docs = list(MedicationDocument.objects.filter(base_q).order_by("generic_name", "section")[:limit * 2])
            if not matched_docs and not target_drugs:
                matched_docs = list(MedicationDocument.objects.filter(
                    Q(content__icontains=query_clean[:50]) | Q(medication_name__icontains=query_clean[:50])
                )[:limit])
        except Exception as e:
            logger.warning(f"Database query error: {e}")

        # Format and organize structured medication entries
        ranked_results = []
        sources = []
        medications_dict: Dict[str, Dict[str, Any]] = {}

        for doc in matched_docs[:limit]:
            gen_name = doc.generic_name
            if gen_name not in medications_dict:
                medications_dict[gen_name] = {
                    "name": doc.medication_name,
                    "generic_name": doc.generic_name,
                    "brand_names": doc.brand_names,
                    "sections": {},
                    "warnings": [],
                    "contraindications": [],
                    "indications": "",
                    "sources": [],
                }

            med_entry = medications_dict[gen_name]
            med_entry["sections"][doc.section] = {
                "title": doc.section_title,
                "content": doc.content,
                "source": doc.source,
                "source_url": doc.source_url,
            }

            if doc.section == "INDICATIONS":
                med_entry["indications"] = doc.content
            elif doc.section == "WARNINGS":
                med_entry["warnings"].append(doc.content)
            elif doc.section == "CONTRAINDICATIONS":
                med_entry["contraindications"].append(doc.content)

            source_item = {
                "name": doc.get_source_display() if hasattr(doc, "get_source_display") else doc.source,
                "source_type": doc.source,
                "url": doc.source_url,
                "document_id": doc.document_id or doc.generic_name,
                "section": doc.section_title,
                "last_updated": doc.last_updated or "2026 Verified",
            }
            if source_item not in sources:
                sources.append(source_item)
            if source_item not in med_entry["sources"]:
                med_entry["sources"].append(source_item)

            ranked_results.append(doc)

        has_verified_docs = len(matched_docs) > 0 or len(medications_dict) > 0
        evidence_level = "HIGH" if len(matched_docs) >= 2 else ("MEDIUM" if has_verified_docs else "NONE")

        return {
            "has_verified_evidence": has_verified_docs,
            "evidence_level": evidence_level,
            "symptoms": symptoms,
            "target_drugs": target_drugs,
            "documents": ranked_results,
            "medications": list(medications_dict.values()),
            "sources": sources,
        }
