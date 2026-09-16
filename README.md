# Velora Care - Hospital Management System

Velora Care is a comprehensive, modern, and highly scalable Hospital Management System designed to streamline hospital operations, enhance patient care, and improve overall administrative efficiency. 

It provides an integrated ecosystem featuring a beautiful, user-friendly, and responsive frontend built with React, Vite, and Tailwind CSS, coupled with a robust backend powered by Django and Django REST Framework.

## 🌟 Key Features

*   **AI Health & Medication Assistant**: Grounded RAG-based clinical medication & symptom assistant embedded in the Patient Portal, backed by official CDSCO (Govt of India) and DailyMed (FDA) regulatory monographs. Features emergency red flag detection, allergy conflict alerts, strict anti-prescription guardrails, and verified source citations.
*   **User & Role Management**: Secure authentication system with role-based access control (Admin, Doctor, Patient, Staff).
*   **Patient Management**: Complete digital tracking of patient records, history, and admission details.
*   **Appointment Scheduling**: Seamless booking, rescheduling, and management of patient-doctor appointments.
*   **Doctor Profiles**: Management of doctors' schedules, specialties, and availability.
*   **Bed Management**: Real-time tracking of ward and bed availability, allocation, and discharge.
*   **Laboratory & Diagnostics**: Integration of lab test orders, tracking, and secure result publishing.
*   **Billing & Invoicing**: Automated invoice generation, payment tracking, and financial reporting.
*   **Analytics Dashboard**: Interactive charts and data visualizations for administrative insights.
*   **Responsive Modern UI**: Built with Shadcn UI, Framer Motion for animations, and dark mode support.
*   **Secure & Scalable Backend**: RESTful API design ensuring data integrity and fast processing.

## 🛠️ Technology Stack

### Frontend
*   **Framework**: React 18, Vite
*   **Language**: TypeScript
*   **Styling**: Tailwind CSS, Shadcn UI
*   **Animations**: Framer Motion
*   **State Management/Data Fetching**: React Query, Axios
*   **Charts**: Recharts
*   **Routing**: React Router DOM
*   **Authentication**: Google OAuth integration

### Backend
*   **Framework**: Django, Django REST Framework
*   **Authentication**: Simple JWT (JSON Web Tokens)
*   **Database**: PostgreSQL / MongoDB
*   **Media Storage**: Cloudinary integration
*   **Server**: Gunicorn, Whitenoise (for static file management)

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Node.js (v18 or higher)
*   Python (3.8 or higher)
*   Git

### 1. Clone the Repository

```bash
git clone https://github.com/VadsolaKishan/HMS.git
cd HMS
```

### 2. Backend Setup

```bash
cd clinic_backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # PowerShell (Windows)
# venv\Scripts\activate.bat  # CMD (Windows)
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start the Django development server
python manage.py runserver
```

### 3. Frontend Setup

```bash
cd ../clinic_frontend

# Install dependencies
npm install  # or bun install

# Start the Vite development server
npm run dev  # or bun run dev
```

## 📁 Project Structure

```text
E:\Hospital_Management_System\
├── clinic_backend/             # Django Backend
│   ├── accounts/               # User authentication & roles
│   ├── appointments/           # Appointment booking logic
│   ├── beds/                   # Bed & ward management
│   ├── billing/                # Financial and invoicing modules
│   ├── doctors/                # Doctor schedules & profiles
│   ├── laboratory/             # Lab test tracking
│   ├── patients/               # Patient records management
│   ├── records/                # Medical document management
│   ├── support/                # Helpdesk module
│   ├── manage.py
│   └── requirements.txt
│
└── clinic_frontend/            # React Frontend
    ├── src/
    ├── public/
    ├── package.json
    ├── tailwind.config.ts
    └── vite.config.ts
```

## 🤖 AI Health & Medication Assistant (RAG System)

The system includes a production-grade, medically responsible **AI Health & Medication Assistant** embedded directly in the Patient Dashboard and Sidebar.

### 🛡️ Safety & Clinical Guardrails
1. **Authoritative Sources Only**: Answers are strictly grounded in regulatory medical documentation from **CDSCO** (Central Drugs Standard Control Organisation, India) and **DailyMed** (FDA Structured Product Labeling).
2. **Deterministic Emergency Detector**: Automatically flags acute red-flag symptoms (severe chest pain, breathing distress, stroke symptoms, anaphylaxis, severe hemorrhage, self-harm) and instructs immediate emergency services (108 / 112) while halting medication discussion.
3. **Allergy Conflict Checker**: Cross-checks retrieved drugs and active ingredients against the authenticated patient's registered hospital allergies.
4. **Anti-Prescription Guardrail**: Strictly prohibits autonomous drug prescribing. Recommends physician consultation and links directly to HMS doctor appointment booking.
5. **Prompt Injection & Hallucination Defense**: System prompts and RAG retrieval pipelines treat all user inputs and retrieved documents as data rather than instructions. If a query cannot be verified, it explicitly responds: *"I could not verify this information from the approved medication documentation."*

### 📥 Medication Knowledge Base Ingestion Commands
```bash
cd clinic_backend

# Seed all verified CDSCO & DailyMed monographs
python manage.py seed_medications

# Sync a specific medication from providers
python manage.py sync_medications --drug paracetamol
```

### 🧪 Running Tests
```bash
# Backend AI assistant unit & safety tests
python manage.py test ai_assistant --keepdb

# Frontend build & type checking
cd ../clinic_frontend
npm run build
```

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📧 Contact

Project Link: [https://github.com/VadsolaKishan/HMS.git](https://github.com/VadsolaKishan/HMS.git)


## ALL ID AND PASSWORD
<!-- Admin 
vadsolakishan1310@gmail.com Pass - Kishan@12345

Doctor
darshan@gmail.com Pass - 123456789
shreeja@gmail.com Pass - shreeja@12345

Patient
harshal@gmail.com Pass - harshal@12345
aryan@gmail.com Pass - aryan@12345 -->
