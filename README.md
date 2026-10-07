# Velora Care - Hospital Management System with AI Clinical Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django: 5.0+](https://img.shields.io/badge/Django-5.0%2B-green.svg)](https://www.djangoproject.com/)
[![React: 18](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0%2B-blue.svg)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-5.0%2B-646CFF.svg)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4%2B-38B2AC.svg)](https://tailwindcss.com/)

**Velora Care** is an enterprise-grade, full-stack Hospital Management System (HMS) integrated with a safety-first **AI Clinical & Medication Assistant**. The platform unites patient portals, doctor consultation consoles, ward and bed management, automated billing, diagnostic laboratories, and hospital administration into a high-performance, secure digital healthcare ecosystem.

---

## 📑 Table of Contents

- [Architectural Overview](#-architectural-overview)
- [System Architecture Diagram](#-system-architecture-diagram)
- [Entity Relationship Diagram (ERD)](#-entity-relationship-diagram-erd)
- [AI Clinical Assistant Architecture & Triage Flow](#-ai-clinical-assistant-architecture--triage-flow)
- [Authentication & Role-Based Access Control (RBAC)](#-authentication--role-based-access-control-rbac)
- [Appointment Scheduling & Concurrency Safeguards](#-appointment-scheduling--concurrency-safeguards)
- [Inpatient Bed Management Workflow](#-inpatient-bed-management-workflow)
- [Billing & Financial Settlement Flow](#-billing--financial-settlement-flow)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Directory Structure](#-directory-structure)
- [Installation & Quickstart Guide](#-installation--quickstart-guide)
- [Environment Configuration](#-environment-configuration)
- [API Reference](#-api-reference)
- [Pre-Configured Demo Accounts](#-pre-configured-demo-accounts)
- [Authors & Contact](#-authors--contact)

---

## 🏛️ Architectural Overview

Velora Care is built on a decoupled, service-oriented web architecture:
- **Client Tier**: A single-page application (SPA) created with React 18, TypeScript, Tailwind CSS, Shadcn UI primitives, and Three.js for interactive 3D clinical avatar animations.
- **Application & API Gateway Tier**: Django REST Framework (DRF) handling JSON APIs, stateless JWT tokens, role-based permission verification, field-level encryption, audit trails, and rate throttling.
- **Clinical Intelligence Engine**: A hybrid clinical conversation system combining deterministic red-flag emergency screening, condition-specific multi-turn triage registries, allergy conflict checking, and grounded Retrieval-Augmented Generation (RAG) powered by Gemini and verified regulatory drug monographs (CDSCO & DailyMed).
- **Persistence Tier**: Relational PostgreSQL database for transactional ACID guarantees and Cloudinary cloud storage for medical records and media.

---

## 📊 System Architecture Diagram

```mermaid
flowchart TB
    subgraph ClientLayer["Frontend Client Layer (React 18 + TypeScript + Vite)"]
        UI_Home["Landing & Public Portal"]
        UI_Auth["Auth & Google OAuth"]
        UI_Admin["Admin Operations Console"]
        UI_Doctor["Doctor Consultation Station"]
        UI_Patient["Patient Health Portal"]
        UI_Staff["Ward & Billing Desk"]
        UI_AI["3D Interactive AI Assistant"]
    end

    subgraph GatewayLayer["API Gateway & Security Layer (Django REST Framework)"]
        AUTH_MW["JWT Authentication & Permissions"]
        THROTTLE_MW["Rate Throttling & DDoS Defense"]
        CORS_MW["CORS & CSRF Middleware"]
        AUDIT_MW["Clinical Audit & Action Logging"]
    end

    subgraph ServiceLayer["Core Backend Modules (Django Applications)"]
        SVC_Users["Accounts & User Management"]
        SVC_Patients["Patient Records & Encrypted EMR"]
        SVC_Doctors["Doctor Profiles & Schedules"]
        SVC_Appts["Atomic Appointment Scheduler"]
        SVC_Beds["Beds & Ward Allocations"]
        SVC_Lab["Laboratory & Diagnostic Tests"]
        SVC_Bill["Billing, Invoicing & Payments"]
        SVC_Notify["Real-time Support & Notifications"]
    end

    subgraph AIEngineLayer["AI Clinical Assistant Engine"]
        CLIN_Triage["Universal Condition Registry (13+ Pillars)"]
        CLIN_Safety["Red-Flag Emergency Detector (108/112)"]
        CLIN_Allergy["Patient Allergy Conflict Checker"]
        CLIN_Guard["Anti-Prescription Guardrail"]
        RAG_Search["Vector/Keyword Monograph Search"]
        LLM_Provider["Gemini 1.5/2.5 / Deterministic Offline Engine"]
    end

    subgraph StorageLayer["Data & Persistence Layer"]
        DB_Postgres[("PostgreSQL Database")]
        STORE_Cloud["Cloudinary Media Storage"]
        KNOW_Base[("CDSCO & DailyMed Drug Monographs")]
    end

    ClientLayer --> GatewayLayer
    GatewayLayer --> ServiceLayer
    ServiceLayer --> StorageLayer
    SVC_Patients -.-> AIEngineLayer
    AIEngineLayer --> KNOW_Base
    AIEngineLayer --> LLM_Provider
```

---

## 🗄️ Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    CUSTOM_USER ||--o| PATIENT_PROFILE : "has profile"
    CUSTOM_USER ||--o| DOCTOR_PROFILE : "has profile"
    CUSTOM_USER ||--o{ NOTIFICATION : "receives"
    CUSTOM_USER ||--o{ AUDIT_LOG : "triggers"

    PATIENT_PROFILE ||--o{ APPOINTMENT : "books"
    PATIENT_PROFILE ||--o{ BED_ASSIGNMENT : "occupies"
    PATIENT_PROFILE ||--o{ INVOICE : "billed to"
    PATIENT_PROFILE ||--o{ LAB_TEST_ORDER : "undergoes"
    PATIENT_PROFILE ||--o{ MEDICAL_RECORD : "owns"
    PATIENT_PROFILE ||--o{ CHAT_SESSION : "holds consultations"

    DOCTOR_PROFILE ||--o{ APPOINTMENT : "attends"
    DOCTOR_PROFILE ||--o{ MEDICAL_RECORD : "creates"
    DOCTOR_PROFILE ||--o{ LAB_TEST_ORDER : "orders"

    WARD ||--o{ BED : "contains"
    BED ||--o{ BED_ASSIGNMENT : "allocated in"

    INVOICE ||--o{ INVOICE_ITEM : "itemizes"
    INVOICE ||--o{ PAYMENT_RECORD : "settled with"

    CHAT_SESSION ||--o{ CHAT_MESSAGE : "contains"
    CHAT_MESSAGE ||--o{ CITATION_SOURCE : "references"

    CUSTOM_USER {
        int id PK
        string email UK
        string username UK
        string role "admin | doctor | patient | staff"
        string first_name
        string last_name
        string phone_number
        boolean is_active
        datetime created_at
    }

    PATIENT_PROFILE {
        int id PK
        int user_id FK
        date date_of_birth
        string gender
        string blood_group
        text encrypted_allergies
        text encrypted_medical_history
        string emergency_contact
        string address
    }

    DOCTOR_PROFILE {
        int id PK
        int user_id FK
        string specialization
        string license_number UK
        int consultation_fee
        string qualification
        int experience_years
        string available_days
        time shift_start
        time shift_end
    }

    APPOINTMENT {
        int id PK
        int patient_id FK
        int doctor_id FK
        date appointment_date
        time appointment_time
        string status "pending | confirmed | completed | cancelled"
        text reason_for_visit
        datetime created_at
    }

    WARD {
        int id PK
        string name
        string ward_type "general | icu | private | semi_private"
        int total_beds
    }

    BED {
        int id PK
        int ward_id FK
        string bed_number UK
        string status "available | occupied | maintenance"
        decimal daily_rate
    }

    INVOICE {
        int id PK
        int patient_id FK
        string invoice_number UK
        decimal total_amount
        decimal paid_amount
        string payment_status "unpaid | partial | paid"
        datetime due_date
    }

    CHAT_SESSION {
        int id PK
        int user_id FK
        string session_title
        string primary_condition
        jsonb clinical_context
        datetime created_at
    }
```

---

## 🤖 AI Clinical Assistant Architecture & Triage Flow

The AI Clinical Assistant is designed with a **safety-first**, **one-question-at-a-time** clinical protocol. It prevents diagnosis claims, detects emergencies immediately, verifies registered patient allergies, and delivers evidence-based guidance.

```mermaid
sequenceDiagram
    autonumber
    actor Patient as Patient / User
    participant Frontend as Chat UI & 3D Avatar
    participant View as Assistant View (DRF)
    participant Emergency as Emergency Detector
    participant Triage as Clinical Triage Engine
    participant Registry as Condition Registry
    participant RAG as Knowledge Base (CDSCO/DailyMed)
    participant LLM as Gemini AI / Safe Engine

    Patient->>Frontend: Types symptom (e.g., "I have high fever")
    Frontend->>Frontend: Sets Avatar State: "listening" -> "processing"
    Frontend->>View: POST /api/ai-assistant/chat/ (message, session_id)
    
    critical Deterministic Safety Gate
        View->>Emergency: Scan message against acute red-flag lexicon
        alt Acute Emergency Detected (Chest pain, Stroke, Hemorrhage)
            Emergency-->>View: Flag Critical (Severity 5)
            View-->>Frontend: Urgent 108/112 Alert + Stop Consultation
            Frontend->>Patient: Display Red Emergency Banner
        end
    end

    View->>Triage: Process message with session clinical_context
    Triage->>Registry: Lookup condition ("fever") & check gathered slots
    
    alt Missing Essential Clinical Data (Age, Duration, Temp)
        Registry-->>Triage: Return NEXT single question
        Triage-->>View: Response: Single inquiry + adaptive guidance
    else Sufficient Clinical Context Gathered
        Triage->>RAG: Search verified drug monographs & care guidelines
        RAG-->>Triage: Grounding documents (paracetamol monograph, caveats)
        Triage->>Triage: Verify Patient Registered Allergies
        Triage->>LLM: Synthesize clinical educational summary
        LLM-->>Triage: Safe, non-prescriptive, structured advice
        Triage-->>View: Formatted response with sources & disclaimer
    end

    View-->>Frontend: Return JSON payload (text, sources, context, metadata)
    Frontend->>Frontend: Update Avatar State: "speaking" (speech synthesis)
    Frontend->>Patient: Render Markdown, Sources & Action Cards
```

### 13 Clinical Conversation Pillars
The universal condition registry covers common outpatient presentations with tailored triage question paths:
1. **Fever & Pyrexia**: Age, duration, peak temperature, chills, rash check.
2. **Headache & Migraine**: Location, severity (1-10), visual auras, neck stiffness (meningitis screen).
3. **Cough & Cold**: Productive vs dry, duration, hemoptysis check, wheezing.
4. **Sore Throat & Pharyngitis**: Tonsil swelling, fever, difficulty swallowing.
5. **Abdominal Discomfort**: Upper/lower quadrant, nausea, meal relation, acute surgical abdomen check.
6. **Diarrhea & Gastrointestinal**: Frequency, hydration status, blood in stool screen.
7. **Chest Congestion & Dyspnea**: Exertion relation, oxygenation check, asthma history.
8. **Skin Rash & Dermatitis**: Spreading rate, itching, blister check, anaphylaxis screening.
9. **Joint & Musculoskeletal Pain**: Joint swelling, injury context, morning stiffness.
10. **Back Pain & Lumbago**: Radiation to legs, numbness, bowel/bladder dysfunction screen.
11. **Fatigue & Weakness**: Onset, sleep patterns, unexplained weight loss check.
12. **Allergies & Rhinitis**: Triggers, facial swelling, breathing impact check.
13. **Hypertension & Blood Pressure Inquiries**: Systolic/diastolic readings, headache, vision changes.

---

## 🔐 Authentication & Role-Based Access Control (RBAC)

The authentication subsystem enforces strict separation of privileges across **Admin**, **Doctor**, **Patient**, and **Staff** accounts:

```mermaid
flowchart TD
    Start(["User Request"]) --> Auth{"Authenticated?"}
    
    Auth -- No --> CheckPublic{"Public Route?"}
    CheckPublic -- Yes --> AllowPublic["Render Public Page (Home, About, Doctors)"]
    CheckPublic -- No --> Login["Redirect to Login (/login)"]
    
    Auth -- Yes --> ExtractRole["Extract Role from JWT Payload"]
    
    ExtractRole --> RoleBranch{"Role Category"}
    
    RoleBranch -- "admin" --> AdminArea["Admin Dashboard (/dashboard)"]
    AdminArea --> AdminCaps["Manage Users, System Settings, Full Analytics, Audit Logs"]
    
    RoleBranch -- "doctor" --> DocArea["Doctor Station (/dashboard)"]
    DocArea --> DocCaps["Manage Appointments, View Assigned Patients, Prescribe Lab Tests"]
    
    RoleBranch -- "patient" --> PatArea["Patient Portal (/dashboard)"]
    PatArea --> PatCaps["Book Appointments, 3D AI Clinical Assistant, Medical History, Bills"]
    
    RoleBranch -- "staff" --> StaffArea["Staff Reception (/dashboard)"]
    StaffArea --> StaffCaps["Bed Allocations, Ward Intake, Cashier Billing, Patient Registration"]
```

---

## 📅 Appointment Scheduling & Concurrency Safeguards

To prevent double-booking of doctor schedules under high concurrency, appointment creation executes within atomic database transactions with row-level locks:

```mermaid
stateDiagram-v2
    [*] --> Requested: Patient selects Doctor, Date & Time Slot
    
    state "Atomic Transaction Check" as TransCheck {
        Requested --> RowLock: Acquire select_for_update on Doctor Schedule
        RowLock --> SlotVerify: Check UniqueConstraint(doctor, date, time)
    }

    SlotVerify --> Conflict: Slot Already Reserved
    Conflict --> Requested: Return 409 Conflict (Choose another slot)

    SlotVerify --> Booked: No Overlap Detected
    Booked --> Confirmed: Saved in Database & Alert Sent
    
    Confirmed --> Rescheduled: Patient/Doctor requests time change
    Rescheduled --> Confirmed: New Slot Validated
    
    Confirmed --> InConsultation: Patient Check-In on Visit Date
    InConsultation --> Completed: Consultation Finished & Prescription Added
    
    Confirmed --> Cancelled: Cancelled before consultation
    Cancelled --> [*]
    Completed --> [*]
```

---

## 🛏️ Inpatient Bed Management Workflow

```mermaid
flowchart LR
    A["Patient Admitted"] --> B{"Bed Available?"}
    B -- No --> C["Place in Ward Waiting Queue"]
    C --> B
    B -- Yes --> D["Assign Bed (General / ICU / Private)"]
    D --> E["Update Bed Status -> 'occupied'"]
    E --> F["Daily Room Charges Added to Patient Invoice"]
    F --> G["Doctor Signs Discharge Order"]
    G --> H["Clear Patient Account & Mark Status -> 'maintenance'"]
    H --> I["Housekeeping Cleaning Complete -> 'available'"]
    I --> J(["Bed Ready for Next Patient"])
```

---

## 💳 Billing & Financial Settlement Flow

```mermaid
flowchart TD
    Trig["Patient Discharge / Consultation / Lab Order"] --> Agg["Aggregate Invoice Line Items"]
    
    subgraph BillableServices["Billable Services"]
        S1["Doctor Consultation Fees"]
        S2["Daily Bed & Ward Charges"]
        S3["Diagnostic Laboratory Tests"]
        S4["Pharmacy & Consumables"]
    end
    
    BillableServices --> Agg
    Agg --> Gen["Generate Invoice with Unique Number (INV-XXXX)"]
    Gen --> Select["Select Payment Method"]
    
    Select --> M1["Cash / Counter Payment"]
    Select --> M2["Credit / Debit Card"]
    Select --> M3["UPI / QR Code"]
    Select --> M4["Mediclaim / Insurance TPA"]
    
    M1 & M2 & M3 & M4 --> Exec["Execute Transaction & Cap Max Limit Safeguard"]
    Exec --> Validate{"Full or Partial?"}
    
    Validate -- Full Amount Paid --> StatusPaid["Status: 'paid'"]
    Validate -- Remaining Balance --> StatusPartial["Status: 'partial'"]
    
    StatusPaid --> Receipt["Generate Printable Thermal / PDF Receipt"]
    StatusPartial --> FollowUp["Add to Receivables Ledger"]
    Receipt --> Done(["Billing Completed"])
```

---

## 🌟 Key Features

### 1. 🤖 AI Clinical Assistant & Interactive 3D Avatar
- **Interactive 3D Doctor Avatar**: Built with Three.js/Fiber with dynamic facial expressions, idle breathing, speaking animations, and status loading screen.
- **Universal Clinical Registry**: 13 comprehensive symptom pillars with specialized multi-turn questioning sequences.
- **Strict Anti-Prescription Protocols**: Prohibits autonomous drug prescriptions; contextualizes OTC education safely.
- **Allergy Conflict Checking**: Cross-references patient allergy profiles against drugs and active ingredients before output.
- **RAG-Backed Monograph Citations**: Real-time retrieval against CDSCO (Central Drugs Standard Control Organisation, India) and DailyMed (FDA SPL).
- **Theme Customizer**: Built-in visual themes (Clean Slate, Soft Indigo, Calming Mint, Warm Sunlight, Midnight Dark) with zero transparency bleed.

### 2. 👥 User & Role-Based Access Control
- Distinct permission boundaries for **Administrators**, **Doctors**, **Patients**, and **Hospital Staff**.
- Protected API routes verified via JWT bearer tokens with refresh token rotation.
- Field-level Fernet symmetric encryption for sensitive patient medical data.

### 3. 🏥 Inpatient Bed & Ward Management
- Visual floor plan and real-time bed status indicators (Available, Occupied, Cleaning/Maintenance).
- Automated daily bed-charge accrual linked directly to the patient's billing account.

### 4. 🔬 Laboratory & Diagnostics Module
- Catalog of diagnostic tests with normal reference intervals.
- Track test specimen lifecycle: Ordered $\rightarrow$ Sample Collected $\rightarrow$ Processing $\rightarrow$ Result Published.

### 5. 💰 Billing, Invoicing & Cashier Desk
- Automated line-item invoice compilation.
- Multi-channel payment recording (Cash, UPI, Credit Card, Insurance).
- Safe payment entry with maximum threshold safeguards preventing accidental overcharges.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend Framework** | React 18, TypeScript, Vite |
| **Styling & Components**| Tailwind CSS, Shadcn UI, Lucide Icons, Class Variance Authority |
| **3D & Animations** | Three.js, React Three Fiber, React Three Drei, Framer Motion |
| **State & HTTP Client** | React Context API, React Query, Axios |
| **Backend Core** | Python 3.10+, Django 5.0+, Django REST Framework (DRF) |
| **Authentication** | Simple JWT (JSON Web Tokens), Google OAuth2 |
| **AI & LLM Services** | Google Gemini API (Gemini 1.5 / 2.5 Flash), Deterministic Fallback Engine |
| **Database** | PostgreSQL (Production) / SQLite3 (Development) |
| **Media & Static Storage** | Cloudinary Storage, Whitenoise |
| **Cryptography** | Cryptography (Fernet symmetric encryption for health records) |

---

## 📁 Directory Structure

```text
HMS/
├── clinic_backend/                     # Django Backend Project
│   ├── accounts/                       # Custom User model, JWT auth & profile views
│   ├── ai_assistant/                   # AI Clinical Assistant & Medical RAG
│   │   ├── clinical/                   # Universal Condition Registry & Multi-turn Triage
│   │   │   ├── condition_registry.py   # 13 clinical conversation pillar schemas
│   │   │   ├── conversation_engine.py  # Turn-by-turn state machine & question logic
│   │   │   ├── entity_extractor.py     # Medical terminology & vital sign extractor
│   │   │   └── response_formatter.py   # Structured markdown response builder
│   │   ├── llm/                        # Gemini AI provider & fallback engine
│   │   ├── providers/                  # CDSCO & DailyMed monograph scrapers
│   │   ├── retrieval/                  # Hybrid semantic / keyword search
│   │   ├── safety/                     # Emergency detector, allergy checker, prescription guard
│   │   └── management/commands/        # CLI scripts: seed_medications, sync_medications
│   ├── appointments/                   # Concurrency-safe appointment bookings
│   ├── audit/                          # System audit log tracking
│   ├── beds/                           # Hospital wards, bed allocation & occupancy
│   ├── billing/                        # Invoices, invoice items, and payment transactions
│   ├── clinic_backend/                 # Root settings, URLs, WSGI/ASGI configuration
│   ├── doctors/                        # Doctor profiles, specialties, and schedules
│   ├── laboratory/                     # Lab tests, orders, and diagnostic results
│   ├── patients/                       # Patient records, encrypted EMR, and history
│   ├── records/                        # Document uploads and medical certificates
│   ├── support/                        # Notifications, tickets, and user feedback
│   ├── manage.py                       # Django CLI execution tool
│   └── requirements.txt                # Python backend dependencies
│
├── clinic_frontend/                    # React + Vite Frontend Project
│   ├── public/                         # Static assets and favicons
│   ├── src/
│   │   ├── components/
│   │   │   ├── assistant/              # 3D Avatar, ChatWindow, ChatInput, Triage UI
│   │   │   ├── common/                 # Header, Sidebar, Navigation, Modals
│   │   │   ├── dashboard/              # Role-specific dashboard layouts & widgets
│   │   │   └── ui/                     # Shadcn UI primitives (Buttons, Cards, Dialogs)
│   │   ├── context/                    # AuthContext, NotificationContext
│   │   ├── hooks/                      # Custom hooks (useAuth, useToast, useDebounce)
│   │   ├── pages/                      # Application route pages
│   │   ├── services/                   # Axios API service clients
│   │   ├── App.tsx                     # Primary router and route protection
│   │   ├── main.tsx                    # React DOM root entrypoint
│   │   └── index.css                   # Tailwind theme tokens and base styles
│   ├── package.json                    # Frontend dependencies and npm scripts
│   ├── tailwind.config.ts              # Tailwind CSS design system configuration
│   └── vite.config.ts                  # Vite build tool and development proxy
│
├── .gitignore                          # Git ignore specification
└── README.md                           # Comprehensive documentation
```

---

## 🚀 Installation & Quickstart Guide

### Prerequisites
- **Node.js**: v18.0.0 or higher
- **npm**: v9.0.0 or higher (or `bun` / `pnpm`)
- **Python**: v3.10 or higher
- **Git**: Installed and configured

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/ThummarDarshan/HMS_AI.git
cd HMS_AI
```

---

### Step 2: Backend Setup (Django)

1. **Navigate to the backend directory**:
   ```bash
   cd clinic_backend
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your database URL, secret keys, and Gemini API Key
   ```

5. **Apply Database Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Seed Medical Monographs into the AI Knowledge Base**:
   ```bash
   python manage.py seed_medications
   ```

7. **Start the Django Development Server**:
   ```bash
   python manage.py runserver 127.0.0.1:8000
   ```
   *The backend REST API will be accessible at `http://127.0.0.1:8000/api/`.*

---

### Step 3: Frontend Setup (React + Vite)

1. **Open a new terminal and navigate to the frontend directory**:
   ```bash
   cd clinic_frontend
   ```

2. **Install frontend packages**:
   ```bash
   npm install
   ```

3. **Create the environment file**:
   ```bash
   # Create .env in clinic_frontend directory
   echo "VITE_API_URL=http://127.0.0.1:8000/api" > .env
   ```

4. **Start the Vite development server**:
   ```bash
   npm run dev
   ```
   *The client application will start at `http://localhost:8080/` (or `http://localhost:5173/`).*

---

## ⚙️ Environment Configuration

### Backend (`clinic_backend/.env`)

| Variable | Description | Example / Default |
| :--- | :--- | :--- |
| `DEBUG` | Enable debug mode | `True` |
| `SECRET_KEY` | Django cryptographic secret | `django-insecure-your-secret-key` |
| `JWT_SIGNING_KEY` | Dedicated signing key for JWT tokens | `your-jwt-signing-key` |
| `ENCRYPTION_KEY` | Fernet key for field-level EMR encryption | `generate-via-cryptography-fernet` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/hms_db` |
| `LLM_PROVIDER` | AI provider (`gemini` or `auto`) | `gemini` |
| `GEMINI_API_KEY` | Google Gemini API key | `AIzaSy...` |
| `GEMINI_MODEL` | Gemini LLM model name | `gemini-1.5-flash` |
| `ALLOWED_HOSTS` | Allowed HTTP Host headers | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | Permitted frontend origins | `http://localhost:8080,http://127.0.0.1:8080` |

### Frontend (`clinic_frontend/.env`)

| Variable | Description | Example / Default |
| :--- | :--- | :--- |
| `VITE_API_URL` | Backend REST API base endpoint | `http://127.0.0.1:8000/api` |
| `VITE_GOOGLE_CLIENT_ID` | Optional Google Sign-In OAuth ID | `your-google-oauth-client-id` |

---

## 📡 API Reference

| Endpoint | Method | Role | Description |
| :--- | :--- | :--- | :--- |
| `/api/accounts/users/register/` | `POST` | Public | Create new patient or staff account |
| `/api/accounts/users/login/` | `POST` | Public | Authenticate user & return JWT tokens |
| `/api/accounts/users/token/refresh/` | `POST` | Public | Refresh expired access token |
| `/api/accounts/users/profile/` | `GET/PUT` | Auth | Fetch / update logged-in user details |
| `/api/doctors/doctors/` | `GET` | Public/Auth | List all doctors, specialties, and schedules |
| `/api/patients/` | `GET/POST` | Auth | List / create patient medical records |
| `/api/appointments/` | `GET/POST` | Auth | View / schedule doctor consultations |
| `/api/beds/beds/` | `GET/POST` | Staff/Admin | View bed availability and allocate beds |
| `/api/billing/` | `GET/POST` | Staff/Admin | Retrieve invoices and post payments |
| `/api/laboratory/orders/` | `GET/POST` | Doctor/Staff | Manage diagnostic lab orders |
| `/api/ai-assistant/sessions/` | `GET/POST` | Patient | List past AI conversations or initiate a new one |
| `/api/ai-assistant/chat/` | `POST` | Patient | Send clinical message, trigger triage and RAG |
| `/api/support/notifications/` | `GET` | Auth | Retrieve user notifications and alerts |

---

## 🔑 Pre-Configured Demo Accounts

For demonstration and testing purposes, use the pre-configured accounts below:

| Role | Email Address | Password | Primary Capabilities |
| :--- | :--- | :--- | :--- |
| 🛡️ **Administrator** | `vadsolakishan1310@gmail.com` | `Kishan@12345` | Full system control, analytics, user & role administration |
| 👨‍⚕️ **Doctor** | `darshan@gmail.com` | `123456789` | Appointments, patient diagnosis, prescription & lab orders |
| 👩‍⚕️ **Doctor** | `shreeja@gmail.com` | `shreeja@12345` | Outpatient queue, clinical summaries, consultations |
| 🩺 **Patient** | `harshal@gmail.com` | `harshal@12345` | 3D AI Assistant, booking appointments, viewing invoices |
| 🩺 **Patient** | `aryan@gmail.com` | `aryan@12345` | Symptom triage, medical history, lab test results |

---

## 🧪 Testing & Code Quality

Run tests across the entire codebase to guarantee reliability:

```bash
# 1. Run Backend AI Clinical Assistant and Safety Tests
cd clinic_backend
python manage.py test ai_assistant --keepdb

# 2. Run Django System Check
python manage.py check

# 3. Verify Frontend TypeScript Compilation and Build
cd ../clinic_frontend
npm run build
```

---

## 👥 Authors & Contact

Developed by the **Velora Care Engineering Team**:

- **Kishan Vadsola** — [vadsolakishan1310@gmail.com](mailto:vadsolakishan1310@gmail.com)
- **Darshan Thummar** — [darshantce.059@gmail.com](mailto:darshantce.059@gmail.com)
- **Shreeja Upadhyay** — [shreejaupdhayaycspitce@gmail.com](mailto:shreejaupdhayaycspitce@gmail.com)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — feel free to use and adapt it for healthcare and educational initiatives.
