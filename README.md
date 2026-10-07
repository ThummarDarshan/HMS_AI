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
flowchart TD
    subgraph Frontend["Frontend Layer (React 18, TypeScript, Vite)"]
        UI_Home[Landing Page]
        UI_Auth[Authentication and Google OAuth]
        UI_Admin[Admin Operations Console]
        UI_Doctor[Doctor Consultation Station]
        UI_Patient[Patient Portal and 3D Avatar]
        UI_Staff[Ward and Billing Desk]
    end

    subgraph API_Gateway["API Gateway and Security (Django REST Framework)"]
        MW_Auth[JWT Auth and Role Verification]
        MW_Throttle[Rate Throttling and Security]
        MW_Audit[Audit Logging and Verification]
    end

    subgraph Backend_Services["Core Hospital Modules"]
        SVC_Users[Accounts and User Management]
        SVC_Patients[Patient Records and Encrypted EMR]
        SVC_Doctors[Doctor Profiles and Schedules]
        SVC_Appts[Atomic Appointment Scheduler]
        SVC_Beds[Beds and Ward Allocations]
        SVC_Lab[Laboratory and Diagnostic Tests]
        SVC_Bill[Billing and Invoicing Engine]
    end

    subgraph AI_Engine["AI Clinical Assistant Engine"]
        CLIN_Triage[Universal Condition Registry]
        CLIN_Safety[Emergency Detector and Red Flags]
        CLIN_Allergy[Allergy Conflict Checker]
        CLIN_Guard[Anti-Prescription Guardrail]
        RAG_Search[Monograph Retrieval RAG]
        LLM_Model[Gemini AI and Safe Fallback]
    end

    subgraph Storage["Persistence Layer"]
        DB_Postgres[(PostgreSQL Database)]
        STORE_Cloud[(Cloudinary Media Storage)]
        KNOW_Base[(CDSCO and DailyMed Monographs)]
    end

    UI_Home --> MW_Auth
    UI_Auth --> MW_Auth
    UI_Admin --> MW_Auth
    UI_Doctor --> MW_Auth
    UI_Patient --> MW_Auth
    UI_Staff --> MW_Auth

    MW_Auth --> MW_Throttle
    MW_Throttle --> MW_Audit

    MW_Audit --> SVC_Users
    MW_Audit --> SVC_Patients
    MW_Audit --> SVC_Doctors
    MW_Audit --> SVC_Appts
    MW_Audit --> SVC_Beds
    MW_Audit --> SVC_Lab
    MW_Audit --> SVC_Bill

    UI_Patient --> CLIN_Triage
    CLIN_Triage --> CLIN_Safety
    CLIN_Safety --> CLIN_Allergy
    CLIN_Allergy --> CLIN_Guard
    CLIN_Guard --> RAG_Search
    RAG_Search --> LLM_Model
    RAG_Search --> KNOW_Base

    SVC_Patients --> DB_Postgres
    SVC_Appts --> DB_Postgres
    SVC_Beds --> DB_Postgres
    SVC_Bill --> DB_Postgres
    SVC_Lab --> STORE_Cloud
```

---

## 🗄️ Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    CUSTOM_USER ||--o| PATIENT_PROFILE : has
    CUSTOM_USER ||--o| DOCTOR_PROFILE : has
    CUSTOM_USER ||--o{ NOTIFICATION : receives
    CUSTOM_USER ||--o{ AUDIT_LOG : triggers

    PATIENT_PROFILE ||--o{ APPOINTMENT : books
    PATIENT_PROFILE ||--o{ BED_ASSIGNMENT : occupies
    PATIENT_PROFILE ||--o{ INVOICE : billed_to
    PATIENT_PROFILE ||--o{ LAB_TEST_ORDER : undergoes
    PATIENT_PROFILE ||--o{ CHAT_SESSION : holds

    DOCTOR_PROFILE ||--o{ APPOINTMENT : attends
    DOCTOR_PROFILE ||--o{ LAB_TEST_ORDER : orders

    WARD ||--o{ BED : contains
    BED ||--o{ BED_ASSIGNMENT : allocated_to

    INVOICE ||--o{ INVOICE_ITEM : itemizes
    INVOICE ||--o{ PAYMENT_RECORD : settled_with

    CHAT_SESSION ||--o{ CHAT_MESSAGE : contains

    CUSTOM_USER {
        int id PK
        string email
        string username
        string role
        string first_name
        string last_name
        boolean is_active
    }

    PATIENT_PROFILE {
        int id PK
        int user_id FK
        string date_of_birth
        string gender
        string blood_group
        string emergency_contact
    }

    DOCTOR_PROFILE {
        int id PK
        int user_id FK
        string specialization
        string license_number
        int consultation_fee
        int experience_years
    }

    APPOINTMENT {
        int id PK
        int patient_id FK
        int doctor_id FK
        string appointment_date
        string appointment_time
        string status
    }

    WARD {
        int id PK
        string name
        string ward_type
        int total_beds
    }

    BED {
        int id PK
        int ward_id FK
        string bed_number
        string status
        decimal daily_rate
    }

    INVOICE {
        int id PK
        int patient_id FK
        string invoice_number
        decimal total_amount
        decimal paid_amount
        string payment_status
    }

    CHAT_SESSION {
        int id PK
        int user_id FK
        string session_title
        string primary_condition
        string created_at
    }
```

---

## 🤖 AI Clinical Assistant Architecture & Triage Flow

The AI Clinical Assistant is designed with a **safety-first**, **one-question-at-a-time** clinical protocol. It prevents diagnosis claims, detects emergencies immediately, verifies registered patient allergies, and delivers evidence-based guidance.

```mermaid
sequenceDiagram
    autonumber
    actor User as Patient User
    participant UI as Chat UI and 3D Avatar
    participant API as Assistant API View
    participant Safety as Emergency Detector
    participant Engine as Clinical Triage Engine
    participant Registry as Condition Registry
    participant RAG as Knowledge Base RAG
    participant LLM as Gemini AI Model

    User->>UI: Reports symptom (e.g. Fever)
    UI->>UI: Avatar state changes to Listening
    UI->>API: POST /api/ai-assistant/chat/
    
    API->>Safety: Check for emergency red flags
    alt Acute Red Flag Emergency Detected
        Safety-->>API: Critical Emergency (Call 108 or 112)
        API-->>UI: Emergency Alert Response
        UI->>User: Display Emergency Banner and Hotline
    else Safe Clinical Presentation
        API->>Engine: Process with conversation history
        Engine->>Registry: Check required clinical slots
        alt Missing Clinical Details (Age, Duration, Temperature)
            Registry-->>Engine: Next single question
            Engine-->>API: Return single targeted question
        else Sufficient Information Collected
            Engine->>RAG: Retrieve verified drug monograph
            RAG-->>Engine: Official CDSCO and DailyMed docs
            Engine->>LLM: Synthesize educational response
            LLM-->>Engine: Safe non-prescriptive advice
            Engine-->>API: Formatted response with citations
        end
        API-->>UI: Return JSON response
        UI->>UI: Avatar state changes to Speaking
        UI->>User: Render markdown answer and sources
    end
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
    Start([User Request]) --> Auth{Authenticated?}
    
    Auth -->|No| CheckPublic{Public Route?}
    CheckPublic -->|Yes| AllowPublic[Render Public Home and Doctors Page]
    CheckPublic -->|No| Login[Redirect to Login Page]
    
    Auth -->|Yes| ExtractRole[Extract Role from JWT Payload]
    ExtractRole --> RoleBranch{User Role}
    
    RoleBranch -->|Admin| AdminArea[Admin Dashboard]
    AdminArea --> AdminCaps[User Management, Analytics, Audit Logs]
    
    RoleBranch -->|Doctor| DocArea[Doctor Station]
    DocArea --> DocCaps[Manage Appointments, Patient EMR, Lab Orders]
    
    RoleBranch -->|Patient| PatArea[Patient Portal]
    PatArea --> PatCaps[3D AI Assistant, Book Appointments, View Bills]
    
    RoleBranch -->|Staff| StaffArea[Staff Desk]
    StaffArea --> StaffCaps[Bed Allocation, Billing Cashier, Admissions]
```

---

## 📅 Appointment Scheduling & Concurrency Safeguards

To prevent double-booking of doctor schedules under high concurrency, appointment creation executes within atomic database transactions with row-level locks:

```mermaid
stateDiagram-v2
    [*] --> SlotSelection
    SlotSelection --> ConcurrencyCheck : Submit Selected Slot
    ConcurrencyCheck --> SlotConflict : Overlapping Reservation
    SlotConflict --> SlotSelection : Choose New Slot
    ConcurrencyCheck --> Confirmed : Lock Acquired and Slot Verified
    Confirmed --> Rescheduled : Time Change Requested
    Rescheduled --> ConcurrencyCheck : Validate New Slot
    Confirmed --> InConsultation : Patient Check In
    InConsultation --> Completed : Doctor Completes Visit
    Confirmed --> Cancelled : Appointment Cancelled
    Cancelled --> [*]
    Completed --> [*]
```

---

## 🛏️ Inpatient Bed Management Workflow

```mermaid
flowchart LR
    A[Patient Admission] --> B{Bed Available?}
    B -->|No| C[Ward Waiting Queue]
    C --> B
    B -->|Yes| D[Assign Bed: General, ICU, or Private]
    D --> E[Set Status to Occupied]
    E --> F[Accrue Daily Bed Charges to Invoice]
    F --> G[Doctor Signs Discharge Order]
    G --> H[Patient Settlement and Maintenance Mode]
    H --> I[Housekeeping Cleaning Finished]
    I --> J[Bed Available for Next Patient]
```

---

## 💳 Billing & Financial Settlement Flow

```mermaid
flowchart TD
    StartBilling[Trigger Billing Event] --> Agg[Aggregate Line Items]
    
    subgraph Services[Billable Services]
        S1[Doctor Consultation Fees]
        S2[Daily Ward Bed Charges]
        S3[Diagnostic Laboratory Orders]
        S4[Pharmacy and Consumables]
    end

    S1 --> Agg
    S2 --> Agg
    S3 --> Agg
    S4 --> Agg

    Agg --> Gen[Generate Invoice INV-XXXX]
    Gen --> Select[Select Payment Method]

    Select --> M1[Cash Counter Payment]
    Select --> M2[Debit or Credit Card]
    Select --> M3[UPI QR Code Payment]
    Select --> M4[Insurance TPA Claim]

    M1 --> Process[Validate Payment and Limit Safeguards]
    M2 --> Process
    M3 --> Process
    M4 --> Process

    Process --> Check{Payment Amount}
    Check -->|Full Payment| Paid[Status Paid]
    Check -->|Partial Payment| Partial[Status Partial]

    Paid --> Receipt[Generate Printable Receipt]
    Partial --> Ledger[Update Receivables Balance]
    Receipt --> Complete([Billing Completed])
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
