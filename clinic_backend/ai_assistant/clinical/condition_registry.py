"""
Universal Clinical Condition Registry
Scalable configuration data model for clinical questioning, red-flag screening,
evidence-based self-care, medication education, and authoritative sources.
"""

from typing import Dict, List, Any, Optional

CONDITION_REGISTRY: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # GENERAL SYMPTOMS
    # =========================================================================
    "fever": {
        "condition": "fever",
        "displayName": "Fever",
        "category": "symptom",
        "keywords": [
            "fever", "high temperature", "running a temperature", "body feels hot",
            "febrile", "pyrexia", "feeling hot", "shivering", "feverish", "high temp",
            "have fever", "got fever", "temperature is high", "mild fever", "warm body"
        ],
        "questions": [
            {
                "id": "age",
                "question": "How old are you?",
                "first_turn_prefix": "I'm sorry you're feeling unwell. I can help you understand your symptoms and provide general health information.\n\n**First, how old are you?**",
                "required": True,
                "extraction_key": "age",
            },
            {
                "id": "duration",
                "question": "How long have you had the fever?",
                "required": True,
                "extraction_key": "duration",
            },
            {
                "id": "temperature",
                "question": "Do you know your current temperature? If possible, provide it in °C or °F.",
                "required": True,
                "extraction_key": "temperature",
            },
            {
                "id": "associated_symptoms",
                "question": "Do you have any other symptoms, such as cough, sore throat, headache, vomiting, diarrhea, body aches, rash, or difficulty breathing?",
                "required": True,
                "extraction_key": "associated_symptoms",
            },
        ],
        "red_flags": [
            "Fever exceeding 104°F (40°C) or unresponsive to cooling measures",
            "Severe headache with stiff neck or light sensitivity",
            "Shortness of breath, chest pain, or rapid breathing",
            "Confusion, extreme lethargy, drowsiness, or seizures",
            "Inability to retain fluids or persistent vomiting",
            "Unexplained dark purple or red skin rash (petechiae)",
        ],
        "possible_causes": [
            "Viral upper respiratory infection (common cold, flu)",
            "Acute viral illness or seasonal influenza",
            "Bacterial infection (such as tonsillitis, UTI, or bronchitis)",
            "Gastrointestinal infection (viral or bacterial gastroenteritis)",
        ],
        "general_advice": [
            "Stay well hydrated with clean water, oral rehydration solutions (ORS), clear broths, or coconut water.",
            "Prioritize physical rest to support immune recovery.",
            "Wear light, breathable clothing and keep the room at a comfortable, well-ventilated temperature.",
            "Lukewarm sponge baths can provide soothing comfort (avoid cold water or ice, which can cause shivering).",
        ],
        "medication_info": {
            "name": "Acetaminophen / Paracetamol",
            "general_use": "Used for temporary reduction of fever and relief of mild to moderate body pain.",
            "warnings": "Do not exceed maximum daily limits (typically 3,000–4,000 mg/day for adults, lower in children by weight) to prevent liver injury. Avoid alcohol. Check other cold medicines to avoid accidental double-dosing.",
            "contraindications": "Severe active liver disease or known hypersensitivity to paracetamol.",
            "adverse_effects": "Rare allergic skin reactions; gastrointestinal upset; hepatotoxicity in acute overdose.",
            "interactions": "Warfarin (chronic high doses may elevate bleeding risk); other paracetamol-containing remedies.",
        },
        "when_to_see_doctor": [
            "Fever persisting for more than 3 consecutive days",
            "Temperature exceeding 103°F (39.4°C) in adults or 100.4°F in infants",
            "Development of any warning signs (stiff neck, chest discomfort, breathing difficulty)",
            "Symptoms progressively worsening despite supportive care",
        ],
        "sources": [
            {"name": "CDSCO (Central Drugs Standard Control Organization)", "url": "https://cdsco.gov.in"},
            {"name": "WHO Clinical Management Guidelines", "url": "https://www.who.int"},
            {"name": "National Health Portal of India", "url": "https://www.nhp.gov.in"},
        ],
    },

    "headache": {
        "condition": "headache",
        "displayName": "Headache",
        "category": "symptom",
        "keywords": [
            "headache", "head pain", "head hurts", "my head is painful", "throbbing head",
            "pain in head", "head is aching", "severe headache", "bad headache"
        ],
        "questions": [
            {
                "id": "age",
                "question": "How old are you?",
                "first_turn_prefix": "I'm sorry you're dealing with a headache. I can help you understand your symptoms.\n\n**First, how old are you?**",
                "required": True,
                "extraction_key": "age",
            },
            {
                "id": "duration",
                "question": "How long have you had the headache?",
                "required": True,
                "extraction_key": "duration",
            },
            {
                "id": "severity",
                "question": "How severe is the headache on a scale from 1 to 10?",
                "required": True,
                "extraction_key": "severity",
            },
            {
                "id": "onset",
                "question": "Did the headache start suddenly (like a thunderclap) or develop gradually?",
                "required": True,
                "extraction_key": "onset",
            },
            {
                "id": "associated_symptoms",
                "question": "Do you have any symptoms such as vomiting, vision changes, weakness, numbness, confusion, fever, neck stiffness, or head injury?",
                "required": True,
                "extraction_key": "associated_symptoms",
            },
        ],
        "red_flags": [
            "Sudden, explosive 'thunderclap' headache reaching peak intensity within seconds",
            "Headache accompanied by high fever and a stiff neck",
            "Neurological deficits: one-sided weakness, slurred speech, confusion, or facial droop",
            "Vision loss, double vision, or aura lasting longer than 1 hour",
            "Headache following recent head trauma or physical impact",
        ],
        "possible_causes": [
            "Tension-type headache (stress, muscle strain, dehydration, prolonged screen time)",
            "Migraine episode (throbbing, sensitivity to light/sound, nausea)",
            "Cervicogenic or sinus headache (neck posture or sinus congestion)",
            "Dehydration or caffeine withdrawal",
        ],
        "general_advice": [
            "Rest in a quiet, dark, well-ventilated room.",
            "Drink plenty of water to rule out dehydration.",
            "Apply a warm or cool compress to your forehead or the back of your neck.",
            "Practice gentle neck stretches and minimize digital screen exposure.",
        ],
        "medication_info": {
            "name": "Acetaminophen / Paracetamol or Ibuprofen",
            "general_use": "Used for temporary relief of mild to moderate tension headache pain.",
            "warnings": "Avoid frequent daily use (over 2-3 days weekly) to prevent medication-overuse headaches. Take NSAIDs with food to protect stomach lining.",
            "contraindications": "Ibuprofen is contraindicated in active peptic ulcer disease, severe renal impairment, or aspirin allergy. Paracetamol contraindicated in severe hepatic impairment.",
            "adverse_effects": "Stomach irritation, nausea (NSAIDs); liver strain in paracetamol overdose.",
            "interactions": "Anticoagulants, ACE inhibitors, other analgesic medications.",
        },
        "when_to_see_doctor": [
            "Headache described as the 'worst headache of your life'",
            "Persistent headache worsening progressively over several days",
            "Headache triggered by coughing, sneezing, or physical exertion",
            "Accompanied by persistent nausea, vomiting, or neurological changes",
        ],
        "sources": [
            {"name": "International Headache Society (IHS) Guidelines", "url": "https://ihs-headache.org"},
            {"name": "CDSCO (Govt of India)", "url": "https://cdsco.gov.in"},
            {"name": "National Health Portal of India", "url": "https://www.nhp.gov.in"},
        ],
    },

    "cough": {
        "condition": "cough",
        "displayName": "Cough",
        "category": "symptom",
        "keywords": [
            "cough", "coughing", "hacking cough", "dry cough", "wet cough", "phlegm cough",
            "cough with mucus", "bad cough", "persistent cough", "barking cough"
        ],
        "questions": [
            {
                "id": "age",
                "question": "How old are you?",
                "first_turn_prefix": "I'm sorry you're dealing with a cough. I can help evaluate your symptoms.\n\n**First, how old are you?**",
                "required": True,
                "extraction_key": "age",
            },
            {
                "id": "duration",
                "question": "How long have you had the cough?",
                "required": True,
                "extraction_key": "duration",
            },
            {
                "id": "character",
                "question": "Is it a dry, tickly cough, or are you coughing up mucus/phlegm (productive cough)?",
                "required": True,
                "extraction_key": "character",
            },
            {
                "id": "associated_symptoms",
                "question": "Do you have any associated symptoms like fever, shortness of breath, chest pain, wheezing, or blood in your sputum?",
                "required": True,
                "extraction_key": "associated_symptoms",
            },
        ],
        "red_flags": [
            "Coughing up blood or blood-tinged rust-colored sputum (hemoptysis)",
            "Severe shortness of breath, rapid breathing, or stridor",
            "Sharp chest pain with deep breathing",
            "High fever persisting more than 3-4 days",
            "Unexplained weight loss or night sweats alongside chronic cough",
        ],
        "possible_causes": [
            "Viral upper respiratory infection (acute bronchitis, common cold)",
            "Post-nasal drip from allergic rhinitis or sinusitis",
            "Asthma or reactive airway bronchospasm",
            "Gastroesophageal reflux disease (acid irritating the airways)",
        ],
        "general_advice": [
            "Stay well hydrated with warm fluids like herbal tea, warm water, or clear broth to thin mucus.",
            "Use warm steam inhalation or a cool-mist humidifier in your room.",
            "A spoonful of honey (for adults and children over 1 year) can naturally soothe throat tickling.",
            "Avoid exposure to tobacco smoke, aerosol sprays, and harsh air pollutants.",
        ],
        "medication_info": {
            "name": "General Supportive Antitussive / Expectorant Information",
            "general_use": "Expectorants (e.g. guaifenesin) help loosen mucus; throat lozenges soothe irritation.",
            "warnings": "Antibiotics do NOT treat viral coughs and should never be taken without a bacterial diagnosis and doctor's prescription. Do not give OTC cough medicines to young children without pediatric guidance.",
            "contraindications": "Suppressive antitussives may not be appropriate in productive phlegm-producing coughs.",
            "adverse_effects": "Mild drowsiness, dry mouth, or stomach upset depending on formulation.",
            "interactions": "Sedating antihistamines combined with alcohol or sedatives.",
        },
        "when_to_see_doctor": [
            "Cough lasting longer than 3 weeks (chronic cough)",
            "Accompanied by high fever, wheezing, or breathing difficulty",
            "Presence of blood in coughed-up phlegm",
            "Cough disrupting sleep or causing significant chest soreness",
        ],
        "sources": [
            {"name": "WHO Clinical Guidance on Respiratory Infections", "url": "https://www.who.int"},
            {"name": "CDSCO (Govt of India)", "url": "https://cdsco.gov.in"},
            {"name": "National Health Portal of India", "url": "https://www.nhp.gov.in"},
        ],
    },

    "abdominal_pain": {
        "condition": "abdominal_pain",
        "displayName": "Abdominal Pain",
        "category": "symptom",
        "keywords": [
            "stomach hurts", "stomach pain", "abdominal pain", "tummy ache", "belly pain",
            "cramps in stomach", "pain in abdomen", "pain in belly", "stomach ache",
            "belly hurts", "cramping belly"
        ],
        "questions": [
            {
                "id": "age",
                "question": "How old are you?",
                "first_turn_prefix": "I'm sorry to hear your stomach hurts. I can help you evaluate your symptoms safely.\n\n**First, how old are you?**",
                "required": True,
                "extraction_key": "age",
            },
            {
                "id": "location_and_duration",
                "question": "Where in your stomach or abdomen is the pain located (upper, lower, right side, left side, or all over), and how long has it lasted?",
                "first_turn_prefix": "I'm sorry you are experiencing stomach or abdominal pain. I can help you evaluate your symptoms safely.\n\n**First, where in your stomach or abdomen is the pain located (upper, lower, right side, left side, or all over), and how long has it lasted?**",
                "required": True,
                "extraction_key": "location",
            },
            {
                "id": "character_and_severity",
                "question": "How would you describe the pain (cramping, sharp, dull, burning), and how severe is it from 1 to 10?",
                "required": True,
                "extraction_key": "severity",
            },
            {
                "id": "associated_symptoms",
                "question": "Are you having any vomiting, diarrhea, constipation, fever, blood in vomit or stool, or possibility of pregnancy?",
                "required": True,
                "extraction_key": "associated_symptoms",
            },
        ],
        "red_flags": [
            "Sudden, excruciating, rigid 'board-like' abdominal tenderness",
            "Pain localized severely in the lower right abdomen (potential acute appendicitis)",
            "Vomiting bright red blood or dark coffee-ground material",
            "Passing black, tarry stools (melena) or fresh blood in stool",
            "Severe pain accompanied by high fever, fainting, or inability to pass gas/stool",
            "Severe lower abdominal pain with possibility of pregnancy (ectopic pregnancy risk)",
        ],
        "possible_causes": [
            "Gastritis, acid peptic disorder, or functional dyspepsia",
            "Acute gastroenteritis or food intolerance",
            "Irritable bowel syndrome (IBS) or constipation",
            "Menstrual cramping or mild muscle strain",
        ],
        "general_advice": [
            "Sip clear fluids (water, ORS, weak tea) to stay hydrated; avoid large heavy meals.",
            "Avoid NSAIDs (like ibuprofen or aspirin) as they can worsen gastric mucosal irritation.",
            "Avoid spicy, greasy, acidic, or fried foods, as well as dairy and alcohol.",
            "Rest comfortably with a warm heating pad on the abdomen if the pain is mild and non-acute.",
        ],
        "medication_info": {
            "name": "Antacids or Proton Pump Inhibitors (Pantoprazole / Omeprazole)",
            "general_use": "Used for symptomatic relief of acid-related indigestion, heartburn, and gastritis.",
            "warnings": "Do NOT take strong analgesics or NSAIDs for unexplained abdominal pain as they mask surgical signs and aggravate stomach lining.",
            "contraindications": "Hypersensitivity to PPIs; severe electrolyte disturbances.",
            "adverse_effects": "Headache, mild diarrhea or constipation, nausea.",
            "interactions": "Ketoconazole, clopidogrel, methotrexate depending on specific agent.",
        },
        "when_to_see_doctor": [
            "Severe or worsening pain persisting for more than 24 hours",
            "Pain localized sharply to the lower right abdomen",
            "Inability to keep liquids down for more than 12-24 hours",
            "Any signs of gastrointestinal bleeding or high fever",
        ],
        "sources": [
            {"name": "World Gastroenterology Organisation (WGO)", "url": "https://www.worldgastroenterology.org"},
            {"name": "CDSCO (Govt of India)", "url": "https://cdsco.gov.in"},
            {"name": "National Health Portal of India", "url": "https://www.nhp.gov.in"},
        ],
    },

    "chest_discomfort": {
        "condition": "chest_discomfort",
        "displayName": "Chest Discomfort",
        "category": "symptom",
        "keywords": [
            "chest pain", "chest discomfort", "chest pressure", "pain in chest",
            "tightness in chest", "chest tightness", "chest ache", "heaviness in chest"
        ],
        "questions": [
            {
                "id": "red_flag_screening",
                "question": "Chest pain requires immediate clinical safety screening. **Is the chest pain severe or crushing, did it start suddenly, and is it spreading to your arm, shoulder, jaw, neck, or back, or accompanied by sweating, faintness, or difficulty breathing?**",
                "first_turn_prefix": "Chest pain requires immediate clinical safety screening. **Is the chest pain severe or crushing, did it start suddenly, and is it spreading to your arm, shoulder, jaw, neck, or back, or accompanied by sweating, faintness, or difficulty breathing?**",
                "required": True,
                "extraction_key": "red_flag_check",
            },
            {
                "id": "age",
                "question": "How old are you?",
                "required": True,
                "extraction_key": "age",
            },
            {
                "id": "character_and_movement",
                "question": "Does the discomfort change when you take a deep breath, press on your chest wall, or change body position?",
                "required": True,
                "extraction_key": "character",
            },
            {
                "id": "duration_and_history",
                "question": "How long has it lasted, and do you have a history of heart conditions, high blood pressure, asthma, or acid reflux?",
                "required": True,
                "extraction_key": "history",
            },
        ],
        "red_flags": [
            "Crushing, squeezing, heavy, or pressing chest pain (substernal)",
            "Pain radiating to left arm, shoulder, neck, jaw, or upper back",
            "Shortness of breath, dizziness, cold sweating (diaphoresis), or syncope",
            "Sudden tearing sensation in the chest or back",
            "Rapid irregular heartbeat or bluish discoloration of lips",
        ],
        "possible_causes": [
            "Musculoskeletal chest wall strain or costochondritis (worse with palpation or movement)",
            "Gastroesophageal reflux disease (acid reflux causing burning retrosternal sensation)",
            "Anxiety, panic attacks, or hyperventilation",
            "Cardiac or pulmonary etiology requiring clinical exclusion",
        ],
        "general_advice": [
            "Stop any physical exertion immediately and sit in a comfortable, upright resting position.",
            "Loosen any restrictive clothing around your neck and chest.",
            "Take slow, gentle breaths to keep calm.",
            "Never ignore chest pain; in-person medical evaluation with an ECG is the gold standard.",
        ],
        "medication_info": {
            "name": "Clinical Evaluation Note",
            "general_use": "Do not self-medicate for unexplained chest pain without confirmed clinical diagnosis.",
            "warnings": "Chest pain must never be assumed benign without professional medical evaluation and ECG testing.",
            "contraindications": "Avoid unprescribed cardiac medications (like nitrates).",
            "adverse_effects": "Varies by clinical intervention.",
            "interactions": "Nitrates contraindicated with PDE-5 inhibitors due to profound hypotension.",
        },
        "when_to_see_doctor": [
            "Any unexplained chest pain warrants urgent in-person medical evaluation",
            "Call emergency services immediately if pain is crushing or radiating",
            "Schedule hospital consultation if pain is recurrent or related to exertion",
        ],
        "sources": [
            {"name": "American Heart Association (AHA) / ACC Guidelines", "url": "https://www.heart.org"},
            {"name": "Cardiological Society of India (CSI)", "url": "https://csi.org.in"},
            {"name": "CDSCO (Govt of India)", "url": "https://cdsco.gov.in"},
        ],
    },

    "shortness_of_breath": {
        "condition": "shortness_of_breath",
        "displayName": "Shortness of Breath",
        "category": "symptom",
        "keywords": [
            "difficulty breathing", "shortness of breath", "trouble breathing", "breathless",
            "hard to breathe", "cannot breathe", "gasping", "breathlessness", "dyspnea",
            "struggling to breathe"
        ],
        "questions": [
            {
                "id": "emergency_screening",
                "question": "Breathing difficulty requires immediate safety assessment. **Are you struggling to breathe right now, gasping for air, unable to speak in full sentences, or experiencing blue/pale lips or chest pain?**",
                "first_turn_prefix": "Breathing difficulty requires immediate safety assessment. **Are you struggling to breathe right now, gasping for air, unable to speak in full sentences, or experiencing blue/pale lips or chest pain?**",
                "required": True,
                "extraction_key": "emergency_check",
            },
            {
                "id": "age",
                "question": "How old are you?",
                "required": True,
                "extraction_key": "age",
            },
            {
                "id": "onset_and_duration",
                "question": "Did this start suddenly or develop gradually, and how long have you noticed it?",
                "required": True,
                "extraction_key": "duration",
            },
            {
                "id": "triggers_and_history",
                "question": "Do you have wheezing, cough, fever, leg swelling, or a personal history of asthma, COPD, or allergies?",
                "required": True,
                "extraction_key": "history",
            },
        ],
        "red_flags": [
            "Severe inability to catch your breath or gasping for air",
            "Bluish or grayish coloration of the lips, face, or fingernails (cyanosis)",
            "Stridor (high-pitched whistling sound during inhalation) or severe airway narrowing",
            "Chest pain, rapid faint pulse, or confusion accompanying breathlessness",
            "Sudden onset following surgery, long flight, or immobilization (pulmonary embolism concern)",
        ],
        "possible_causes": [
            "Asthma bronchospasm or allergic airway reaction",
            "Acute viral bronchitis, pneumonia, or respiratory tract infection",
            "Anxiety, panic episode, or hyperventilation syndrome",
            "Deconditioning, anemia, or cardiac/pulmonary congestion",
        ],
        "general_advice": [
            "Sit upright leaning slightly forward (tripod position) with arms supported on a table.",
            "Practice pursed-lip breathing: inhale gently through your nose and exhale slowly through pursed lips.",
            "Ensure the space has plenty of fresh, well-ventilated air; avoid fans blowing directly in cold drafts.",
            "If you have a prescribed rescue inhaler (e.g. salbutamol) for diagnosed asthma, use it as prescribed.",
        ],
        "medication_info": {
            "name": "Bronchodilator (Salbutamol Inhaler - for diagnosed asthma only)",
            "general_use": "Used as a fast-acting rescue bronchodilator for reversible airway obstruction.",
            "warnings": "Overuse of rescue inhalers without doctor review can mask worsening underlying asthma.",
            "contraindications": "Known hypersensitivity; caution in severe cardiac arrhythmias.",
            "adverse_effects": "Mild tremor, palpitations, transient tachycardia, headache.",
            "interactions": "Beta-blockers can antagonize bronchodilation effects.",
        },
        "when_to_see_doctor": [
            "Any sudden, unexplained, or worsening shortness of breath",
            "Breathlessness accompanied by fever, productive cough, or wheeze",
            "Inability to perform normal daily activities without getting breathless",
        ],
        "sources": [
            {"name": "Global Initiative for Asthma (GINA)", "url": "https://ginasthma.org"},
            {"name": "WHO Clinical Guidelines", "url": "https://www.who.int"},
            {"name": "National Health Portal of India", "url": "https://www.nhp.gov.in"},
        ],
    },

    "vomiting": {
        "condition": "vomiting",
        "displayName": "Vomiting and Nausea",
        "category": "symptom",
        "keywords": [
            "vomiting", "throwing up", "puking", "vomited", "threw up", "feeling sick",
            "nauseous", "nausea", "urge to vomit", "cannot keep food down"
        ],
        "questions": [
            {
                "id": "age",
                "question": "How old are you?",
                "first_turn_prefix": "I'm sorry you are vomiting. Let's look at your symptoms.\n\n**First, how old are you?**",
                "required": True,
                "extraction_key": "age",
            },
            {
                "id": "duration_and_frequency",
                "question": "How long have you been vomiting, and approximately how many times have you vomited today?",
                "required": True,
                "extraction_key": "duration",
            },
            {
                "id": "hydration_and_character",
                "question": "Are you able to keep small sips of water or ORS down, and have you noticed any blood or dark coffee-ground material in the vomit?",
                "required": True,
                "extraction_key": "character",
            },
            {
                "id": "associated_symptoms",
                "question": "Do you have any severe abdominal pain, high fever, diarrhea, severe headache, or dizziness when standing up?",
                "required": True,
                "extraction_key": "associated_symptoms",
            },
        ],
        "red_flags": [
            "Vomiting bright red blood or dark coffee-ground material",
            "Inability to retain any liquids for over 12-24 hours leading to severe dehydration",
            "Severe dizziness, fainting, or dry mouth with absent urination",
            "Severe sharp or rigid abdominal pain",
            "Severe headache with neck stiffness and vomiting",
        ],
        "possible_causes": [
            "Acute viral gastroenteritis (stomach flu)",
            "Food poisoning or bacterial foodborne toxins",
            "Gastritis or acid peptic reflux irritation",
            "Motion sickness, migraine, or pregnancy-related nausea",
        ],
        "general_advice": [
            "Wait 30-60 minutes after vomiting before drinking, then take very small sips of oral rehydration solution (ORS) or electrolyte water every 5 minutes.",
            "Avoid chugging large glasses of water at once as it triggers the stomach stretch reflex.",
            "Avoid solid food until vomiting has settled for several hours, then introduce bland items (rice, toast, bananas).",
            "Avoid dairy, greasy, fried, sugary, or spicy foods.",
        ],
        "medication_info": {
            "name": "Oral Rehydration Salts (ORS) & Antiemetic Information",
            "general_use": "ORS is the cornerstone of safe recovery to restore water and lost electrolytes (sodium, potassium).",
            "warnings": "Prescription antiemetics (e.g. ondansetron) should only be taken when prescribed by a doctor after clinical evaluation.",
            "contraindications": "Severe bowel obstruction or perforation.",
            "adverse_effects": "Rare mild constipation or headache with antiemetics.",
            "interactions": "QT-prolonging medications with certain antiemetic agents.",
        },
        "when_to_see_doctor": [
            "Vomiting lasting more than 24 hours in adults or 12 hours in young children",
            "Signs of dehydration: extreme thirst, dark urine, sunken eyes, or lightheadedness",
            "Inability to retain essential prescribed medications",
            "Any presence of blood in vomit or severe abdominal pain",
        ],
        "sources": [
            {"name": "WHO Guidelines on Dehydration & Diarrheal Diseases", "url": "https://www.who.int"},
            {"name": "CDSCO (Govt of India)", "url": "https://cdsco.gov.in"},
            {"name": "National Health Portal of India", "url": "https://www.nhp.gov.in"},
        ],
    },

    "diarrhea": {
        "condition": "diarrhea",
        "displayName": "Diarrhea",
        "category": "symptom",
        "keywords": [
            "diarrhea", "loose motion", "watery stool", "loose stools", "upset stomach",
            "frequent stool", "motions", "loose motion since", "watery motions", "runny stool"
        ],
        "questions": [
            {
                "id": "age",
                "question": "How old are you?",
                "first_turn_prefix": "I'm sorry you are experiencing loose motions. I can help you understand your symptoms and provide general health information.\n\n**First, how old are you?**",
                "required": True,
                "extraction_key": "age",
            },
            {
                "id": "duration_and_frequency",
                "question": "How long have you had loose motions or loose stools, and approximately how many times have you passed stool today?",
                "first_turn_prefix": "I'm sorry you are experiencing loose motions. I can help you understand your symptoms and provide general health information.\n\n**First, how long have you had loose motions or loose stools, and approximately how many times have you passed stool today?**",
                "required": True,
                "extraction_key": "duration",
            },
            {
                "id": "stool_character_and_red_flags",
                "question": "Have you noticed any blood, black color, or mucus in the stool, high fever, or severe stomach cramping?",
                "required": True,
                "extraction_key": "character",
            },
            {
                "id": "hydration_status",
                "question": "Are you able to drink and retain fluids (like ORS, coconut water, or water) without vomiting?",
                "required": True,
                "extraction_key": "hydration",
            },
        ],
        "red_flags": [
            "Blood or black tarry material in the stool (dysentery)",
            "High fever exceeding 102°F (38.9°C)",
            "Signs of severe dehydration: little or no urine, sunken eyes, dry mouth, or dizziness upon standing",
            "Severe unremitting abdominal pain",
            "Diarrhea lasting more than 7 days without improvement",
        ],
        "possible_causes": [
            "Acute viral gastroenteritis (rotavirus, norovirus)",
            "Bacterial foodborne infection (Salmonella, Campylobacter, E. coli)",
            "Dietary indiscretion, lactose intolerance, or food sensitivity",
            "Medication side effect (especially recent antibiotic use)",
        ],
        "general_advice": [
            "Drink Oral Rehydration Salts (ORS) solution regularly after each loose stool to replenish lost electrolytes.",
            "Eat light, easily digestible foods such as curd (probiotic yogurt), khichdi, rice, bananas, and toast.",
            "Avoid caffeine, alcohol, milk, greasy foods, and artificial sweeteners which can aggravate diarrhea.",
            "Wash hands thoroughly with soap and water to prevent the spread of gastrointestinal germs.",
        ],
        "medication_info": {
            "name": "Oral Rehydration Salts (ORS) & Zinc / Probiotics",
            "general_use": "ORS is the primary evidence-based clinical treatment to prevent dehydration.",
            "warnings": "Do NOT take anti-motility drugs (like loperamide) if you have fever or blood in your stool, as stopping motility can worsen bacterial toxins. Avoid unprescribed antibiotics.",
            "contraindications": "Severe intestinal obstruction.",
            "adverse_effects": "Very safe when mixed with the correct volume of clean drinking water.",
            "interactions": "None significant for standard ORS formulations.",
        },
        "when_to_see_doctor": [
            "Diarrhea persisting for more than 48 hours without improvement",
            "Presence of blood, black stool, or high fever",
            "Signs of progressive dehydration or inability to retain fluids",
            "Severe abdominal cramping or pain",
        ],
        "sources": [
            {"name": "WHO Clinical Guidelines on Diarrheal Diseases", "url": "https://www.who.int"},
            {"name": "CDSCO (Govt of India)", "url": "https://cdsco.gov.in"},
            {"name": "National Health Portal of India", "url": "https://www.nhp.gov.in"},
        ],
    },

    "sore_throat": {
        "condition": "sore_throat",
        "displayName": "Sore Throat",
        "category": "symptom",
        "keywords": [
            "sore throat", "throat hurts", "throat pain", "scratchy throat", "hurts to swallow",
            "pain when swallowing", "throat irritation", "pain in throat", "raw throat"
        ],
        "questions": [
            {
                "id": "age",
                "question": "How old are you?",
                "first_turn_prefix": "I'm sorry your throat is hurting. I can help evaluate your symptoms.\n\n**First, how old are you?**",
                "required": True,
                "extraction_key": "age",
            },
            {
                "id": "duration_and_swallowing",
                "question": "How long has your throat been sore, and is it painful when you swallow?",
                "required": True,
                "extraction_key": "duration",
            },
            {
                "id": "associated_symptoms",
                "question": "Do you have any fever, cough, runny nose, or swollen tender glands in your neck?",
                "required": True,
                "extraction_key": "associated_symptoms",
            },
            {
                "id": "airway_check",
                "question": "Are you having any difficulty breathing, inability to swallow your own saliva (drooling), or a stiff neck?",
                "required": True,
                "extraction_key": "red_flag_check",
            },
        ],
        "red_flags": [
            "Inability to swallow liquids or saliva (drooling)",
            "Difficulty breathing or stridor (whistling airway sound)",
            "Severe inability to open your mouth (trismus / peritonsillar abscess)",
            "High fever accompanied by severe neck swelling",
        ],
        "possible_causes": [
            "Viral pharyngitis (associated with common cold, adenovirus, or flu)",
            "Streptococcal pharyngitis (bacterial 'strep throat' requiring antibiotics)",
            "Post-nasal drip irritation or sleeping with an open mouth in dry air",
            "Acid reflux laryngitis (GERD)",
        ],
        "general_advice": [
            "Gargle with warm salt water (1/2 teaspoon of salt in a glass of warm water) 3-4 times daily.",
            "Drink warm soothing fluids like warm water, chamomile tea, or warm broth with honey (adults).",
            "Suck on soothing throat lozenges or hard candies to stimulate saliva.",
            "Use a cool-mist humidifier in your room to prevent airway dryness.",
        ],
        "medication_info": {
            "name": "Acetaminophen / Paracetamol & Antiseptic Lozenges",
            "general_use": "Provides temporary symptomatic pain relief for throat discomfort and fever.",
            "warnings": "Antibiotics should only be prescribed if a healthcare professional confirms bacterial pharyngitis (e.g. Centor criteria or throat swab). They do not treat viral throat infections.",
            "contraindications": "Refer to paracetamol precautions.",
            "adverse_effects": "Rare mild stomach upset.",
            "interactions": "Standard analgesic interaction profiles.",
        },
        "when_to_see_doctor": [
            "Sore throat lasting longer than 5-7 days",
            "Severe pain when swallowing with high fever and absence of cough (suggests strep)",
            "Any difficulty breathing, drooling, or inability to open your mouth",
            "Visible white patches or pus spots on tonsils",
        ],
        "sources": [
            {"name": "IDSA Guidelines on Pharyngitis", "url": "https://www.idsociety.org"},
            {"name": "CDSCO (Govt of India)", "url": "https://cdsco.gov.in"},
            {"name": "National Health Portal of India", "url": "https://www.nhp.gov.in"},
        ],
    },

    "dizziness": {
        "condition": "dizziness",
        "displayName": "Dizziness / Vertigo",
        "category": "symptom",
        "keywords": [
            "dizzy", "dizziness", "feeling dizzy", "lightheaded", "room spinning",
            "spinning sensation", "vertigo", "giddy", "unsteady", "feeling faint",
            "head spinning", "woozy"
        ],
        "questions": [
            {
                "id": "age",
                "question": "How old are you?",
                "first_turn_prefix": "I'm sorry you're feeling dizzy. Let's gather a few details to understand your symptoms.\n\n**First, how old are you?**",
                "required": True,
                "extraction_key": "age",
            },
            {
                "id": "sensation_character",
                "question": "Does the dizziness feel like lightheadedness/faintness, or does the room feel like it is actively spinning around you (vertigo)?",
                "required": True,
                "extraction_key": "character",
            },
            {
                "id": "duration_and_triggers",
                "question": "Did this start suddenly, and is it triggered by standing up quickly, rolling over in bed, or moving your head?",
                "required": True,
                "extraction_key": "triggers",
            },
            {
                "id": "neurological_and_cardiac_check",
                "question": "Do you have any weakness, numbness, slurred speech, chest pain, palpitations, or fainting episodes?",
                "required": True,
                "extraction_key": "red_flag_check",
            },
        ],
        "red_flags": [
            "Sudden dizziness with neurological signs: slurred speech, facial droop, or arm weakness (stroke warning)",
            "Dizziness accompanied by chest pain, irregular rapid heartbeat, or shortness of breath",
            "Loss of consciousness (syncope) or seizure",
            "Dizziness following head trauma or with severe sudden headache",
        ],
        "possible_causes": [
            "Orthostatic hypotension (temporary blood pressure drop upon standing)",
            "Benign paroxysmal positional vertigo (BPPV) or vestibular neuritis",
            "Dehydration, low blood sugar (hypoglycemia), or missed meals",
            "Inner ear infection, labyrinthitis, or medication side effect",
        ],
        "general_advice": [
            "Sit or lie down immediately when feeling dizzy to prevent accidental falls or injury.",
            "Stand up very slowly from sitting or lying positions, pausing for 30 seconds before walking.",
            "Drink plenty of water throughout the day to support blood volume and hydration.",
            "Avoid sudden head turns and refrain from driving or operating machinery while symptomatic.",
        ],
        "medication_info": {
            "name": "General Clinical Evaluation Guidance",
            "general_use": "Dizziness causes vary widely; vestibular suppressants or blood pressure management require doctor diagnosis.",
            "warnings": "Do NOT take OTC sedatives or anti-vertigo drugs without a medical examination.",
            "contraindications": "Depends on underlying etiology (cardiac vs vestibular).",
            "adverse_effects": "Sedation, dry mouth with vestibular antihistamines.",
            "interactions": "Antihypertensive drugs, CNS depressants.",
        },
        "when_to_see_doctor": [
            "Dizziness that is recurrent, severe, or worsening",
            "Any episode where you lose consciousness or fall",
            "Dizziness accompanied by hearing loss or ringing in ears (tinnitus)",
            "Dizziness starting after beginning a new prescription medication",
        ],
        "sources": [
            {"name": "American Academy of Otolaryngology - Head and Neck Surgery", "url": "https://www.entnet.org"},
            {"name": "CDSCO (Govt of India)", "url": "https://cdsco.gov.in"},
            {"name": "National Health Portal of India", "url": "https://www.nhp.gov.in"},
        ],
    },

    "back_pain": {
        "condition": "back_pain",
        "displayName": "Back Pain",
        "category": "symptom",
        "keywords": [
            "back pain", "back hurts", "pain in back", "lower back pain", "lumbar pain",
            "upper back pain", "backache", "stiff back", "spine pain"
        ],
        "questions": [
            {
                "id": "age",
                "question": "How old are you?",
                "first_turn_prefix": "I'm sorry you're dealing with back pain. I can help evaluate your symptoms.\n\n**First, how old are you?**",
                "required": True,
                "extraction_key": "age",
            },
            {
                "id": "location_and_onset",
                "question": "Where in your back is the pain (upper, middle, or lower), and did it start after any heavy lifting, bending, or physical injury?",
                "required": True,
                "extraction_key": "location",
            },
            {
                "id": "duration_and_character",
                "question": "How long have you had the pain, and is it a dull ache, sharp pain, or muscle stiffness?",
                "required": True,
                "extraction_key": "severity",
            },
            {
                "id": "nerve_and_red_flags",
                "question": "Do you have any numbness, tingling, or weakness radiating down your legs, any changes in bowel or bladder control, or fever?",
                "required": True,
                "extraction_key": "red_flag_check",
            },
        ],
        "red_flags": [
            "Loss of bowel or bladder control or numbness in the groin/saddle area (cauda equina emergency)",
            "Progressive weakness, 'foot drop', or inability to walk on your heels or toes",
            "Back pain accompanied by unexplained fever or history of cancer",
            "Pain following high-impact trauma, car crash, or fall from height",
        ],
        "possible_causes": [
            "Acute lumbar muscle or ligament strain (lifting, awkward posture)",
            "Lumbar disc herniation or sciatic nerve root irritation",
            "Degenerative disc disease or lumbar facet arthropathy",
            "Poor ergonomic seating posture or prolonged sedentary desk work",
        ],
        "general_advice": [
            "Stay gently active; short, gentle walks promote healing faster than strict prolonged bed rest.",
            "Apply an ice pack for the first 48 hours to reduce inflammation, then switch to warm heat packs.",
            "Sleep on your side with a pillow between your knees or on your back with a pillow under your knees.",
            "Use ergonomic lumbar support when sitting and avoid heavy lifting or sudden twisting.",
        ],
        "medication_info": {
            "name": "Acetaminophen / Paracetamol or Topical NSAID Gel",
            "general_use": "Temporary relief of mild to moderate musculoskeletal strain pain.",
            "warnings": "Topical gels (like diclofenac) provide targeted relief with lower systemic gastrointestinal risk. Do not exceed oral dosing limits.",
            "contraindications": "Oral NSAIDs contraindicated in active peptic ulcers or kidney disease.",
            "adverse_effects": "Skin irritation with topicals; GI distress with oral agents.",
            "interactions": "Anticoagulants, ACE inhibitors with oral NSAIDs.",
        },
        "when_to_see_doctor": [
            "Pain radiating past your knee into your foot with numbness or tingling",
            "Back pain that does not improve after 2 to 4 weeks of self-care",
            "Any loss of bladder/bowel control (seek immediate emergency care)",
            "Severe pain disturbing sleep or accompanied by fever",
        ],
        "sources": [
            {"name": "North American Spine Society (NASS)", "url": "https://www.spine.org"},
            {"name": "CDSCO (Govt of India)", "url": "https://cdsco.gov.in"},
            {"name": "National Health Portal of India", "url": "https://www.nhp.gov.in"},
        ],
    },

    "skin_rash": {
        "condition": "skin_rash",
        "displayName": "Skin Rash / Itching",
        "category": "symptom",
        "keywords": [
            "rash", "skin rash", "rash on skin", "itching", "itchy skin", "hives",
            "urticaria", "red bumps", "red spots on skin", "skin allergy", "allergic rash"
        ],
        "questions": [
            {
                "id": "age",
                "question": "How old are you?",
                "first_turn_prefix": "I'm sorry you're having skin trouble. Let's look at your symptoms.\n\n**First, how old are you?**",
                "required": True,
                "extraction_key": "age",
            },
            {
                "id": "location_and_duration",
                "question": "Where on your body did the rash appear, how long has it been there, and is it spreading or itching?",
                "required": True,
                "extraction_key": "location",
            },
            {
                "id": "triggers",
                "question": "Did you recently start any new medication, food, cosmetic, laundry detergent, or have outdoor/insect exposure?",
                "required": True,
                "extraction_key": "triggers",
            },
            {
                "id": "anaphylaxis_check",
                "question": "Are you experiencing any swelling of your face, lips, tongue, or throat, difficulty breathing, or high fever?",
                "required": True,
                "extraction_key": "red_flag_check",
            },
        ],
        "red_flags": [
            "Swelling of the lips, tongue, throat, or difficulty breathing (anaphylactic emergency)",
            "Rash spreading extremely rapidly across large areas of the body with blistering or skin peeling",
            "Dark purple, non-blanching spots (petechiae or purpura that do not fade when pressed with a clear glass)",
            "Rash accompanied by high fever, confusion, or severe illness",
        ],
        "possible_causes": [
            "Contact dermatitis (reaction to soap, plant, jewelry, or chemical)",
            "Acute urticaria (hives from viral infection, food, or medication)",
            "Eczema / atopic dermatitis flare",
            "Viral exanthem (common viral rash) or insect bite reaction",
        ],
        "general_advice": [
            "Apply cool, damp compresses to the itchy areas to reduce heat and irritation.",
            "Avoid scratching, which can damage the skin barrier and cause secondary bacterial infection; keep nails trimmed.",
            "Take lukewarm showers and use mild, fragrance-free cleansers and moisturizers (like plain calamine or ceramide creams).",
            "Wear loose, soft cotton clothing and avoid synthetic fabrics.",
        ],
        "medication_info": {
            "name": "Calamine Lotion & Non-sedating Antihistamine (Cetirizine)",
            "general_use": "Topical calamine soothes itching; oral antihistamines reduce allergic histamine response.",
            "warnings": "If a rash started after taking a newly prescribed medication, notify your prescribing doctor immediately before taking another dose.",
            "contraindications": "Severe renal impairment for certain antihistamines; open broken skin for topical irritants.",
            "adverse_effects": "Mild drowsiness or dry mouth with some antihistamines.",
            "interactions": "Sedatives, alcohol with antihistamines.",
        },
        "when_to_see_doctor": [
            "Rash accompanied by facial/throat swelling or breathing trouble (emergency)",
            "Rash with blisters, skin peeling, or involvement of eyes, mouth, or genitals",
            "Rash showing signs of infection (increasing redness, warmth, pus, or streaks)",
            "Rash not improving after 1 week of gentle self-care",
        ],
        "sources": [
            {"name": "American Academy of Dermatology (AAD)", "url": "https://www.aad.org"},
            {"name": "CDSCO (Govt of India)", "url": "https://cdsco.gov.in"},
            {"name": "National Health Portal of India", "url": "https://www.nhp.gov.in"},
        ],
    },

    "fatigue": {
        "condition": "fatigue",
        "displayName": "Fatigue and Weakness",
        "category": "symptom",
        "keywords": [
            "fatigue", "tired", "tiredness", "exhausted", "exhaustion", "weakness",
            "feeling weak", "lack of energy", "body weakness", "no energy", "drained"
        ],
        "questions": [
            {
                "id": "age",
                "question": "How old are you?",
                "first_turn_prefix": "I'm sorry you're feeling so fatigued. I can help evaluate your symptoms.\n\n**First, how old are you?**",
                "required": True,
                "extraction_key": "age",
            },
            {
                "id": "duration_and_onset",
                "question": "How long have you been feeling this fatigue, and did it start after a specific illness, stress, or lifestyle change?",
                "required": True,
                "extraction_key": "duration",
            },
            {
                "id": "sleep_and_lifestyle",
                "question": "How many hours of sleep do you get nightly, and do you feel refreshed in the morning or wake up tired?",
                "required": True,
                "extraction_key": "lifestyle",
            },
            {
                "id": "associated_symptoms",
                "question": "Do you have any other symptoms like fever, shortness of breath, unexplained weight changes, dizziness, or pale skin?",
                "required": True,
                "extraction_key": "associated_symptoms",
            },
        ],
        "red_flags": [
            "Sudden profound muscle weakness or inability to move a limb (stroke warning)",
            "Fatigue accompanied by shortness of breath on minimal exertion or chest pain",
            "Black tarry stools, heavy bleeding, or severe pallor (anemia / internal bleeding)",
            "Fever with persistent weight loss and night sweats",
        ],
        "possible_causes": [
            "Sleep deprivation, poor sleep hygiene, or sleep apnea",
            "Post-viral fatigue (recovering from flu, COVID-19, or dengue)",
            "Iron deficiency anemia or vitamin D / B12 deficiency",
            "Hypothyroidism, chronic stress, or metabolic imbalance",
        ],
        "general_advice": [
            "Maintain a consistent sleep schedule aiming for 7-9 hours of restful sleep in a dark, quiet room.",
            "Stay hydrated and eat balanced meals rich in iron, protein, and complex carbohydrates.",
            "Engage in light physical activity like 20-minute daily walks to boost circulation.",
            "Limit excessive caffeine, energy drinks, and late-night digital screen usage.",
        ],
        "medication_info": {
            "name": "General Health & Nutritional Evaluation",
            "general_use": "Supplements (like iron or vitamin D) should ideally be guided by blood lab tests (e.g. CBC, ferritin).",
            "warnings": "Taking high-dose iron without confirmed deficiency can cause toxicity and GI distress.",
            "contraindications": "Hemochromatosis for iron supplements.",
            "adverse_effects": "Constipation, dark stool with oral iron.",
            "interactions": "Calcium supplements decrease iron absorption.",
        },
        "when_to_see_doctor": [
            "Fatigue persisting for more than 2-4 weeks despite adequate rest",
            "Accompanied by unexplained weight loss, fever, or swollen lymph nodes",
            "Accompanied by shortness of breath or dizziness",
            "Consider a routine blood checkup (CBC, thyroid panel, vitamin levels)",
        ],
        "sources": [
            {"name": "WHO Health Topics: Fatigue & Anemia", "url": "https://www.who.int"},
            {"name": "CDSCO (Govt of India)", "url": "https://cdsco.gov.in"},
            {"name": "National Health Portal of India", "url": "https://www.nhp.gov.in"},
        ],
    },

    "body_pain": {
        "condition": "body_pain",
        "displayName": "Body Pain / Aches",
        "category": "symptom",
        "keywords": [
            "body pain", "body ache", "body aches", "aching all over", "muscle pain",
            "muscle ache", "joint pain", "pain in joints", "aching body", "chills and body pain"
        ],
        "questions": [
            {
                "id": "age",
                "question": "How old are you?",
                "first_turn_prefix": "I'm sorry you're experiencing body aches. Let's look at your symptoms together.\n\n**First, how old are you?**",
                "required": True,
                "extraction_key": "age",
            },
            {
                "id": "duration_and_onset",
                "question": "How long have you had these body aches, and did they start after intense exercise or alongside a fever?",
                "required": True,
                "extraction_key": "duration",
            },
            {
                "id": "associated_symptoms",
                "question": "Do you have any fever, chills, sore throat, cough, joint swelling, or skin rash?",
                "required": True,
                "extraction_key": "associated_symptoms",
            },
            {
                "id": "severity_and_mobility",
                "question": "Are the aches mild and generalized, or are specific joints swollen, red, hot, or unable to move?",
                "required": True,
                "extraction_key": "severity",
            },
        ],
        "red_flags": [
            "Hot, swollen, red joint with severe pain and high fever (septic arthritis concern)",
            "Extreme muscle weakness, dark tea-colored urine (rhabdomyolysis warning)",
            "High fever with severe headache, neck stiffness, or purple rash",
            "Difficulty breathing or chest pain accompanying body aches",
        ],
        "possible_causes": [
            "Viral prodrome or systemic viral infection (influenza, dengue, COVID-19)",
            "Delayed onset muscle soreness (DOMS) from physical exertion",
            "Tension, stress, or dehydration",
            "Early arthritic or inflammatory joint condition",
        ],
        "general_advice": [
            "Rest your body and drink ample fluids (water, electrolyte solutions, warm soups).",
            "Take a warm bath or apply a heating pad to soothe generalized muscular stiffness.",
            "Perform gentle stretching once the acute pain begins to subside.",
            "Avoid strenuous physical workouts while your body is actively recovering.",
        ],
        "medication_info": {
            "name": "Acetaminophen / Paracetamol",
            "general_use": "Temporary relief of generalized viral myalgias and fever.",
            "warnings": "Do not exceed maximum daily limits (3,000–4,000 mg/day for adults). Avoid combining multiple medicines containing paracetamol.",
            "contraindications": "Severe liver disease.",
            "adverse_effects": "Rare liver toxicity in overdose.",
            "interactions": "Alcohol, warfarin with high chronic doses.",
        },
        "when_to_see_doctor": [
            "Body aches persisting for more than 5-7 days",
            "High fever persisting more than 3 days",
            "Swelling, redness, or heat in one or more specific joints",
            "Dark cola-colored urine following muscle pain",
        ],
        "sources": [
            {"name": "WHO Guidelines on Viral Illnesses", "url": "https://www.who.int"},
            {"name": "CDSCO (Govt of India)", "url": "https://cdsco.gov.in"},
            {"name": "National Health Portal of India", "url": "https://www.nhp.gov.in"},
        ],
    },

    # =========================================================================
    # COMMON CHRONIC & ACUTE CONDITIONS
    # =========================================================================
    "type_2_diabetes": {
        "condition": "type_2_diabetes",
        "displayName": "Type 2 Diabetes",
        "category": "condition",
        "keywords": [
            "diabetes", "diabetic", "type 2 diabetes", "sugar patient", "blood sugar",
            "high sugar", "high blood sugar", "hyperglycemia", "hypoglycemia", "sugar problem",
            "i have diabetes"
        ],
        "questions": [
            {
                "id": "current_symptoms_and_readings",
                "question": "Managing diabetes is very important. To provide relevant clinical guidance, **do you have any current symptoms (such as extreme thirst, frequent urination, shakiness, or dizziness), and do you know your recent blood sugar readings?**",
                "first_turn_prefix": "Managing diabetes is very important. To provide relevant clinical guidance, **do you have any current symptoms (such as extreme thirst, frequent urination, shakiness, or dizziness), and do you know your recent blood sugar readings?**",
                "required": True,
                "extraction_key": "symptoms_and_glucose",
            },
            {
                "id": "age_and_duration",
                "question": "How old are you, and how long have you been diagnosed with diabetes?",
                "required": True,
                "extraction_key": "age",
            },
            {
                "id": "current_medications",
                "question": "Are you currently taking any prescribed diabetes medications (such as metformin) or insulin?",
                "required": True,
                "extraction_key": "medications",
            },
        ],
        "red_flags": [
            "Hypoglycemia warning: blood sugar < 70 mg/dL with confusion, sweating, shakiness, or loss of consciousness",
            "Severely elevated glucose (> 300 mg/dL) with fruity breath odor, persistent vomiting, or rapid breathing (DKA / HHS emergency)",
            "Non-healing foot ulcers, blackening, numbness, or loss of sensation in feet",
            "Sudden vision changes or blurry vision",
        ],
        "possible_causes": [
            "Impaired insulin sensitivity and relative insulin deficiency",
            "Lifestyle factors (diet high in refined carbohydrates, physical inactivity)",
            "Genetic predisposition and family history",
        ],
        "general_advice": [
            "Follow a balanced low-glycemic diet rich in fiber (vegetables, whole grains, lentils) and avoid refined sugars, sweet beverages, and bakery items.",
            "Engage in at least 150 minutes of moderate aerobic activity weekly (such as brisk walking) as cleared by your doctor.",
            "Inspect your feet daily for any cuts, blisters, redness, or calluses, and keep them clean and dry.",
            "Monitor blood glucose levels as recommended by your physician and maintain a log.",
        ],
        "medication_info": {
            "name": "Metformin (General Educational Information)",
            "general_use": "First-line oral biguanide medication that improves insulin sensitivity and decreases hepatic glucose production.",
            "warnings": "Prescription only. Always take with meals to reduce stomach upset. Must be withheld before certain iodinated contrast imaging studies.",
            "contraindications": "Severe renal impairment (eGFR < 30 mL/min), acute metabolic acidosis, severe liver disease.",
            "adverse_effects": "Gastrointestinal upset (diarrhea, nausea, abdominal discomfort), metallic taste, rare lactic acidosis.",
            "interactions": "Alcohol (increases lactic acidosis risk), contrast media.",
        },
        "when_to_see_doctor": [
            "Blood sugar consistently above or below your target range",
            "Any cuts or sores on your feet that do not heal quickly",
            "Regular periodic visits every 3-6 months for HbA1c testing, blood pressure checks, kidney panel, and annual eye exams",
        ],
        "sources": [
            {"name": "American Diabetes Association (ADA) Standards of Care", "url": "https://diabetes.org"},
            {"name": "CDSCO (Govt of India)", "url": "https://cdsco.gov.in"},
            {"name": "National Health Portal of India", "url": "https://www.nhp.gov.in"},
        ],
    },

    "hypertension": {
        "condition": "hypertension",
        "displayName": "Hypertension (High Blood Pressure)",
        "category": "condition",
        "keywords": [
            "hypertension", "high blood pressure", "high bp", "bp high", "blood pressure high",
            "bp problem", "i have high blood pressure", "i have hypertension", "elevated bp"
        ],
        "questions": [
            {
                "id": "symptoms_and_reading",
                "question": "Managing blood pressure is essential for cardiovascular health. **Do you currently have any symptoms like severe headache, chest discomfort, shortness of breath, or vision changes, and do you know your recent blood pressure reading?**",
                "first_turn_prefix": "Managing blood pressure is essential for cardiovascular health. **Do you currently have any symptoms like severe headache, chest discomfort, shortness of breath, or vision changes, and do you know your recent blood pressure reading?**",
                "required": True,
                "extraction_key": "symptoms_and_bp",
            },
            {
                "id": "age_and_duration",
                "question": "How old are you, and how long have you had high blood pressure?",
                "required": True,
                "extraction_key": "age",
            },
            {
                "id": "current_medications",
                "question": "Are you currently taking any prescribed blood pressure medications (like amlodipine or telmisartan)?",
                "required": True,
                "extraction_key": "medications",
            },
        ],
        "red_flags": [
            "Hypertensive crisis: Blood pressure > 180/120 mmHg with severe headache, chest pain, or shortness of breath",
            "Sudden numbness or weakness in face, arm, or leg (stroke warning)",
            "Difficulty speaking, slurred speech, or acute confusion",
            "Sudden blurry vision or loss of vision",
        ],
        "possible_causes": [
            "Primary (essential) hypertension: age, genetic factors, high dietary sodium, sedentary lifestyle, stress",
            "Secondary hypertension: renal artery stenosis, sleep apnea, endocrine disorders",
        ],
        "general_advice": [
            "Adopt the DASH diet (Dietary Approaches to Stop Hypertension): rich in fruits, vegetables, whole grains, and low-fat dairy.",
            "Reduce dietary sodium intake to under 2,000 mg/day (less than 1 teaspoon of table salt daily); avoid processed foods and papads.",
            "Maintain regular moderate physical exercise (brisk walking 30 minutes daily).",
            "Manage stress through deep breathing and maintain a healthy weight.",
        ],
        "medication_info": {
            "name": "Telmisartan / Amlodipine (General Educational Information)",
            "general_use": "Antihypertensive agents (ARBs or Calcium Channel Blockers) that relax blood vessels to lower blood pressure.",
            "warnings": "Prescription only. Never stop blood pressure medicines suddenly without your doctor's direction, as rebound hypertension can occur.",
            "contraindications": "Telmisartan is strictly contraindicated in pregnancy due to fetal toxicity. Amlodipine caution in severe aortic stenosis.",
            "adverse_effects": "Dizziness, peripheral ankle swelling (amlodipine), mild hyperkalemia (telmisartan).",
            "interactions": "Potassium supplements with ARBs; NSAIDs may decrease antihypertensive efficacy.",
        },
        "when_to_see_doctor": [
            "Blood pressure readings consistently exceeding 140/90 mmHg",
            "Any hypertensive reading accompanied by headache or chest pain (urgent)",
            "Routine monitoring every 3 to 6 months for medication adjustment and kidney function review",
        ],
        "sources": [
            {"name": "AHA / ACC Hypertension Clinical Practice Guidelines", "url": "https://www.heart.org"},
            {"name": "Cardiological Society of India (CSI)", "url": "https://csi.org.in"},
            {"name": "CDSCO (Govt of India)", "url": "https://cdsco.gov.in"},
        ],
    },

    "migraine": {
        "condition": "migraine",
        "displayName": "Migraine",
        "category": "condition",
        "keywords": [
            "migraine", "migraine headache", "migraines", "hemi-crania", "throbbing one side head",
            "migraine attack", "aura headache"
        ],
        "questions": [
            {
                "id": "age",
                "question": "How old are you?",
                "first_turn_prefix": "I'm sorry you're dealing with a migraine episode. I can help provide supportive health information.\n\n**First, how old are you?**",
                "required": True,
                "extraction_key": "age",
            },
            {
                "id": "duration_and_side",
                "question": "How long has this episode lasted, and is the throbbing pain concentrated on one side of your head or both?",
                "required": True,
                "extraction_key": "duration",
            },
            {
                "id": "sensory_and_nausea",
                "question": "Are you experiencing sensitivity to light (photophobia), sensitivity to sound, nausea, or visual auras (flashing lights)?",
                "required": True,
                "extraction_key": "associated_symptoms",
            },
            {
                "id": "red_flag_check",
                "question": "Did this pain start with sudden explosive intensity (thunderclap), or do you have any weakness, numbness, or fever?",
                "required": True,
                "extraction_key": "red_flag_check",
            },
        ],
        "red_flags": [
            "Sudden severe 'thunderclap' headache reaching maximum intensity in seconds",
            "Aura symptoms lasting longer than 60 minutes or motor weakness",
            "Migraine accompanied by fever, neck stiffness, or confusion",
            "New onset headache in individuals over 50 years of age",
        ],
        "possible_causes": [
            "Neurovascular inflammation and trigeminovascular activation",
            "Triggers: lack of sleep, emotional stress, skipped meals, hormonal fluctuations, bright lights, weather shifts",
        ],
        "general_advice": [
            "Rest in a completely dark, quiet room with minimal sensory stimulation.",
            "Place a cool ice pack or cloth over your forehead or temples.",
            "Stay hydrated by sipping cool water or electrolyte drinks.",
            "Keep a headache diary to identify and avoid individual personal triggers.",
        ],
        "medication_info": {
            "name": "Acute Analgesics (Paracetamol / NSAIDs / Triptans)",
            "general_use": "Taken early during attack onset to reduce pain and disability.",
            "warnings": "Limit acute migraine medications to no more than 2-3 days per week to avoid rebound medication-overuse headaches. Triptans require doctor prescription.",
            "contraindications": "Triptans contraindicated in ischemic heart disease or uncontrolled hypertension.",
            "adverse_effects": "Chest tightness, dizziness, drowsiness with triptans; stomach upset with NSAIDs.",
            "interactions": "SSRIs, SNRIs (serotonin syndrome caution), ergotamines.",
        },
        "when_to_see_doctor": [
            "Migraines occurring more than 3-4 times per month (may require prophylactic medication)",
            "Attacks that do not respond to over-the-counter measures",
            "Any change in the usual headache pattern or frequency",
        ],
        "sources": [
            {"name": "International Headache Society (IHS)", "url": "https://ihs-headache.org"},
            {"name": "CDSCO (Govt of India)", "url": "https://cdsco.gov.in"},
            {"name": "National Health Portal of India", "url": "https://www.nhp.gov.in"},
        ],
    },

    "gerd": {
        "condition": "gerd",
        "displayName": "GERD / Gastritis",
        "category": "condition",
        "keywords": [
            "gerd", "acid reflux", "heartburn", "acidity", "gastritis", "sour burps",
            "burning in chest", "acid coming up", "hyperacidity", "stomach acid"
        ],
        "questions": [
            {
                "id": "age",
                "question": "How old are you?",
                "first_turn_prefix": "I can help you understand acid reflux and gastritis symptoms.\n\n**First, how old are you?**",
                "required": True,
                "extraction_key": "age",
            },
            {
                "id": "duration_and_timing",
                "question": "How long have you had these symptoms, and do they worsen after eating, when lying down, or at night?",
                "required": True,
                "extraction_key": "duration",
            },
            {
                "id": "associated_symptoms",
                "question": "Do you have sour burps, burning in your throat or chest, difficulty swallowing, or nausea?",
                "required": True,
                "extraction_key": "associated_symptoms",
            },
            {
                "id": "cardiac_red_flag_check",
                "question": "Are you having any chest pain spreading to your arm, neck, or jaw, shortness of breath, or sweating?",
                "required": True,
                "extraction_key": "red_flag_check",
            },
        ],
        "red_flags": [
            "Chest discomfort radiating to arm or jaw (cardiac ischemia must be ruled out)",
            "Difficulty swallowing (dysphagia) or feeling food stuck in esophagus",
            "Vomiting blood or coffee-ground material, or passing black stools",
            "Unexplained weight loss or chronic persistent vomiting",
        ],
        "possible_causes": [
            "Lower esophageal sphincter relaxation and reflux of gastric acid",
            "Gastric mucosal irritation (gastritis, NSAID use, H. pylori infection)",
            "Dietary triggers: oily, spicy foods, caffeine, chocolate, citrus, carbonated drinks",
            "Lying down immediately after eating or smoking",
        ],
        "general_advice": [
            "Eat smaller, more frequent meals instead of heavy dinners.",
            "Avoid lying down for at least 2-3 hours after finishing a meal.",
            "Elevate the head of your bed by 6 inches with bed risers or an incline wedge.",
            "Avoid spicy, acidic, fried, and tomato-based foods, as well as peppermint and coffee.",
        ],
        "medication_info": {
            "name": "Pantoprazole / Antacids",
            "general_use": "Antacids provide rapid temporary neutralization; PPIs (like pantoprazole) reduce acid secretion.",
            "warnings": "Take PPIs 30-60 minutes before breakfast for best efficacy. Long-term use should be under medical supervision.",
            "contraindications": "Hypersensitivity to PPI formulations.",
            "adverse_effects": "Mild headache, diarrhea or constipation.",
            "interactions": "Ketoconazole, iron absorption, clopidogrel depending on agent.",
        },
        "when_to_see_doctor": [
            "Symptoms occurring more than twice a week for several weeks",
            "Difficulty or pain while swallowing food",
            "Symptoms that do not improve with over-the-counter antacids",
            "Any vomiting or blood in stool",
        ],
        "sources": [
            {"name": "World Gastroenterology Organisation (WGO)", "url": "https://www.worldgastroenterology.org"},
            {"name": "CDSCO (Govt of India)", "url": "https://cdsco.gov.in"},
            {"name": "National Health Portal of India", "url": "https://www.nhp.gov.in"},
        ],
    },

    "uti": {
        "condition": "uti",
        "displayName": "Urinary Tract Infection (UTI)",
        "category": "condition",
        "keywords": [
            "uti", "urine infection", "urinary infection", "burning urination", "pain when urinating",
            "frequent urination", "pain peeing", "dysuria", "burning pee"
        ],
        "questions": [
            {
                "id": "age",
                "question": "How old are you?",
                "first_turn_prefix": "I can help you understand urinary tract symptoms.\n\n**First, how old are you?**",
                "required": True,
                "extraction_key": "age",
            },
            {
                "id": "duration_and_symptoms",
                "question": "How long have you had burning or pain during urination, and are you feeling an urgent need to urinate more frequently than usual?",
                "required": True,
                "extraction_key": "duration",
            },
            {
                "id": "urine_character",
                "question": "Have you noticed any visible blood in the urine, cloudiness, or a strong unusual odor?",
                "required": True,
                "extraction_key": "character",
            },
            {
                "id": "upper_tract_red_flags",
                "question": "Do you have any high fever, shivering chills, or pain in your lower back or flanks (kidney area)?",
                "required": True,
                "extraction_key": "red_flag_check",
            },
        ],
        "red_flags": [
            "High fever, shaking chills, and nausea (pyelonephritis / kidney infection)",
            "Severe pain in the flank or mid-back",
            "Visible gross hematuria (significant blood in urine)",
            "Confusion or altered mental status in elderly patients (urosepsis risk)",
        ],
        "possible_causes": [
            "Bacterial cystitis (commonly E. coli ascending the urethra into the bladder)",
            "Urethritis or localized irritation",
            "Dehydration and infrequent urination",
        ],
        "general_advice": [
            "Drink plenty of water (2 to 3 liters daily) to naturally flush bacteria from the urinary tract.",
            "Urinate as soon as you feel the urge; do not hold urine for extended periods.",
            "Wipe from front to back after using the bathroom to avoid transferring bacteria.",
            "Urinate shortly after sexual intercourse.",
        ],
        "medication_info": {
            "name": "Antibiotic Therapy & Urinary Alkalinizers",
            "general_use": "Bacterial UTIs require a doctor-prescribed antibiotic based on urine analysis and culture.",
            "warnings": "Do NOT take leftover antibiotics without a doctor's examination and urine test. Improper antibiotic use breeds resistant bacteria.",
            "contraindications": "Antibiotic specific (e.g. fluoroquinolones in pregnancy or tendon disorders).",
            "adverse_effects": "GI upset, mild nausea with antibiotics.",
            "interactions": "Antacids can decrease absorption of certain antibiotics.",
        },
        "when_to_see_doctor": [
            "Burning urination or frequent urgency requires a physician consultation and urine routine test",
            "Immediate doctor visit if accompanied by fever, chills, flank pain, or blood in urine",
            "Pregnant individuals with any urinary symptoms should consult immediately",
        ],
        "sources": [
            {"name": "Infectious Diseases Society of America (IDSA)", "url": "https://www.idsociety.org"},
            {"name": "CDSCO (Govt of India)", "url": "https://cdsco.gov.in"},
            {"name": "National Health Portal of India", "url": "https://www.nhp.gov.in"},
        ],
    },

    "asthma": {
        "condition": "asthma",
        "displayName": "Asthma / Bronchospasm",
        "category": "condition",
        "keywords": [
            "asthma", "asthmatic", "wheezing", "asthma attack", "inhaler", "bronchospasm",
            "wheeze", "tight chest asthma", "allergic asthma"
        ],
        "questions": [
            {
                "id": "emergency_check",
                "question": "Asthma symptoms require safety assessment. **Are you having severe breathlessness, struggling to speak in sentences, or using your neck muscles to breathe right now?**",
                "first_turn_prefix": "Asthma symptoms require safety assessment. **Are you having severe breathlessness, struggling to speak in sentences, or using your neck muscles to breathe right now?**",
                "required": True,
                "extraction_key": "emergency_check",
            },
            {
                "id": "age",
                "question": "How old are you?",
                "required": True,
                "extraction_key": "age",
            },
            {
                "id": "symptoms_and_triggers",
                "question": "Are you experiencing wheezing, coughing, or chest tightness, and were you exposed to cold air, dust, smoke, or physical exercise?",
                "required": True,
                "extraction_key": "triggers",
            },
            {
                "id": "inhaler_use",
                "question": "Do you have a diagnosed asthma action plan and a prescribed rescue inhaler (such as salbutamol)?",
                "required": True,
                "extraction_key": "medications",
            },
        ],
        "red_flags": [
            "Severe distress: inability to speak more than a few words in a single breath",
            "Lips or fingernails turning blue or gray (cyanosis)",
            "Chest retractions (skin sucking in around ribs or collarbone during breathing)",
            "No relief within 15-20 minutes after using your prescribed rescue inhaler",
        ],
        "possible_causes": [
            "Chronic airway inflammation and bronchial hyperresponsiveness",
            "Triggers: viral infections, aeroallergens (dust mites, pollen, pet dander), smoke, exercise, cold air",
        ],
        "general_advice": [
            "Follow your personalized asthma action plan provided by your doctor.",
            "Sit upright calmly; avoid lying flat which restricts lung expansion.",
            "Move away from any identifiable triggers (smoke, cold drafts, pets, chemical odors).",
            "Use your prescribed fast-acting bronchodilator inhaler with a spacer device if available.",
        ],
        "medication_info": {
            "name": "Salbutamol (Reliever) & Inhaled Corticosteroid (Controller)",
            "general_use": "Salbutamol provides fast rescue bronchodilation; inhaled steroids control underlying airway inflammation.",
            "warnings": "Rinse your mouth with water after using steroid inhalers to prevent oral thrush. Frequent rescue inhaler use indicates poorly controlled asthma needing doctor review.",
            "contraindications": "Caution in cardiac arrhythmias.",
            "adverse_effects": "Mild shakiness, temporary fast pulse with salbutamol.",
            "interactions": "Non-selective beta-blockers can trigger severe bronchospasm.",
        },
        "when_to_see_doctor": [
            "Any severe asthma flare not responding to your rescue inhaler requires immediate emergency care",
            "Using your rescue inhaler more than twice a week indicates poor control needing treatment adjustment",
            "Waking up at night due to coughing or wheezing",
        ],
        "sources": [
            {"name": "Global Initiative for Asthma (GINA)", "url": "https://ginasthma.org"},
            {"name": "CDSCO (Govt of India)", "url": "https://cdsco.gov.in"},
            {"name": "National Health Portal of India", "url": "https://www.nhp.gov.in"},
        ],
    },
}

# Aliases and mappings to support all condition synonyms
CONDITION_ALIASES: Dict[str, str] = {
    # General symptoms
    "fever": "fever",
    "pyrexia": "fever",
    "chills": "fever",
    "headache": "headache",
    "head pain": "headache",
    "cough": "cough",
    "coughing": "cough",
    "stomach pain": "abdominal_pain",
    "abdominal pain": "abdominal_pain",
    "tummy ache": "abdominal_pain",
    "belly pain": "abdominal_pain",
    "chest pain": "chest_discomfort",
    "chest discomfort": "chest_discomfort",
    "chest pressure": "chest_discomfort",
    "shortness of breath": "shortness_of_breath",
    "difficulty breathing": "shortness_of_breath",
    "breathless": "shortness_of_breath",
    "vomiting": "vomiting",
    "nausea": "vomiting",
    "diarrhea": "diarrhea",
    "loose motion": "diarrhea",
    "watery stool": "diarrhea",
    "sore throat": "sore_throat",
    "throat pain": "sore_throat",
    "dizziness": "dizziness",
    "dizzy": "dizziness",
    "vertigo": "dizziness",
    "back pain": "back_pain",
    "backache": "back_pain",
    "skin rash": "skin_rash",
    "rash": "skin_rash",
    "itching": "skin_rash",
    "fatigue": "fatigue",
    "weakness": "fatigue",
    "tiredness": "fatigue",
    "body pain": "body_pain",
    "body ache": "body_pain",
    "joint pain": "body_pain",
    "muscle pain": "body_pain",
    # Conditions
    "diabetes": "type_2_diabetes",
    "type 2 diabetes": "type_2_diabetes",
    "high blood sugar": "type_2_diabetes",
    "hypertension": "hypertension",
    "high blood pressure": "hypertension",
    "high bp": "hypertension",
    "migraine": "migraine",
    "gerd": "gerd",
    "gastritis": "gerd",
    "acid reflux": "gerd",
    "heartburn": "gerd",
    "uti": "uti",
    "urinary tract infection": "uti",
    "urine infection": "uti",
    "asthma": "asthma",
    "wheezing": "asthma",
    "common cold": "cough",
    "cold": "cough",
    "influenza": "fever",
    "flu": "fever",
    "covid-19": "fever",
    "covid": "fever",
    "allergic rhinitis": "skin_rash",
    "eczema": "skin_rash",
    "dermatitis": "skin_rash",
    "bronchitis": "cough",
    "pneumonia": "cough",
    "sinusitis": "headache",
    "gastroenteritis": "diarrhea",
    "anemia": "fatigue",
    "arthritis": "body_pain",
    "conjunctivitis": "skin_rash",
    "constipation": "abdominal_pain",
    "runny nose": "cough",
    "nasal congestion": "cough",
}


def get_condition_by_id(condition_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve condition configuration by identifier"""
    canon_id = CONDITION_ALIASES.get(condition_id.lower().strip(), condition_id.lower().strip())
    return CONDITION_REGISTRY.get(canon_id)


def find_condition_by_text(text: str) -> Optional[Dict[str, Any]]:
    """
    Identifies the best matching clinical condition from user natural language input.
    """
    text_clean = text.lower().strip()

    # Exact alias check
    for phrase, cond_id in CONDITION_ALIASES.items():
        pattern = r"\b" + phrase.replace(" ", r"\s+") + r"\b"
        import re
        if re.search(pattern, text_clean):
            return CONDITION_REGISTRY.get(cond_id)

    # Keywords check
    for cond_id, config in CONDITION_REGISTRY.items():
        for kw in config.get("keywords", []):
            pattern = r"\b" + kw.replace(" ", r"\s+") + r"\b"
            import re
            if re.search(pattern, text_clean):
                return config

    return None


def find_all_conditions_by_text(text: str) -> List[Dict[str, Any]]:
    """
    Detects all mentioned symptoms/conditions to handle multi-symptom clusters.
    """
    text_clean = text.lower().strip()
    matched_ids = set()
    results = []

    for phrase, cond_id in CONDITION_ALIASES.items():
        pattern = r"\b" + phrase.replace(" ", r"\s+") + r"\b"
        import re
        if re.search(pattern, text_clean):
            if cond_id not in matched_ids and cond_id in CONDITION_REGISTRY:
                matched_ids.add(cond_id)
                results.append(CONDITION_REGISTRY[cond_id])

    for cond_id, config in CONDITION_REGISTRY.items():
        if cond_id in matched_ids:
            continue
        for kw in config.get("keywords", []):
            pattern = r"\b" + kw.replace(" ", r"\s+") + r"\b"
            import re
            if re.search(pattern, text_clean):
                matched_ids.add(cond_id)
                results.append(config)
                break

    return results


def register_condition(condition_config: Dict[str, Any]) -> None:
    """
    Allows adding or updating conditions dynamically without modifying core engine.
    """
    cond_id = condition_config.get("condition")
    if cond_id:
        CONDITION_REGISTRY[cond_id] = condition_config
        CONDITION_ALIASES[cond_id] = cond_id
        for kw in condition_config.get("keywords", []):
            CONDITION_ALIASES[kw] = cond_id
