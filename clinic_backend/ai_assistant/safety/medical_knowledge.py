import re
from typing import Dict, List, Any, Optional, Tuple

# ==============================================================================
# 1. MEDICAL TERMINOLOGY & ABBREVIATION DICTIONARY
# ==============================================================================
MEDICAL_ABBREVIATIONS: Dict[str, Dict[str, str]] = {
    "bp": {"expansion": "Blood Pressure", "category": "Vitals"},
    "hr": {"expansion": "Heart Rate", "category": "Vitals"},
    "pr": {"expansion": "Pulse Rate", "category": "Vitals"},
    "rr": {"expansion": "Respiratory Rate", "category": "Vitals"},
    "spo2": {"expansion": "Oxygen Saturation", "category": "Vitals"},
    "temp": {"expansion": "Body Temperature", "category": "Vitals"},
    "dm": {"expansion": "Diabetes Mellitus", "category": "Endocrine"},
    "t2dm": {"expansion": "Type 2 Diabetes Mellitus", "category": "Endocrine"},
    "t1dm": {"expansion": "Type 1 Diabetes Mellitus", "category": "Endocrine"},
    "htn": {"expansion": "Hypertension (High Blood Pressure)", "category": "Cardiovascular"},
    "sob": {"expansion": "Shortness of Breath (Dyspnea)", "category": "Respiratory"},
    "uti": {"expansion": "Urinary Tract Infection", "category": "Genitourinary"},
    "gerd": {"expansion": "Gastroesophageal Reflux Disease (Acid Reflux)", "category": "Digestive"},
    "cad": {"expansion": "Coronary Artery Disease", "category": "Cardiovascular"},
    "mi": {"expansion": "Myocardial Infarction (Heart Attack)", "category": "Cardiovascular"},
    "ckd": {"expansion": "Chronic Kidney Disease", "category": "Renal"},
    "copd": {"expansion": "Chronic Obstructive Pulmonary Disease", "category": "Respiratory"},
    "pud": {"expansion": "Peptic Ulcer Disease", "category": "Digestive"},
    "dvt": {"expansion": "Deep Vein Thrombosis", "category": "Cardiovascular"},
    "cva": {"expansion": "Cerebrovascular Accident (Stroke)", "category": "Neurological"},
    "tia": {"expansion": "Transient Ischemic Attack", "category": "Neurological"},
    "uri": {"expansion": "Upper Respiratory Infection", "category": "Respiratory"},
    "urti": {"expansion": "Upper Respiratory Tract Infection", "category": "Respiratory"},
    "lrti": {"expansion": "Lower Respiratory Tract Infection", "category": "Respiratory"},
    "ibs": {"expansion": "Irritable Bowel Syndrome", "category": "Digestive"},
    "ibd": {"expansion": "Inflammatory Bowel Disease", "category": "Digestive"},
    "pcos": {"expansion": "Polycystic Ovary Syndrome", "category": "Endocrine"},
    "cbc": {"expansion": "Complete Blood Count", "category": "Laboratory"},
    "tlc": {"expansion": "Total Leukocyte Count (WBC)", "category": "Laboratory"},
    "lft": {"expansion": "Liver Function Test", "category": "Laboratory"},
    "kft": {"expansion": "Kidney Function Test", "category": "Laboratory"},
    "rft": {"expansion": "Renal Function Test", "category": "Laboratory"},
    "fbs": {"expansion": "Fasting Blood Sugar", "category": "Laboratory"},
    "ppbs": {"expansion": "Post-Prandial Blood Sugar", "category": "Laboratory"},
    "rbs": {"expansion": "Random Blood Sugar", "category": "Laboratory"},
    "hba1c": {"expansion": "Glycated Hemoglobin (3-Month Sugar Average)", "category": "Laboratory"},
    "sgot": {"expansion": "AST (Aspartate Aminotransferase)", "category": "Laboratory"},
    "sgpt": {"expansion": "ALT (Alanine Aminotransferase)", "category": "Laboratory"},
    "tsh": {"expansion": "Thyroid Stimulating Hormone", "category": "Laboratory"},
    "crp": {"expansion": "C-Reactive Protein (Inflammation Marker)", "category": "Laboratory"},
    "esr": {"expansion": "Erythrocyte Sedimentation Rate", "category": "Laboratory"},
    "otc": {"expansion": "Over-The-Counter Medication", "category": "Pharmacology"},
    "ecg": {"expansion": "Electrocardiogram", "category": "Diagnostic"},
    "ekg": {"expansion": "Electrocardiogram", "category": "Diagnostic"},
    "cxr": {"expansion": "Chest X-Ray", "category": "Radiology"},
    "usg": {"expansion": "Ultrasonography", "category": "Radiology"},
    "ct": {"expansion": "Computed Tomography Scan", "category": "Radiology"},
    "mri": {"expansion": "Magnetic Resonance Imaging", "category": "Radiology"},
}


def expand_medical_abbreviations(text: str) -> Tuple[str, List[Dict[str, str]]]:
    """
    Expands common clinical abbreviations in user text and returns identified terms.
    """
    expanded_terms = []
    processed_text = text
    text_lower = text.lower()

    for abbr, data in MEDICAL_ABBREVIATIONS.items():
        pattern = r"\b" + re.escape(abbr) + r"\b"
        if re.search(pattern, text_lower):
            expanded_terms.append({
                "abbreviation": abbr.upper(),
                "expansion": data["expansion"],
                "category": data["category"]
            })

    return processed_text, expanded_terms


# ==============================================================================
# 2. COMPREHENSIVE DISEASE & SYMPTOM PROTOCOLS ACROSS ALL BODY SYSTEMS
# ==============================================================================
COMPREHENSIVE_DISEASE_PROTOCOLS: Dict[str, Dict[str, Any]] = {
    # --- 1. RESPIRATORY SYSTEM ---
    "respiratory_infections": {
        "system": "Respiratory",
        "keywords": ["cough", "fever", "sore throat", "runny nose", "phlegm", "cold", "mucus", "sneezing", "congestion"],
        "name": "Respiratory Tract Infection / Cold",
        "red_flag_terms": ["coughing blood", "difficulty breathing", "stridor", "chest pain", "wheezing", "lips turning blue"],
        "differentials": [
            "Viral Upper Respiratory Tract Infection (Common Cold)",
            "Acute Bronchitis",
            "Influenza (Flu)",
            "COVID-19",
            "Acute Pharyngitis / Tonsillitis",
            "Pneumonia (if accompanied by high persistent fever & breathlessness)"
        ],
        "intake_questions": [
            "How many days have you had the cough or cold, and is it a dry cough or with phlegm/mucus?",
            "What is your approximate body temperature in °F or °C, and do you experience chills or shivering?",
            "Are you experiencing any shortness of breath, chest pain, or wheezing?"
        ],
        "default_otc": ["paracetamol", "cetirizine"],
    },
    "asthma_dyspnea": {
        "system": "Respiratory",
        "keywords": ["shortness of breath", "breathlessness", "wheezing", "tight chest", "asthma attack", "difficulty breathing"],
        "name": "Dyspnea / Asthma / Wheezing",
        "red_flag_terms": ["cannot speak full sentences", "gasping for air", "cyanosis", "severe chest tightness"],
        "differentials": [
            "Bronchial Asthma Exacerbation",
            "Acute Bronchospasm",
            "Chronic Obstructive Pulmonary Disease (COPD) Flare",
            "Pneumonia or Pulmonary Infection",
            "Cardiac Dyspnea (if associated with ankle swelling or chest pressure)"
        ],
        "intake_questions": [
            "Did the breathlessness begin suddenly or gradually, and do you hear a whistling or wheezing sound when breathing?",
            "Do you have a known history of asthma, allergies, or chronic lung conditions?",
            "Are you able to speak in complete sentences without needing to catch your breath?"
        ],
        "default_otc": [],
    },

    # --- 2. DIGESTIVE / GASTROINTESTINAL SYSTEM ---
    "acute_gastroenteritis": {
        "system": "Digestive",
        "keywords": ["diarrhea", "loose motion", "watery stool", "loose stools", "stomach bug", "food poisoning", "motions"],
        "name": "Acute Diarrhea / Gastroenteritis",
        "red_flag_terms": ["blood in stool", "black stool", "cannot keep fluids down", "extreme dizziness", "sunken eyes", "high fever"],
        "differentials": [
            "Acute Viral Gastroenteritis (Stomach Flu)",
            "Foodborne Illness / Bacterial Gastroenteritis",
            "Dietary Indiscretion / Osmotic Diarrhea",
            "Medication-Induced Loose Stools"
        ],
        "intake_questions": [
            "How many times today have you passed loose stools, and when did this begin?",
            "Have you noticed any fever, vomiting, blood or black color in the stool?",
            "Are you able to drink and retain fluids (like ORS, coconut water, or clear broth)?"
        ],
        "default_otc": ["paracetamol"],
    },
    "gastritis_gerd": {
        "system": "Digestive",
        "keywords": ["acidity", "heartburn", "acid reflux", "gerd", "stomach burning", "sour burps", "indigestion", "dyspepsia"],
        "name": "Gastritis / GERD / Hyperacidity",
        "red_flag_terms": ["vomiting blood", "coffee ground vomit", "difficulty swallowing", "unexplained weight loss", "black tarry stool"],
        "differentials": [
            "Gastroesophageal Reflux Disease (GERD)",
            "Acute Gastritis",
            "Functional Dyspepsia",
            "Peptic Ulcer Disease",
            "NSAID-Induced Gastric Irritation"
        ],
        "intake_questions": [
            "Does the burning sensation worsen after meals, upon lying down, or on an empty stomach?",
            "Have you had nausea, vomiting, or pain radiating up into your throat or chest?",
            "Are you currently taking pain medications (like ibuprofen or aspirin) or steroids?"
        ],
        "default_otc": ["pantoprazole"],
    },
    "abdominal_pain_acute": {
        "system": "Digestive",
        "keywords": ["stomach pain", "abdominal pain", "tummy ache", "belly cramps", "lower stomach pain", "upper stomach pain"],
        "name": "Abdominal Pain",
        "red_flag_terms": ["rigid board-like abdomen", "severe unbearable pain", "vomiting blood", "high fever", "pain in lower right abdomen"],
        "differentials": [
            "Acute Appendicitis (especially if pain localized to lower right abdomen)",
            "Cholecystitis / Gallstones (upper right abdomen, especially after fatty food)",
            "Renal Colic / Kidney Stone (flank pain radiating to groin)",
            "Intestinal Colic / Gastroenteritis",
            "Peptic Ulcer Disease / Gastritis"
        ],
        "intake_questions": [
            "Where precisely is the pain located (upper, lower, right side, or left side)?",
            "How severe is the pain on a scale of 1 to 10, and is it sharp, crampy, or constant?",
            "Do you have accompanying fever, vomiting, or inability to pass gas or stool?"
        ],
        "default_otc": [],
    },
    "nausea_vomiting": {
        "system": "Digestive",
        "keywords": ["vomiting", "throwing up", "nausea", "puking", "feeling sick"],
        "name": "Nausea & Vomiting",
        "red_flag_terms": ["vomiting blood", "coffee ground vomit", "severe headache with vomiting", "inability to retain fluids for 24 hours"],
        "differentials": [
            "Acute Gastroenteritis",
            "Food Poisoning",
            "Gastric Irritation / Gastritis",
            "Labyrinthitis / Vestibular Disorder (if associated with room-spinning vertigo)",
            "Migraine-Associated Nausea"
        ],
        "intake_questions": [
            "How many episodes of vomiting have you had, and are you able to keep small sips of water down?",
            "Is there any fever, severe abdominal pain, or blood in the vomit?",
            "Do you experience lightheadedness or dizziness when standing up?"
        ],
        "default_otc": [],
    },

    # --- 3. NEUROLOGICAL SYSTEM ---
    "headache_disorders": {
        "system": "Neurological",
        "keywords": ["headache", "head pain", "migraine", "throbbing head", "temple pain", "forehead pain"],
        "name": "Headache Disorder",
        "red_flag_terms": ["thunderclap", "worst headache of my life", "neck stiffness with fever", "slurred speech", "weakness on one side", "vision loss"],
        "differentials": [
            "Tension-Type Headache (bilateral band-like dull ache)",
            "Migraine (unilateral throbbing, nausea, light sensitivity)",
            "Sinus Headache (facial pressure, nasal congestion)",
            "Cervicogenic Headache (neck stiffness and occipital pain)",
            "Dehydration or Eyestrain Headache"
        ],
        "intake_questions": [
            "Where in your head is the pain located, and is it throbbing, dull, or sharp?",
            "How severe is the pain on a scale of 1 to 10?",
            "Do you have sensitivity to light or sound, nausea, visual aura, or neck stiffness?"
        ],
        "default_otc": ["paracetamol", "ibuprofen"],
    },
    "vertigo_dizziness": {
        "system": "Neurological",
        "keywords": ["dizzy", "dizziness", "vertigo", "spinning", "lightheaded", "loss of balance", "fainting feeling"],
        "name": "Dizziness / Vertigo",
        "red_flag_terms": ["fainting", "passed out", "slurred speech", "facial numbness", "inability to walk", "chest pain"],
        "differentials": [
            "Benign Paroxysmal Positional Vertigo (BPPV)",
            "Orthostatic Hypotension (dizziness on standing up)",
            "Hypoglycemia (especially in diabetic patients)",
            "Vestibular Neuritis / Labyrinthitis",
            "Dehydration / Anemia"
        ],
        "intake_questions": [
            "Does the room feel like it is spinning around you, or do you feel lightheaded as if you might faint?",
            "Does the dizziness occur specifically when you stand up or turn your head?",
            "Do you have any hearing changes, ringing in the ears (tinnitus), or weakness in your arms or legs?"
        ],
        "default_otc": [],
    },

    # --- 4. CARDIOVASCULAR SYSTEM ---
    "chest_discomfort": {
        "system": "Cardiovascular",
        "keywords": ["chest pain", "chest tightness", "chest pressure", "palpitations", "racing heart", "skipping heartbeat"],
        "name": "Chest Discomfort / Palpitations",
        "red_flag_terms": ["crushing chest pain", "radiating to left arm", "radiating to jaw", "sweating with chest pain", "syncope"],
        "differentials": [
            "Acute Coronary Syndrome / Angina (REQUIRES IMMEDIATE ER EVALUATION)",
            "Gastroesophageal Reflux Disease (GERD) / Esophageal Spasm",
            "Costochondritis (musculoskeletal inflammation tender to touch)",
            "Anxiety / Panic Reaction (with hyperventilation)",
            "Cardiac Arrhythmia / Tachycardia"
        ],
        "intake_questions": [
            "Can you describe the feeling: is it a pressure, burning, sharp pain, or racing heartbeat?",
            "Does the sensation radiate to your left arm, neck, jaw, or back?",
            "Are you experiencing any shortness of breath, cold sweating, or dizziness?"
        ],
        "default_otc": [],
    },

    # --- 5. MUSCULOSKELETAL SYSTEM ---
    "joint_muscle_pain": {
        "system": "Musculoskeletal",
        "keywords": ["joint pain", "knee pain", "back pain", "body ache", "muscle pain", "arthritis", "stiffness", "sprain", "myalgia"],
        "name": "Musculoskeletal & Joint Pain",
        "red_flag_terms": ["joint hot and red with high fever", "loss of bowel or bladder control", "sudden leg numbness", "inability to bear weight"],
        "differentials": [
            "Mechanical Back Strain / Lumbar Muscle Spasm",
            "Osteoarthritis (degenerative wear and tear)",
            "Viral Myalgia / Body Aches",
            "Tendonitis / Ligamentous Sprain",
            "Inflammatory Arthritis / Gout (if acute hot swollen joint)"
        ],
        "intake_questions": [
            "Which specific joint or muscle is affected, and was there any recent fall or heavy lifting?",
            "How severe is the discomfort on a scale of 1 to 10, and does it worsen with movement or rest?",
            "Is there any visible swelling, redness, or morning stiffness lasting more than 30 minutes?"
        ],
        "default_otc": ["paracetamol", "ibuprofen"],
    },

    # --- 6. DERMATOLOGICAL SYSTEM ---
    "dermatology_allergy": {
        "system": "Dermatological",
        "keywords": ["rash", "itching", "hives", "skin allergy", "red spots", "blisters", "eczema", "skin bumps", "pruritus"],
        "name": "Dermatological Rash / Urticaria",
        "red_flag_terms": ["swelling of lips", "swelling of tongue", "difficulty breathing", "skin peeling", "blisters inside mouth"],
        "differentials": [
            "Acute Urticaria (Hives / Allergic Reaction)",
            "Contact Dermatitis (reaction to soap, detergent, or substance)",
            "Atopic Dermatitis / Eczema",
            "Fungal Infection (Tinea / Ringworm)",
            "Drug-Induced Exanthem"
        ],
        "intake_questions": [
            "Where on your body did the rash first appear, and is it actively spreading or itching?",
            "Did you recently start any new medication, food, cosmetics, or chemical exposure?",
            "Are you experiencing any swelling of your face, lips, tongue, or difficulty breathing?"
        ],
        "default_otc": ["cetirizine"],
    },

    # --- 7. GENITOURINARY SYSTEM ---
    "urinary_symptoms": {
        "system": "Genitourinary",
        "keywords": ["burning urination", "urine burning", "frequent urination", "uti", "urine pain", "cloudy urine", "dysuria"],
        "name": "Urinary Symptoms / Dysuria",
        "red_flag_terms": ["blood in urine", "high fever with chills", "severe flank or back pain", "inability to pass urine"],
        "differentials": [
            "Lower Urinary Tract Infection (Acute Cystitis)",
            "Urethritis",
            "Urinary Dehydration / Concentrated Urine Irritation",
            "Renal Calculi / Kidney Stone (if accompanied by severe flank spasms)"
        ],
        "intake_questions": [
            "How long have you felt the burning sensation, and are you needing to urinate much more frequently?",
            "Have you noticed any fever, shivering, lower back/flank pain, or blood in the urine?",
            "Are you able to pass urine freely without blockage or extreme difficulty?"
        ],
        "default_otc": [],
    },

    # --- 8. ENDOCRINE & METABOLIC SYSTEM ---
    "diabetes_metabolic": {
        "system": "Endocrine & Metabolic",
        "keywords": ["high sugar", "diabetes", "blood sugar", "excessive thirst", "frequent urination at night", "shakiness", "low sugar"],
        "name": "Glycemic & Metabolic Symptoms",
        "red_flag_terms": ["confusion", "fruity breath odor", "deep rapid breathing", "loss of consciousness", "severe hypoglycemia"],
        "differentials": [
            "Uncontrolled Hyperglycemia (Type 2 Diabetes Mellitus)",
            "Acute Hypoglycemia (if shakiness, sweating, palpitations after missed meal)",
            "Metabolic Decompensation (requires urgent physician assessment)",
            "Medication Non-Adherence / Dosage Adjustment Requirement"
        ],
        "intake_questions": [
            "Have you recently checked your blood sugar (fasting or post-meal), and what was the reading?",
            "Do you have a known history of diabetes, and which medications (or insulin) do you take?",
            "Are you experiencing excessive thirst, unexpected weight loss, or severe shakiness and sweating?"
        ],
        "default_otc": ["metformin"],
    },

    # --- 9. GENERAL / FEVER & SYSTEMIC ---
    "fever_systemic": {
        "system": "General / Systemic",
        "keywords": ["fever", "high temperature", "chills", "feeling hot", "shivering", "pyrexia"],
        "name": "Fever & Systemic Illness",
        "red_flag_terms": ["stiff neck with fever", "fever above 103", "seizure", "unresponsive", "petechial rash", "difficulty breathing"],
        "differentials": [
            "Acute Viral Syndrome",
            "Upper Respiratory Tract Infection",
            "Acute Gastroenteritis",
            "Tropical Infection (Dengue, Malaria, Typhoid - if prolonged or high spikes)",
            "Urinary Tract Infection"
        ],
        "intake_questions": [
            "For how many days have you had the fever, and what is your highest recorded temperature in °F or °C?",
            "Is the fever accompanied by severe shivering (rigors), body aches, severe headache, or rash?",
            "Are you able to drink water and fluids comfortably, and have you taken any fever medicine today?"
        ],
        "default_otc": ["paracetamol"],
    },
}


# ==============================================================================
# 3. MEDICAL REPORT & LAB VALUE INTERPRETATION ENGINE
# ==============================================================================
LAB_TEST_REFERENCE_RANGES: Dict[str, Dict[str, Any]] = {
    "hemoglobin": {
        "names": ["hemoglobin", "hb", "hgb"],
        "unit": "g/dL",
        "normal_range": (12.0, 17.5),
        "low_label": "Low (Anemia)",
        "high_label": "Elevated (Polycythemia)",
        "clinical_significance": "Oxygen-carrying capacity of red blood cells.",
        "guidance": "Low levels suggest nutritional deficiency (iron/B12), blood loss, or chronic condition. High levels can occur with chronic smoking, dehydration, or altitude."
    },
    "wbc": {
        "names": ["wbc", "tlc", "white blood cells", "total leukocyte count"],
        "unit": "/mcL",
        "normal_range": (4000, 11000),
        "low_label": "Low (Leukopenia)",
        "high_label": "Elevated (Leukocytosis)",
        "clinical_significance": "Immune system cell count.",
        "guidance": "Elevated levels commonly point to acute bacterial or viral infection, inflammation, or physical stress. Low levels can occur in viral illnesses or bone marrow suppression."
    },
    "platelets": {
        "names": ["platelets", "platelet count", "plt"],
        "unit": "/mcL",
        "normal_range": (150000, 450000),
        "low_label": "Low (Thrombocytopenia)",
        "high_label": "Elevated (Thrombocytosis)",
        "clinical_significance": "Blood clotting and coagulation component.",
        "guidance": "Low counts are frequently seen in viral fevers (such as Dengue) and require monitoring to prevent bleeding. High counts can occur as a reactive inflammatory response."
    },
    "fasting_blood_sugar": {
        "names": ["fasting blood sugar", "fbs", "fasting glucose", "fasting sugar"],
        "unit": "mg/dL",
        "normal_range": (70, 99),
        "low_label": "Low (Hypoglycemia < 70)",
        "high_label": "High (Pre-diabetes: 100-125, Diabetes: >= 126)",
        "clinical_significance": "Basal metabolic blood sugar after 8 hours of fasting.",
        "guidance": "Fasting glucose >= 126 mg/dL on repeated testing suggests Diabetes Mellitus. Levels between 100-125 mg/dL indicate impaired fasting glucose (pre-diabetes)."
    },
    "post_prandial_blood_sugar": {
        "names": ["ppbs", "pp blood sugar", "post prandial glucose", "after meal sugar", "2 hour glucose"],
        "unit": "mg/dL",
        "normal_range": (70, 139),
        "low_label": "Low (< 70)",
        "high_label": "Elevated (>= 140 mg/dL)",
        "clinical_significance": "Blood glucose measured 2 hours post-meal.",
        "guidance": "Levels >= 200 mg/dL indicate Diabetes Mellitus. Levels between 140-199 mg/dL signify impaired glucose tolerance."
    },
    "random_blood_sugar": {
        "names": ["rbs", "random blood sugar", "random glucose", "blood sugar", "sugar level"],
        "unit": "mg/dL",
        "normal_range": (70, 140),
        "low_label": "Low (Hypoglycemia < 70)",
        "high_label": "Elevated (> 140 mg/dL, Diabetes threshold >= 200)",
        "clinical_significance": "Blood glucose at any unscheduled time of day.",
        "guidance": "A random blood glucose >= 200 mg/dL accompanied by symptoms like excessive thirst or urination is diagnostic of diabetes."
    },
    "hba1c": {
        "names": ["hba1c", "glycated hemoglobin", "a1c"],
        "unit": "%",
        "normal_range": (4.0, 5.6),
        "low_label": "Normal/Low",
        "high_label": "Elevated (Pre-diabetes: 5.7-6.4%, Diabetes: >= 6.5%)",
        "clinical_significance": "Estimated 3-month average blood glucose control.",
        "guidance": "HbA1c >= 6.5% indicates diabetes. For established diabetic patients, the standard target is usually under 7.0% under physician supervision."
    },
    "creatinine": {
        "names": ["serum creatinine", "creatinine", "creat"],
        "unit": "mg/dL",
        "normal_range": (0.6, 1.2),
        "low_label": "Low",
        "high_label": "Elevated (Renal Impairment)",
        "clinical_significance": "Primary marker of kidney filtration efficiency.",
        "guidance": "Elevated creatinine indicates reduced renal filtration and may signify acute dehydration, kidney strain, or chronic kidney disease. Requires doctor review."
    },
    "blood_urea": {
        "names": ["blood urea", "urea", "bun"],
        "unit": "mg/dL",
        "normal_range": (15, 45),
        "low_label": "Low",
        "high_label": "Elevated",
        "clinical_significance": "Nitrogenous waste product from protein breakdown.",
        "guidance": "Elevated urea along with creatinine indicates renal impairment or severe dehydration."
    },
    "sgpt_alt": {
        "names": ["sgpt", "alt", "alanine aminotransferase"],
        "unit": "U/L",
        "normal_range": (7, 56),
        "low_label": "Normal",
        "high_label": "Elevated (Hepatocellular Strain)",
        "clinical_significance": "Liver-specific cellular enzyme.",
        "guidance": "Elevated ALT indicates inflammation of liver cells, which can occur with viral hepatitis, fatty liver, alcohol, or hepatotoxic medications."
    },
    "sgot_ast": {
        "names": ["sgot", "ast", "aspartate aminotransferase"],
        "unit": "U/L",
        "normal_range": (10, 40),
        "low_label": "Normal",
        "high_label": "Elevated",
        "clinical_significance": "Enzyme present in liver, heart, and muscle tissue.",
        "guidance": "Elevated levels along with SGPT point to liver inflammation."
    },
    "total_cholesterol": {
        "names": ["total cholesterol", "cholesterol", "serum cholesterol"],
        "unit": "mg/dL",
        "normal_range": (120, 199),
        "low_label": "Low",
        "high_label": "Elevated (Borderline: 200-239, High: >= 240)",
        "clinical_significance": "Overall circulating blood cholesterol.",
        "guidance": "Elevated cholesterol increases cardiovascular risk. Lifestyle changes (diet, aerobic activity) and medical review are recommended."
    },
    "tsh": {
        "names": ["tsh", "thyroid stimulating hormone"],
        "unit": "mIU/L",
        "normal_range": (0.4, 4.5),
        "low_label": "Low (Hyperthyroidism Suspected)",
        "high_label": "Elevated (Hypothyroidism Suspected)",
        "clinical_significance": "Pituitary regulator of thyroid gland function.",
        "guidance": "High TSH indicates an underactive thyroid (hypothyroidism), which can cause fatigue and weight gain. Low TSH suggests overactivity (hyperthyroidism)."
    },
}


def parse_lab_reports_from_text(text: str) -> List[Dict[str, Any]]:
    """
    Scans patient input for laboratory test values, compares against
    authoritative reference ranges, and returns structured flags (High/Normal/Low).
    """
    found_reports = []
    text_clean = text.lower()

    for test_key, test_meta in LAB_TEST_REFERENCE_RANGES.items():
        for name in test_meta["names"]:
            # Pattern: "hb = 10.2", "hb: 10.2", "hb 10.2 g/dl", "fasting sugar is 150"
            pattern = r"\b" + re.escape(name) + r"\s*(?:=|:|is|\s)\s*(\d+(?:\.\d+)?)\s*(?:[a-zA-Z/%]+)?"
            match = re.search(pattern, text_clean)
            if match:
                try:
                    val = float(match.group(1))
                    low, high = test_meta["normal_range"]
                    if val < low:
                        flag = "LOW"
                        flag_label = test_meta["low_label"]
                    elif val > high:
                        flag = "HIGH"
                        flag_label = test_meta["high_label"]
                    else:
                        flag = "NORMAL"
                        flag_label = "Within Normal Limits"

                    found_reports.append({
                        "test_name": test_meta["names"][0].title(),
                        "value": val,
                        "unit": test_meta["unit"],
                        "reference_range": f"{low} - {high} {test_meta['unit']}",
                        "flag": flag,
                        "flag_label": flag_label,
                        "guidance": test_meta["guidance"],
                    })
                    break
                except (ValueError, IndexError):
                    continue

    return found_reports


# ==============================================================================
# 4. INTENT CLASSIFIER
# ==============================================================================
INTENT_CATEGORIES = [
    "EMERGENCY",
    "SYMPTOM_INQUIRY",
    "MEDICATION_QUESTION",
    "REPORT_QUESTION",
    "ALLERGY_QUESTION",
    "MEDICAL_HISTORY",
    "APPOINTMENT",
    "HOSPITAL_INFORMATION",
    "GENERAL_HEALTH_QUESTION",
]


def classify_user_intent(user_text: str, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Classifies user message into a clinical conversation intent.
    """
    text_lower = user_text.lower().strip()

    # 1. Check lab reports first
    reports = parse_lab_reports_from_text(text_lower)
    if reports or any(term in text_lower for term in ["report", "lab result", "blood test", "test result", "hba1c", "creatinine", "hemoglobin"]):
        return "REPORT_QUESTION"

    # 2. Check appointment requests
    if any(k in text_lower for k in ["book appointment", "see a doctor", "schedule appointment", "doctor visit", "appointment with"]):
        return "APPOINTMENT"

    # 3. Check allergy queries
    if any(k in text_lower for k in ["am allergic to", "can i take", "allergy to", "allergic reaction to", "conflict with my allergy"]):
        return "ALLERGY_QUESTION"

    # 4. Check pure medication queries
    med_keywords = ["dose", "dosage", "side effects", "how to take", "what is this medicine", "tablets", "syrup", "capsule", "contraindications", "uses of"]
    if any(k in text_lower for k in med_keywords) and not any(s in text_lower for s in ["i have", "suffering", "my stomach", "pain in"]):
        return "MEDICATION_QUESTION"

    # 5. Check hospital information
    if any(k in text_lower for k in ["hospital timing", "visiting hours", "where is the hospital", "departments available", "bed available", "ambulance number"]):
        return "HOSPITAL_INFORMATION"

    # 6. Check medical history discussion
    if any(k in text_lower for k in ["my history", "i had surgery", "diagnosed with", "past medical", "chronic condition"]):
        return "MEDICAL_HISTORY"

    # 7. Check symptom inquiries (default for personal complaint descriptions)
    symptom_triggers = ["i have", "feeling", "suffering", "pain", "fever", "cough", "headache", "vomit", "stomach", "rash", "dizzy", "hurt", "burn", "ache"]
    if any(s in text_lower for s in symptom_triggers):
        return "SYMPTOM_INQUIRY"

    return "GENERAL_HEALTH_QUESTION"


# ==============================================================================
# 5. CONVERSATION STATE & ATTRIBUTE EXTRACTOR
# ==============================================================================
def extract_clinical_state_attributes(full_text: str) -> Dict[str, Any]:
    """
    Extracts structured clinical intake attributes from conversation text
    so that follow-up questioning never repeats an already-answered question.
    """
    text_lower = full_text.lower()

    # Duration parsing
    duration_match = re.search(r"\b(\d+\s*(?:days?|weeks?|hours?|months?)|since\s+\w+|yesterday|today|from\s+\w+)\b", text_lower)
    duration = duration_match.group(1) if duration_match else None

    # Temperature parsing
    temp_match = re.search(r"\b(\d{2,3}(?:\.\d+)?)\s*(?:°?\s*[fFcC]|deg|degrees?|fahrenheit|celsius)\b", text_lower)
    if not temp_match:
        temp_match = re.search(r"\b(?:temp|temperature|fever is)\s*(?:is|of)?\s*(\d{2,3}(?:\.\d+)?)\b", text_lower)
    temperature = temp_match.group(1) if temp_match else None

    # Severity parsing
    severity = None
    sev_num = re.search(r"\b(\d{1,2})\s*(?:out of 10|\/10|scale of 1 to 10)\b", text_lower)
    if sev_num:
        severity = f"{sev_num.group(1)}/10"
    elif "severe" in text_lower or "unbearable" in text_lower or "intense" in text_lower:
        severity = "Severe"
    elif "moderate" in text_lower:
        severity = "Moderate"
    elif "mild" in text_lower or "slight" in text_lower:
        severity = "Mild"

    # Location parsing
    location = None
    for loc in ["lower right", "lower left", "upper right", "upper left", "epigastric", "forehead", "temple", "back of head", "chest", "flank", "knee", "lower back", "throat"]:
        if loc in text_lower:
            location = loc.title()
            break

    # Age parsing
    age = None
    age_match = re.search(r"\b(?:i am|age is|age|i'm)?\s*(\d{1,2})\s*(?:years? old|yrs?|yo)\b", text_lower)
    if age_match:
        try:
            age = int(age_match.group(1))
        except ValueError:
            pass

    return {
        "duration": duration,
        "temperature": temperature,
        "severity": severity,
        "location": location,
        "age": age,
    }
