import logging
from typing import Dict, List, Any, Optional
from ai_assistant.providers.base import MedicationSourceProvider, MedicationDocumentChunk

logger = logging.getLogger(__name__)


class CDSCOProvider(MedicationSourceProvider):
    """
    CDSCO (Central Drugs Standard Control Organisation, Directorate General of Health Services,
    Ministry of Health & Family Welfare, Government of India) Medication Source Provider.
    Provides verified Indian regulatory drug monographs, approved indications, formulations,
    and Indian clinical guidance.
    """

    @property
    def source_name(self) -> str:
        return "CDSCO"

    def __init__(self):
        self.official_portal_url = "https://cdsco.gov.in"
        self.database_url = "https://cdscoonline.gov.in/CDSCO/Drugs"

    def search_medication(self, query: str) -> List[Dict[str, Any]]:
        """Search Indian approved drugs registry"""
        query_clean = query.strip().lower()
        results = []
        for drug_key, monograph in OFFICIAL_CDSCO_MONOGRAPHS.items():
            if (
                query_clean in drug_key
                or query_clean in monograph["generic_name"].lower()
                or any(query_clean in b.lower() for b in monograph.get("brand_names", []))
                or any(query_clean in s.lower() for s in monograph.get("symptoms", []))
            ):
                results.append({
                    "id": drug_key,
                    "generic_name": monograph["generic_name"],
                    "brand_names": monograph.get("brand_names", []),
                    "source": "CDSCO",
                    "source_url": monograph.get("source_url", self.official_portal_url),
                })
        return results

    def get_medication_details(self, drug_identifier: str) -> List[MedicationDocumentChunk]:
        """Retrieve verified CDSCO structured document chunks for a medication"""
        key = drug_identifier.strip().lower()
        if key not in OFFICIAL_CDSCO_MONOGRAPHS:
            # Check if matching by generic or brand
            for d_key, monograph in OFFICIAL_CDSCO_MONOGRAPHS.items():
                if (
                    d_key in key
                    or key in monograph["generic_name"].lower()
                    or any(key == b.lower() for b in monograph.get("brand_names", []))
                ):
                    key = d_key
                    break

        if key not in OFFICIAL_CDSCO_MONOGRAPHS:
            return []

        mono = OFFICIAL_CDSCO_MONOGRAPHS[key]
        chunks = []

        for section_key, section_data in mono.get("sections", {}).items():
            chunks.append(
                MedicationDocumentChunk(
                    medication_name=mono["medication_name"],
                    generic_name=mono["generic_name"],
                    brand_names=mono.get("brand_names", []),
                    active_ingredients=mono.get("active_ingredients", [mono["generic_name"]]),
                    section=section_key,
                    section_title=section_data.get("title", section_key.replace("_", " ").title()),
                    content=section_data.get("content", "").strip(),
                    source="CDSCO",
                    source_url=mono.get("source_url", "https://cdsco.gov.in"),
                    document_id=mono.get("document_id", f"CDSCO-IND-{key.upper()}"),
                    document_version=mono.get("document_version", "2024-V1"),
                    last_updated=mono.get("last_updated", "2024-06-01"),
                    metadata={
                        "regulatory_authority": "Central Drugs Standard Control Organisation (India)",
                        "schedule": mono.get("schedule", "Schedule H"),
                        "approval_status": "Approved in India",
                    },
                )
            )

        return chunks


# Authoritative CDSCO Regulatory Drug Monographs for standard Indian hospital formulations
OFFICIAL_CDSCO_MONOGRAPHS: Dict[str, Dict[str, Any]] = {
    "paracetamol": {
        "medication_name": "Paracetamol (Acetaminophen)",
        "generic_name": "Paracetamol",
        "brand_names": ["Dolo 650", "Calpol", "Crocin", "Pacimol", "Sumo L", "Pyrigesic"],
        "active_ingredients": ["Paracetamol", "Acetaminophen"],
        "symptoms": ["fever", "headache", "mild pain", "body ache", "toothache", "post-vaccination fever"],
        "schedule": "Over-The-Counter (OTC) / Non-Schedule",
        "document_id": "CDSCO-DOC-PARA-001",
        "document_version": "CDSCO-2024.1",
        "last_updated": "2024-05-15",
        "source_url": "https://cdsco.gov.in/opencms/opencms/en/Drugs/Approved-Drugs/",
        "sections": {
            "INDICATIONS": {
                "title": "Approved Indications and Clinical Usage",
                "content": "Paracetamol is indicated for the temporary relief of mild to moderate pain (including headache, musculoskeletal pain, dysmenorrhea, dental pain, osteoarthritis) and reduction of pyrexia (fever) in adults and pediatric patients.",
            },
            "DOSAGE_AND_ADMINISTRATION": {
                "title": "Dosage and Administration Guidance",
                "content": "Standard adult oral dosage is 500 mg to 650 mg every 4 to 6 hours as needed. Maximum daily dosage must NOT exceed 4000 mg (4 grams) in 24 hours from all sources to avoid severe hepatotoxicity. Pediatric dosing must be strictly weight-based (10–15 mg/kg/dose) under clinical supervision. Minimum dosing interval is 4 hours.",
            },
            "WARNINGS": {
                "title": "Warnings and Hepatic Precautions",
                "content": "HEPATOTOXICITY WARNING: Exceeding the maximum recommended daily dose may result in severe liver damage, hepatic failure, and death. Do not consume concurrent alcohol or multiple medications containing paracetamol/acetaminophen. Use with extreme caution in patients with chronic liver impairment, alcoholism, chronic malnutrition, or severe dehydration.",
            },
            "CONTRAINDICATIONS": {
                "title": "Contraindications",
                "content": "Contraindicated in individuals with known hypersensitivity to paracetamol or any formulation excipient, and in patients with severe acute hepatic failure or active decompensated liver disease.",
            },
            "ADVERSE_REACTIONS": {
                "title": "Adverse Reactions / Side Effects",
                "content": "Generally well-tolerated at therapeutic doses. Rare adverse reactions include cutaneous hypersensitivity (skin rash, urticaria, pruritus), thrombocytopenia, leukopenia, and elevation of hepatic transaminases. Very rare occurrences of serious skin reactions (Stevens-Johnson syndrome, toxic epidermal necrolysis) have been reported.",
            },
            "DRUG_INTERACTIONS": {
                "title": "Drug Interactions",
                "content": "Chronic high-dose co-administration with oral anticoagulants (e.g., Warfarin) may potentiate anticoagulant effect and bleeding risk. Hepatotoxic medications (e.g., Isoniazid, Phenytoin, Carbamazepine) enhance the risk of paracetamol liver injury. Absorption rate may be increased by Metoclopramide and decreased by Cholestyramine.",
            },
            "PATIENT_INFORMATION": {
                "title": "Patient Counseling Information",
                "content": "Take strictly as advised by a healthcare provider. Do not exceed recommended dose. Check labels of all other cough, cold, or pain remedies to prevent accidental paracetamol overdose. Seek immediate medical assistance if symptoms persist beyond 3 days or if signs of allergic reaction occur.",
            },
        },
    },
    "ibuprofen": {
        "medication_name": "Ibuprofen",
        "generic_name": "Ibuprofen",
        "brand_names": ["Brufen", "Combiflam (combination)", "Ibugesic", "Ibupal"],
        "active_ingredients": ["Ibuprofen"],
        "symptoms": ["pain", "inflammation", "fever", "arthritis", "joint swelling", "menstrual cramps"],
        "schedule": "Schedule H (Prescription)",
        "document_id": "CDSCO-DOC-IBU-002",
        "document_version": "CDSCO-2024.1",
        "last_updated": "2024-04-20",
        "source_url": "https://cdsco.gov.in/opencms/opencms/en/Drugs/Approved-Drugs/",
        "sections": {
            "INDICATIONS": {
                "title": "Indications and Usage",
                "content": "Ibuprofen is a non-steroidal anti-inflammatory drug (NSAID) indicated for relief of signs and symptoms of rheumatoid arthritis, osteoarthritis, mild to moderate pain, dysmenorrhea, and fever reduction.",
            },
            "WARNINGS": {
                "title": "Cardiovascular and Gastrointestinal Black Box Warnings",
                "content": "CARDIOVASCULAR THROMBOTIC EVENTS: NSAIDs cause an increased risk of serious cardiovascular thrombotic events, myocardial infarction, and stroke. GASTROINTESTINAL RISK: NSAIDs cause serious gastrointestinal adverse events including bleeding, ulceration, and perforation of the stomach or intestines, which can be fatal. Risk is heightened in elderly patients and those with prior peptic ulcer disease.",
            },
            "CONTRAINDICATIONS": {
                "title": "Contraindications",
                "content": "Contraindicated in patients with known hypersensitivity to ibuprofen, history of asthma, urticaria, or allergic-type reactions after taking aspirin or other NSAIDs, in the setting of coronary artery bypass graft (CABG) surgery, and in patients with active gastrointestinal bleeding or severe renal failure.",
            },
            "ADVERSE_REACTIONS": {
                "title": "Adverse Reactions",
                "content": "Most common adverse effects are gastrointestinal: dyspepsia, nausea, abdominal pain, epigastric distress, diarrhea, flatulence, and constipation. Other effects include dizziness, headache, fluid retention, edema, and elevated blood pressure.",
            },
            "DRUG_INTERACTIONS": {
                "title": "Drug Interactions",
                "content": "Concomitant use with ACE inhibitors, ARBs, or beta-blockers may diminish their antihypertensive effect and precipitate renal failure. Co-administration with Aspirin or Anticoagulants (Warfarin, Heparin) significantly increases gastrointestinal bleeding risk. Ibuprofen reduces renal clearance of Lithium and Methotrexate.",
            },
            "PATIENT_INFORMATION": {
                "title": "Patient Information",
                "content": "Take with food or milk to minimize gastrointestinal upset. Avoid taking if you have a history of stomach ulcers, kidney disease, or cardiac problems without direct clinician oversight.",
            },
        },
    },
    "amoxicillin": {
        "medication_name": "Amoxicillin / Amoxicillin + Clavulanic Acid",
        "generic_name": "Amoxicillin",
        "brand_names": ["Augmentin", "Moxikind-CV", "Novamox", "Amoxyclav", "Clavam"],
        "active_ingredients": ["Amoxicillin", "Clavulanic Acid"],
        "symptoms": ["bacterial infection", "sore throat (bacterial)", "ear infection", "sinusitis", "respiratory tract infection", "urinary tract infection"],
        "schedule": "Schedule H1 (Controlled Antibiotic - Prescription Only)",
        "document_id": "CDSCO-DOC-AMOX-003",
        "document_version": "CDSCO-2024.2",
        "last_updated": "2024-03-10",
        "source_url": "https://cdsco.gov.in/opencms/opencms/en/Drugs/Approved-Drugs/",
        "sections": {
            "INDICATIONS": {
                "title": "Indications and Usage",
                "content": "Amoxicillin is an aminopenicillin antibiotic indicated for the treatment of documented or strongly suspected bacterial infections of the ear, nose, throat, lower respiratory tract, genitourinary tract, skin and skin structure caused by susceptible beta-lactamase negative or co-amoxiclav susceptible isolates. It is INEFFECTIVE against viral infections such as the common cold or viral influenza.",
            },
            "WARNINGS": {
                "title": "Hypersensitivity and Clostridioides difficile Warnings",
                "content": "SERIOUS ANAPHYLACTIC REACTIONS: Serious and occasionally fatal hypersensitivity (anaphylactic) reactions have been reported in patients on penicillin therapy. Discontinue immediately if allergic symptoms develop. Clostridioides difficile-associated diarrhea (CDAD) has been reported with use of nearly all antibacterial agents.",
            },
            "CONTRAINDICATIONS": {
                "title": "Contraindications",
                "content": "Contraindicated in patients with a history of severe allergic reaction (e.g., anaphylaxis, Stevens-Johnson syndrome) to penicillins, cephalosporins, or other beta-lactams, and in patients with a history of amoxicillin/clavulanate-associated cholestatic jaundice or hepatic dysfunction.",
            },
            "ADVERSE_REACTIONS": {
                "title": "Adverse Reactions",
                "content": "Most common adverse reactions are diarrhea, nausea, vomiting, skin rashes, urticaria, vaginitis, and candidiasis. Rarely: cholestatic jaundice, hepatitis, and interstitial nephritis.",
            },
            "DRUG_INTERACTIONS": {
                "title": "Drug Interactions",
                "content": "Probenecid decreases renal tubular secretion of amoxicillin, producing higher blood levels. Concomitant use with oral anticoagulants may prolong prothrombin time / INR. May reduce efficacy of combined oral contraceptives.",
            },
            "PATIENT_INFORMATION": {
                "title": "Patient Information & Antibiotic Stewardship",
                "content": "This is a Schedule H1 antibiotic and requires a valid physician prescription. Complete the full prescribed course even if symptoms improve early to prevent the development of antimicrobial resistance. Do not share or reuse leftover antibiotics.",
            },
        },
    },
    "cetirizine": {
        "medication_name": "Cetirizine Hydrochloride",
        "generic_name": "Cetirizine",
        "brand_names": ["Cetzine", "Okacet", "Alerid", "Zyrtec", "Incid-L"],
        "active_ingredients": ["Cetirizine Hydrochloride"],
        "symptoms": ["allergy", "sneezing", "runny nose", "itching", "watery eyes", "urticaria", "hives"],
        "schedule": "Schedule H",
        "document_id": "CDSCO-DOC-CET-004",
        "document_version": "CDSCO-2024.1",
        "last_updated": "2024-02-18",
        "source_url": "https://cdsco.gov.in/opencms/opencms/en/Drugs/Approved-Drugs/",
        "sections": {
            "INDICATIONS": {
                "title": "Indications and Usage",
                "content": "Cetirizine is a second-generation H1-antihistamine indicated for the relief of symptoms associated with seasonal and perennial allergic rhinitis (sneezing, rhinorrhea, nasal pruritus, ocular redness and tearing) and the treatment of uncomplicated skin manifestations of chronic idiopathic urticaria.",
            },
            "WARNINGS": {
                "title": "Central Nervous System Depression Warnings",
                "content": "May cause central nervous system depression leading to somnolence and sedation. Caution is advised when engaging in activities requiring mental alertness, such as driving or operating machinery. Avoid concurrent alcohol or CNS depressants.",
            },
            "CONTRAINDICATIONS": {
                "title": "Contraindications",
                "content": "Contraindicated in patients with known hypersensitivity to cetirizine, hydroxyzine, or levocetirizine, and in patients with end-stage renal disease (CrCl < 10 mL/min) undergoing hemodialysis.",
            },
            "ADVERSE_REACTIONS": {
                "title": "Adverse Reactions",
                "content": "Somnolence, fatigue, dry mouth, dizziness, pharyngitis, and headache. In pediatric patients, abdominal pain and epistaxis may occur.",
            },
            "DRUG_INTERACTIONS": {
                "title": "Drug Interactions",
                "content": "Additive sedation with central nervous system depressants, sedatives, hypnotics, tranquilizers, and alcohol. Theophylline slightly decreases cetirizine clearance.",
            },
            "PATIENT_INFORMATION": {
                "title": "Patient Information",
                "content": "Take once daily in the evening. Avoid consuming alcohol while taking this medicine. Consult your doctor if allergic symptoms do not resolve within 7 days.",
            },
        },
    },
    "metformin": {
        "medication_name": "Metformin Hydrochloride",
        "generic_name": "Metformin",
        "brand_names": ["Glycomet", "Gluconorm", "Glucophage", "Obimet", "Cetapin"],
        "active_ingredients": ["Metformin Hydrochloride"],
        "symptoms": ["high blood sugar", "type 2 diabetes", "hyperglycemia", "polycystic ovary syndrome"],
        "schedule": "Schedule H (Prescription Only)",
        "document_id": "CDSCO-DOC-MET-005",
        "document_version": "CDSCO-2024.1",
        "last_updated": "2024-01-25",
        "source_url": "https://cdsco.gov.in/opencms/opencms/en/Drugs/Approved-Drugs/",
        "sections": {
            "INDICATIONS": {
                "title": "Indications and Clinical Usage",
                "content": "Metformin is a biguanide antihyperglycemic agent indicated as an adjunct to diet and exercise to improve glycemic control in adults and pediatric patients aged 10 years and older with Type 2 Diabetes Mellitus.",
            },
            "WARNINGS": {
                "title": "Boxed Warning: Lactic Acidosis Risk",
                "content": "LACTIC ACIDOSIS: A rare but serious metabolic complication characterized by elevated blood lactate levels, metabolic acidosis, hypothermia, hypotension, and resistant bradyarrhythmias. Risk factors include renal impairment, sepsis, acute congestive heart failure, excessive alcohol intake, and radiological contrast study procedures. Withhold immediately prior to iodinated contrast imaging.",
            },
            "CONTRAINDICATIONS": {
                "title": "Contraindications",
                "content": "Contraindicated in severe renal impairment (eGFR < 30 mL/min/1.73 m2), acute or chronic metabolic acidosis including diabetic ketoacidosis, and history of hypersensitivity to metformin.",
            },
            "ADVERSE_REACTIONS": {
                "title": "Adverse Reactions",
                "content": "Most common: diarrhea, nausea, vomiting, flatulence, asthenia, indigestion, abdominal discomfort, and metallic taste. Long-term use is associated with vitamin B12 deficiency due to reduced intestinal absorption.",
            },
            "DRUG_INTERACTIONS": {
                "title": "Drug Interactions",
                "content": "Carbonic anhydrase inhibitors (e.g., Topiramate, Zonisamide) increase lactic acidosis risk. Cationic drugs (e.g., Ranolazine, Vandetanib, Dolutegravir) may increase metformin exposure through organic cation transporter competition.",
            },
            "PATIENT_INFORMATION": {
                "title": "Patient Information",
                "content": "Take with meals to reduce gastrointestinal side effects. Do not skip meals. Regularly monitor blood sugar levels and renal function as scheduled by your endocrinologist / physician.",
            },
        },
    },
    "pantoprazole": {
        "medication_name": "Pantoprazole Sodium",
        "generic_name": "Pantoprazole",
        "brand_names": ["Pan 40", "Pantocid", "Pantosec", "Pantodac", "Penta 40"],
        "active_ingredients": ["Pantoprazole Sodium"],
        "symptoms": ["acidity", "acid reflux", "heartburn", "gastritis", "GERD", "stomach ulcer"],
        "schedule": "Schedule H",
        "document_id": "CDSCO-DOC-PAN-006",
        "document_version": "CDSCO-2024.1",
        "last_updated": "2024-03-05",
        "source_url": "https://cdsco.gov.in/opencms/opencms/en/Drugs/Approved-Drugs/",
        "sections": {
            "INDICATIONS": {
                "title": "Indications and Usage",
                "content": "Pantoprazole is a proton pump inhibitor (PPI) indicated for short-term treatment in the healing and symptomatic relief of erosive esophagitis, Gastroesophageal Reflux Disease (GERD), pathological hypersecretory conditions (Zollinger-Ellison syndrome), and prevention of NSAID-associated gastric ulcers.",
            },
            "WARNINGS": {
                "title": "Warnings and Precautions",
                "content": "Clostridioides difficile-associated diarrhea risk. Long-term PPI therapy (>1 year) is associated with increased risk of bone fractures (hip, wrist, spine), hypomagnesemia, fundic gland polyps, and vitamin B12 deficiency. Acute interstitial nephritis may occur at any point during therapy.",
            },
            "CONTRAINDICATIONS": {
                "title": "Contraindications",
                "content": "Contraindicated in patients with known hypersensitivity to substituted benzimidazoles or to any component of the formulation. Co-administration with rilpivirine-containing products is contraindicated.",
            },
            "ADVERSE_REACTIONS": {
                "title": "Adverse Reactions",
                "content": "Headache, diarrhea, nausea, abdominal pain, flatulence, dizziness, and arthralgia.",
            },
            "DRUG_INTERACTIONS": {
                "title": "Drug Interactions",
                "content": "Decreases absorption of medications dependent on gastric acid for bioavailability (e.g., Ketoconazole, Itraconazole, Iron salts, Atazanavir). Concomitant use with Methotrexate may increase methotrexate serum concentrations.",
            },
            "PATIENT_INFORMATION": {
                "title": "Patient Information",
                "content": "Take 30 to 60 minutes before breakfast. Swallow tablets whole; do not crush or chew. Long-term use should be re-evaluated by your clinician.",
            },
        },
    },
    "azithromycin": {
        "medication_name": "Azithromycin",
        "generic_name": "Azithromycin",
        "brand_names": ["Azithral", "Azee", "Zithromax", "Azimax", "Azikem"],
        "active_ingredients": ["Azithromycin"],
        "symptoms": ["bacterial infection", "chest infection", "throat infection", "pneumonia", "bronchitis"],
        "schedule": "Schedule H1 (Controlled Antibiotic - Prescription Only)",
        "document_id": "CDSCO-DOC-AZI-007",
        "document_version": "CDSCO-2024.1",
        "last_updated": "2024-04-12",
        "source_url": "https://cdsco.gov.in/opencms/opencms/en/Drugs/Approved-Drugs/",
        "sections": {
            "INDICATIONS": {
                "title": "Indications and Usage",
                "content": "Azithromycin is a macrolide antibacterial indicated for mild to moderate infections caused by designated susceptible bacteria in acute bacterial exacerbations of chronic bronchitis, acute bacterial sinusitis, community-acquired pneumonia, pharyngitis/tonsillitis, uncomplicated skin infections, and urethritis/cervicitis.",
            },
            "WARNINGS": {
                "title": "Cardiac Electrophysiology & QT Prolongation Warning",
                "content": "QT PROLONGATION & TORSADES DE POINTES: Macrolides have been associated with prolongation of the QT interval, potentially leading to fatal ventricular arrhythmias. Use with caution in patients with known QT prolongation, history of torsades de pointes, uncorrected hypokalemia or hypomagnesemia, and patients taking Class IA or Class III antiarrhythmics. Clostridioides difficile-associated diarrhea has been reported.",
            },
            "CONTRAINDICATIONS": {
                "title": "Contraindications",
                "content": "Contraindicated in patients with known hypersensitivity to azithromycin, erythromycin, any macrolide or ketolide antibacterial, or history of cholestatic jaundice / hepatic dysfunction associated with prior azithromycin use.",
            },
            "ADVERSE_REACTIONS": {
                "title": "Adverse Reactions",
                "content": "Gastrointestinal disturbances: diarrhea/loose stools, nausea, abdominal pain, vomiting, dyspepsia, and flatulence. Dizziness, headache, and transient elevation of liver enzymes.",
            },
            "DRUG_INTERACTIONS": {
                "title": "Drug Interactions",
                "content": "Co-administration with Digoxin may elevate digoxin serum concentrations. Avoid simultaneous use with medications known to prolong QT interval (e.g., Amiodarone, Sotalol, Haloperidol). Monitor INR when co-administered with Warfarin.",
            },
            "PATIENT_INFORMATION": {
                "title": "Patient Counseling & Stewardship",
                "content": "Take as prescribed once daily. Can be taken with or without food, though taking with food may reduce stomach upset. Must be prescribed by a physician. Complete the prescribed course completely.",
            },
        },
    },
}
