import os
import django
from decimal import Decimal
import datetime
import random
import uuid
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinic_backend.settings')
django.setup()

from accounts.models import User
from doctors.models import Doctor, Department
from patients.models import Patient
from appointments.models import Appointment
from billing.models import Billing, Payment
from billing.services import sync_billing_ledger


def seed_data():
    print("========================================")
    print("Seeding Velora Care Hospital Data...")
    print("========================================")

    # 1. Departments
    dept_names = ["Cardiology", "Neurology", "Orthopedics", "Pediatrics", "General Medicine"]
    depts = {}
    for d_name in dept_names:
        dept, _ = Department.objects.get_or_create(
            name=d_name, defaults={"description": f"Department of {d_name}"}
        )
        depts[d_name] = dept

    # 2. Indian Doctors
    doctors_data = [
        {"first_name": "Ramesh", "last_name": "Sharma", "email": "ramesh.sharma@hospital.com", "spec": "Cardiologist", "dept": "Cardiology", "fee": Decimal("1500.00")},
        {"first_name": "Priya", "last_name": "Patel", "email": "priya.patel@hospital.com", "spec": "Neurologist", "dept": "Neurology", "fee": Decimal("1200.00")},
        {"first_name": "Amit", "last_name": "Singh", "email": "amit.singh@hospital.com", "spec": "Orthopedic Surgeon", "dept": "Orthopedics", "fee": Decimal("1000.00")},
        {"first_name": "Sunita", "last_name": "Rao", "email": "sunita.rao@hospital.com", "spec": "Pediatrician", "dept": "Pediatrics", "fee": Decimal("800.00")},
        {"first_name": "Vikram", "last_name": "Malhotra", "email": "vikram.malhotra@hospital.com", "spec": "General Physician", "dept": "General Medicine", "fee": Decimal("600.00")},
    ]

    doctors = []
    print("\n[1/4] Ensuring Doctors...")
    for doc in doctors_data:
        user, created = User.objects.get_or_create(
            email=doc["email"],
            defaults={
                "first_name": doc["first_name"],
                "last_name": doc["last_name"],
                "role": "DOCTOR",
                "phone": f"99{random.randint(10000000, 99999999)}",
            },
        )
        if created:
            user.set_password("Password@123")
            user.save()

        doctor, doc_created = Doctor.objects.get_or_create(
            user=user,
            defaults={
                "department": depts[doc["dept"]],
                "specialization": doc["spec"],
                "qualification": "MBBS, MD",
                "experience_years": random.randint(5, 25),
                "consultation_fee": doc["fee"],
                "license_number": f"MCI-{random.randint(10000, 99999)}",
                "bio": f"Senior {doc['spec']} at Velora Care Hospital.",
            },
        )
        doctors.append(doctor)
        if doc_created:
            print(f"  + Created Doctor: Dr. {doc['first_name']} {doc['last_name']}")

    # 3. Staff and Admin
    admin_user, _ = User.objects.get_or_create(
        email="admin@veloracare.com",
        defaults={
            "first_name": "Admin",
            "last_name": "Velora",
            "role": "ADMIN",
            "is_staff": True,
            "is_superuser": True,
        },
    )
    admin_user.set_password("Admin@123")
    admin_user.save()

    staff_user, _ = User.objects.get_or_create(
        email="cashier.staff@veloracare.com",
        defaults={
            "first_name": "Pooja",
            "last_name": "Sharma",
            "role": "STAFF",
            "is_staff": True,
        },
    )
    staff_user.set_password("Staff@123")
    staff_user.save()

    # 4. Indian Patients
    patients_data = [
        {"first_name": "Rahul", "last_name": "Verma", "email": "rahul.verma@gmail.com", "phone": "9876543210", "gender": "M", "blood": "B+"},
        {"first_name": "Sneha", "last_name": "Gupta", "email": "sneha.gupta@gmail.com", "phone": "9876543211", "gender": "F", "blood": "O+"},
        {"first_name": "Karan", "last_name": "Joshi", "email": "karan.joshi@gmail.com", "phone": "9876543212", "gender": "M", "blood": "A+"},
        {"first_name": "Anjali", "last_name": "Desai", "email": "anjali.desai@gmail.com", "phone": "9876543213", "gender": "F", "blood": "AB+"},
        {"first_name": "Rohan", "last_name": "Mehta", "email": "rohan.mehta@gmail.com", "phone": "9876543214", "gender": "M", "blood": "O-"},
    ]

    patients = []
    print("\n[2/4] Ensuring Patients...")
    for pat in patients_data:
        user, created = User.objects.get_or_create(
            email=pat["email"],
            defaults={
                "first_name": pat["first_name"],
                "last_name": pat["last_name"],
                "role": "PATIENT",
                "phone": pat["phone"],
            },
        )
        if created:
            user.set_password("Password@123")
            user.save()

        patient, pat_created = Patient.objects.get_or_create(
            user=user,
            defaults={
                "gender": pat["gender"],
                "blood_group": pat["blood"],
                "address": "Ahmedabad, Gujarat, India",
                "emergency_contact": f"98{random.randint(10000000, 99999999)}",
            },
        )
        patients.append(patient)
        if pat_created:
            print(f"  + Created Patient: {pat['first_name']} {pat['last_name']} ({patient.uhid})")

    # 5. Realistic Invoices & Payments
    print("\n[3/4] Creating Realistic Hospital Billing Invoices & Payment Ledger...")

    scenarios = [
        {
            "patient": patients[0], # Rahul Verma
            "doctor": doctors[0], # Dr. Ramesh Sharma
            "inv": "INV-2026-00101",
            "doc_fee": Decimal("1500.00"),
            "hosp_charge": Decimal("150.00"),
            "bed_charge": Decimal("2000.00"),
            "bed_days": 1,
            "bed_rate": Decimal("2000.00"),
            "lab_charge": Decimal("1350.00"),
            "total": Decimal("5000.00"),
            "discount": Decimal("0.00"),
            "final": Decimal("5000.00"),
            # Partial UPI Payment of 2000
            "payments": [
                {
                    "amount": Decimal("2000.00"),
                    "method": "UPI",
                    "status": "SUCCESS",
                    "ref": "PAY-UPI-RAHUL01",
                    "txn": "TXN-UPI-98421001",
                    "note": "Paid via Google Pay QR",
                }
            ],
        },
        {
            "patient": patients[1], # Sneha Gupta
            "doctor": doctors[1], # Dr. Priya Patel
            "inv": "INV-2026-00102",
            "doc_fee": Decimal("1200.00"),
            "hosp_charge": Decimal("120.00"),
            "bed_charge": Decimal("0.00"),
            "bed_days": 0,
            "bed_rate": Decimal("0.00"),
            "lab_charge": Decimal("1180.00"),
            "total": Decimal("2500.00"),
            "discount": Decimal("0.00"),
            "final": Decimal("2500.00"),
            # Fully paid via Cash at desk
            "payments": [
                {
                    "amount": Decimal("2500.00"),
                    "method": "CASH",
                    "status": "SUCCESS",
                    "ref": "PAY-CSH-SNEHA01",
                    "txn": "TXN-CSH-55441122",
                    "note": "Collected at OPD billing counter",
                    "user": staff_user,
                }
            ],
        },
        {
            "patient": patients[2], # Karan Joshi
            "doctor": doctors[2], # Dr. Amit Singh
            "inv": "INV-2026-00103",
            "doc_fee": Decimal("1000.00"),
            "hosp_charge": Decimal("100.00"),
            "bed_charge": Decimal("3000.00"),
            "bed_days": 2,
            "bed_rate": Decimal("1500.00"),
            "lab_charge": Decimal("900.00"),
            "total": Decimal("5000.00"),
            "discount": Decimal("1000.00"), # 20% loyalty discount
            "final": Decimal("4000.00"),
            # Multi-payment: 2000 Online UPI + 2000 Card
            "payments": [
                {
                    "amount": Decimal("2000.00"),
                    "method": "ONLINE_UPI",
                    "status": "SUCCESS",
                    "ref": "PAY-UPI-KARAN01",
                    "txn": "TXN-ONL-88229911",
                    "note": "PhonePe Online Payment",
                },
                {
                    "amount": Decimal("2000.00"),
                    "method": "CARD",
                    "status": "SUCCESS",
                    "ref": "PAY-CRD-KARAN02",
                    "txn": "TXN-CRD-33771144",
                    "note": "HDFC RuPay Debit Card",
                },
            ],
        },
        {
            "patient": patients[3], # Anjali Desai
            "doctor": doctors[3], # Dr. Sunita Rao
            "inv": "INV-2026-00104",
            "doc_fee": Decimal("800.00"),
            "hosp_charge": Decimal("80.00"),
            "bed_charge": Decimal("5000.00"),
            "bed_days": 2,
            "bed_rate": Decimal("2500.00"),
            "lab_charge": Decimal("2120.00"),
            "total": Decimal("8000.00"),
            "discount": Decimal("0.00"),
            "final": Decimal("8000.00"),
            # Insurance Claim
            "payments": [
                {
                    "amount": Decimal("8000.00"),
                    "method": "INSURANCE",
                    "status": "PENDING",
                    "ref": "PAY-INS-ANJALI01",
                    "note": "Star Health Pre-Auth Claim Submitted",
                    "insurance_provider": "Star Health & Allied Insurance",
                    "policy_number": "SH-POL-2026-7788",
                    "claim_number": "CLM-STAR-99001",
                    "insurance_status": "SUBMITTED",
                }
            ],
        },
        {
            "patient": patients[4], # Rohan Mehta
            "doctor": doctors[4], # Dr. Vikram Malhotra
            "inv": "INV-2026-00105",
            "doc_fee": Decimal("600.00"),
            "hosp_charge": Decimal("60.00"),
            "bed_charge": Decimal("0.00"),
            "bed_days": 0,
            "bed_rate": Decimal("0.00"),
            "lab_charge": Decimal("540.00"),
            "total": Decimal("1200.00"),
            "discount": Decimal("0.00"),
            "final": Decimal("1200.00"),
            "payments": [], # Completely Pending
        },
    ]

    for item in scenarios:
        # Create Appointment if needed
        apt, _ = Appointment.objects.get_or_create(
            patient=item["patient"],
            doctor=item["doctor"],
            appointment_date=datetime.date.today(),
            appointment_time=datetime.time(11, 0),
            defaults={"reason": "Hospital Consultation", "status": "APPROVED"},
        )

        billing, b_created = Billing.objects.get_or_create(
            invoice_number=item["inv"],
            defaults={
                "appointment": apt,
                "patient": item["patient"],
                "doctor_fee": item["doc_fee"],
                "hospital_charge": item["hosp_charge"],
                "bed_charge": item["bed_charge"],
                "bed_days": item["bed_days"],
                "bed_charge_per_day": item["bed_rate"],
                "lab_charge": item["lab_charge"],
                "discount_percentage": 20 if item["discount"] > 0 else 0,
                "discount_amount": item["discount"],
                "total_amount": item["total"],
                "final_amount": item["final"],
                "paid_amount": Decimal("0.00"),
                "payment_status": "PENDING",
            },
        )

        # Create Payments
        for p_data in item["payments"]:
            p, p_created = Payment.objects.get_or_create(
                payment_reference=p_data["ref"],
                defaults={
                    "billing": billing,
                    "patient": item["patient"],
                    "amount": p_data["amount"],
                    "currency": "INR",
                    "method": p_data["method"],
                    "provider": "mock" if p_data["method"] != "CASH" else "manual",
                    "status": p_data["status"],
                    "transaction_id": p_data.get("txn"),
                    "payment_note": p_data.get("note"),
                    "insurance_provider": p_data.get("insurance_provider"),
                    "policy_number": p_data.get("policy_number"),
                    "claim_number": p_data.get("claim_number"),
                    "insurance_status": p_data.get("insurance_status"),
                    "created_by": p_data.get("user") or admin_user,
                    "paid_at": timezone.now() if p_data["status"] == "SUCCESS" else None,
                },
            )

        # Synchronize ledger
        sync_billing_ledger(billing)
        billing.refresh_from_db()
        print(f"  + Invoice {billing.invoice_number}: Total Rs. {billing.final_amount}, Paid Rs. {billing.paid_amount}, Status {billing.payment_status}")

    print("\n========================================")
    print("Seed Completed Successfully!")
    print("========================================")


if __name__ == '__main__':
    seed_data()
