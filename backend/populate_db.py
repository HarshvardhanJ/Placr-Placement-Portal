#!/usr/bin/env python3
"""
Populate the PLACR database with demo data.

Usage:
    python populate_db.py
    python populate_db.py --no-reset

Run this inside the backend container or backend directory:
    docker compose exec flask python populate_db.py
"""

from __future__ import annotations

import argparse
import random
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable, List

from app import create_app
from app.extensions import bcrypt, db
from app.models.application import Application, ApplicationStatusEnum, InterviewEnum
from app.models.company import Company, CompanyStatusEnum
from app.models.drive import Drive, DriveStatusEnum
from app.models.placement import Placement
from app.models.student import Student
from app.models.user import User, UserRoleEnum
from app.utils.cache_helper import clear_cache_pattern


RNG = random.Random(42)

BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "uploads"
RESUMES_DIR = UPLOADS_DIR / "resumes"
OFFER_LETTERS_DIR = UPLOADS_DIR / "offer_letters"

ADMIN_EMAIL = "admin@admin.com"
ADMIN_PASSWORD = "admin"

COMPANY_PASSWORD = "Company123"
STUDENT_PASSWORD = "Student123"

FIRST_NAMES = [
    "Aarav",
    "Aanya",
    "Aditya",
    "Akshara",
    "Ananya",
    "Arjun",
    "Diya",
    "Ishaan",
    "Kavya",
    "Lakshmi",
    "Maya",
    "Nikhil",
    "Priya",
    "Rahul",
    "Riya",
    "Sana",
    "Shreya",
    "Sneha",
    "Tanvi",
    "Varun",
    "Vikram",
    "Zoya",
    "Meera",
    "Dev",
]

LAST_NAMES = [
    "Sharma",
    "Nair",
    "Iyer",
    "Reddy",
    "Menon",
    "Gupta",
    "Verma",
    "Patel",
    "Srinivasan",
    "Bhat",
    "Rao",
    "Das",
    "Khan",
    "Singh",
    "Jain",
    "Malhotra",
    "Kumar",
    "Pillai",
    "Yadav",
    "Chopra",
]

COMPANY_SEEDS = [
    {
        "name": "Nexora Systems",
        "industry": "Software",
        "location": "Bengaluru",
        "website": "https://nexora.example",
        "description": "Cloud-native product engineering and platform solutions.",
        "contact": "+91 90000 10001",
        "status": CompanyStatusEnum.approved,
    },
    {
        "name": "Aster Analytics",
        "industry": "Data Analytics",
        "location": "Hyderabad",
        "website": "https://aster.example",
        "description": "Data engineering, analytics dashboards, and reporting.",
        "contact": "+91 90000 10002",
        "status": CompanyStatusEnum.approved,
    },
    {
        "name": "BluePeak Technologies",
        "industry": "IT Services",
        "location": "Chennai",
        "website": "https://bluepeak.example",
        "description": "Enterprise software and full-stack delivery teams.",
        "contact": "+91 90000 10003",
        "status": CompanyStatusEnum.approved,
    },
    {
        "name": "Vertex AI Labs",
        "industry": "Artificial Intelligence",
        "location": "Pune",
        "website": "https://vertexailabs.example",
        "description": "AI products, ML engineering, and research tooling.",
        "contact": "+91 90000 10004",
        "status": CompanyStatusEnum.approved,
    },
    {
        "name": "Orbit Cloud",
        "industry": "Cloud Infrastructure",
        "location": "Bengaluru",
        "website": "https://orbitcloud.example",
        "description": "DevOps, SRE, and cloud migration services.",
        "contact": "+91 90000 10005",
        "status": CompanyStatusEnum.not_approved,
    },
]

DRIVE_SEEDS = [
    {
        "job_title": "Backend Engineer",
        "job_location": "Bengaluru",
        "min_cgpa": 6.5,
        "year": 4,
        "salary": 1200000,
        "required_skills": "Python, Flask, SQL, Redis, Docker",
        "experience_required": "0-2 years",
        "benefits": "Hybrid work, medical insurance, learning budget",
    },
    {
        "job_title": "Full Stack Developer",
        "job_location": "Hyderabad",
        "min_cgpa": 6.0,
        "year": 4,
        "salary": 1000000,
        "required_skills": "Vue.js, Flask, REST API, Git, SQL",
        "experience_required": "Internships or academic projects",
        "benefits": "Hybrid work, flexible hours, certification support",
    },
    {
        "job_title": "Data Analyst",
        "job_location": "Chennai",
        "min_cgpa": 6.5,
        "year": 4,
        "salary": 900000,
        "required_skills": "SQL, Python, Excel, Dashboards, Statistics",
        "experience_required": "0-1 year",
        "benefits": "Training stipend, performance bonus",
    },
    {
        "job_title": "Machine Learning Engineer",
        "job_location": "Pune",
        "min_cgpa": 7.0,
        "year": 4,
        "salary": 1500000,
        "required_skills": "Python, Machine Learning, PyTorch, Data Structures",
        "experience_required": "Internship experience preferred",
        "benefits": "Research mentorship, cloud credits, wellness support",
    },
    {
        "job_title": "DevOps Engineer",
        "job_location": "Remote",
        "min_cgpa": 6.5,
        "year": 4,
        "salary": 1300000,
        "required_skills": "Linux, Docker, Redis, CI/CD, AWS",
        "experience_required": "0-2 years",
        "benefits": "Remote work, home office support, upskilling budget",
    },
    {
        "job_title": "Software Engineer Intern",
        "job_location": "Bengaluru",
        "min_cgpa": 5.5,
        "year": 4,
        "salary": 600000,
        "required_skills": "Python, Git, HTML, CSS, JavaScript",
        "experience_required": "Students with project experience",
        "benefits": "Internship certificate, mentorship, pre-placement offer",
    },
    {
        "job_title": "Platform Engineer",
        "job_location": "Mumbai",
        "min_cgpa": 7.0,
        "year": 4,
        "salary": 1400000,
        "required_skills": "APIs, SQL, Kubernetes, Linux, Monitoring",
        "experience_required": "0-2 years",
        "benefits": "Health insurance, relocation support",
    },
    {
        "job_title": "Product Engineer",
        "job_location": "Delhi NCR",
        "min_cgpa": 6.5,
        "year": 4,
        "salary": 1100000,
        "required_skills": "Python, Web Development, SQL, Communication",
        "experience_required": "Project-based experience",
        "benefits": "Performance bonus, hybrid work, learning stipend",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Populate PLACR with demo data.")
    parser.add_argument(
        "--no-reset",
        action="store_true",
        help="Keep existing database rows and add new demo data on top.",
    )
    parser.add_argument(
        "--students",
        type=int,
        default=20,
        help="Number of demo students to create (default: 20).",
    )
    parser.add_argument(
        "--companies",
        type=int,
        default=len(COMPANY_SEEDS),
        help=f"Number of demo companies to create (default: {len(COMPANY_SEEDS)}).",
    )
    parser.add_argument(
        "--drives",
        type=int,
        default=len(DRIVE_SEEDS),
        help=f"Number of demo drives to create (default: {len(DRIVE_SEEDS)}).",
    )
    return parser.parse_args()


def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_minimal_pdf(lines: Iterable[str]) -> bytes:
    # One-page PDF with Helvetica text.
    content_lines = []
    y = 760
    for line in lines:
        content_lines.append(f"BT /F1 12 Tf 72 {y} Td ({pdf_escape(line)}) Tj ET")
        y -= 18
    content = "\n".join(content_lines).encode("latin-1")

    objects = []

    def add(obj: str) -> None:
        objects.append(obj.encode("latin-1"))

    add("1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n")
    add("2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n")
    add(
        "3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        "/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n"
    )
    add("4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n")
    add(
        f"5 0 obj << /Length {len(content)} >> stream\n".encode("latin-1").decode(
            "latin-1"
        )
    )
    # object 5 content must be inserted manually
    header = b"%PDF-1.4\n"
    body = b""
    offsets = [0]
    current = len(header)

    for i, obj in enumerate(objects, start=1):
        if i == 5:
            obj_prefix = f"5 0 obj << /Length {len(content)} >> stream\n".encode(
                "latin-1"
            )
            offsets.append(current)
            body += obj_prefix
            current += len(obj_prefix)
            offsets.append(current)
            body += content + b"\nendstream\nendobj\n"
            current += len(content) + len(b"\nendstream\nendobj\n")
        else:
            offsets.append(current)
            body += obj
            current += len(obj)

    xref_start = len(header) + len(body)
    xref = [b"xref\n0 6\n0000000000 65535 f \n"]
    # offsets list has [0, obj1, obj2, obj3, obj4, obj5start, obj5content]? simplify by reconstructing
    # Rebuild accurate offsets for all 5 objects
    offsets = [0]
    current = len(header)
    for idx, obj in enumerate(objects, start=1):
        if idx == 5:
            obj_prefix = f"5 0 obj << /Length {len(content)} >> stream\n".encode(
                "latin-1"
            )
            offsets.append(current)
            current += len(obj_prefix)
            offsets.append(current)
            current += len(content) + len(b"\nendstream\nendobj\n")
        else:
            offsets.append(current)
            current += len(obj)

    # We only need entries for objects 1..5, not the stream content offset.
    xref_entries = [
        f"{offsets[1]:010d} 00000 n \n".encode("latin-1"),
        f"{offsets[2]:010d} 00000 n \n".encode("latin-1"),
        f"{offsets[3]:010d} 00000 n \n".encode("latin-1"),
        f"{offsets[4]:010d} 00000 n \n".encode("latin-1"),
        f"{offsets[5]:010d} 00000 n \n".encode("latin-1"),
    ]
    xref_bytes = b"xref\n0 6\n0000000000 65535 f \n" + b"".join(xref_entries)
    trailer = (
        f"trailer << /Size 6 /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF\n".encode(
            "latin-1"
        )
    )
    # Build full body once correctly, because above body contains all objects plus stream.
    body = b""
    current = len(header)
    for idx, obj in enumerate(objects, start=1):
        if idx == 5:
            obj_prefix = f"5 0 obj << /Length {len(content)} >> stream\n".encode(
                "latin-1"
            )
            body += obj_prefix
            body += content + b"\nendstream\nendobj\n"
        else:
            body += obj

    return header + body + xref_bytes + trailer


def write_pdf(path: Path, title: str, lines: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pdf_lines = [title, ""] + lines
    path.write_bytes(build_minimal_pdf(pdf_lines))


def random_choice(items):
    return RNG.choice(items)


def random_sample(items, k):
    return RNG.sample(items, k)


def make_name(index: int) -> str:
    return f"{random_choice(FIRST_NAMES)} {random_choice(LAST_NAMES)}"


def make_email(name: str, index: int) -> str:
    base = name.lower().replace(" ", ".")
    return f"{base}.{index:02d}@demo.placr.local"


def make_roll_no(index: int) -> str:
    return f"24F2001{index:03d}"


def clear_uploads() -> None:
    for folder in (RESUMES_DIR, OFFER_LETTERS_DIR):
        folder.mkdir(parents=True, exist_ok=True)
        for item in folder.iterdir():
            if item.name == ".gitkeep":
                continue
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)


def reset_database() -> None:
    # Clear children before parents to avoid FK issues.
    db.session.query(Placement).delete(synchronize_session=False)
    db.session.query(Application).delete(synchronize_session=False)
    db.session.query(Drive).delete(synchronize_session=False)
    db.session.query(Student).delete(synchronize_session=False)
    db.session.query(Company).delete(synchronize_session=False)
    db.session.query(User).filter(User.role != UserRoleEnum.admin).delete(
        synchronize_session=False
    )
    db.session.commit()
    clear_uploads()
    clear_cache_pattern("admin_")
    clear_cache_pattern("company_")
    clear_cache_pattern("student_")
    clear_cache_pattern("flask_cache_")


def ensure_admin_user() -> User:
    admin = User.query.filter_by(email=ADMIN_EMAIL).first()
    if admin:
        if admin.role != UserRoleEnum.admin:
            admin.role = UserRoleEnum.admin
            db.session.commit()
        return admin

    admin = User(
        email=ADMIN_EMAIL,
        password=bcrypt.generate_password_hash(ADMIN_PASSWORD).decode("utf-8"),
        role=UserRoleEnum.admin,
    )
    db.session.add(admin)
    db.session.commit()
    return admin


def create_company(seed: dict, index: int) -> Company:
    name = seed["name"]
    email = f"contact.{index:02d}@{name.lower().replace(' ', '')}.demo"
    user = User(
        email=email,
        password=bcrypt.generate_password_hash(COMPANY_PASSWORD).decode("utf-8"),
        role=UserRoleEnum.company,
    )
    db.session.add(user)
    db.session.flush()

    company = Company(
        user_id=user.user_id,
        name=name,
        contact=seed["contact"],
        website=seed["website"],
        industry=seed["industry"],
        description=seed["description"],
        location=seed["location"],
        approval_status=seed["status"],
    )
    db.session.add(company)
    db.session.flush()
    return company


def create_student(index: int) -> Student:
    name = make_name(index)
    user = User(
        email=make_email(name, index),
        password=bcrypt.generate_password_hash(STUDENT_PASSWORD).decode("utf-8"),
        role=UserRoleEnum.student,
    )
    db.session.add(user)
    db.session.flush()

    department = random_choice(["CSE", "ECE", "EEE", "ME", "CE", "MSE", "AI"])
    cgpa = round(RNG.uniform(6.3, 9.7), 2)
    year = 4
    skills_pool = [
        "Python",
        "Flask",
        "SQL",
        "Redis",
        "Docker",
        "Git",
        "Linux",
        "JavaScript",
        "Vue.js",
        "Data Structures",
        "Problem Solving",
    ]
    chosen_skills = random_sample(skills_pool, 6)

    student = Student(
        user_id=user.user_id,
        name=name,
        roll_no=make_roll_no(index),
        phone_number=f"+91 98{index:08d}"[:13],
        department=department,
        cgpa=cgpa,
        year=year,
        skills=", ".join(chosen_skills),
        experience=(
            "Built backend and full-stack academic projects involving Flask, Vue, "
            "SQLAlchemy, Docker, Redis, and JWT authentication."
        ),
    )
    db.session.add(student)
    db.session.flush()

    resume_path = RESUMES_DIR / f"{student.student_id}_resume.pdf"
    write_pdf(
        resume_path,
        f"{student.name} - Resume",
        [
            f"Name: {student.name}",
            f"Roll No: {student.roll_no}",
            f"Department: {student.department}",
            f"CGPA: {student.cgpa}",
            f"Skills: {student.skills}",
            "Demo resume generated for PLACR.",
        ],
    )
    student.resume_path = str(resume_path)
    return student


def create_drive(company: Company, seed: dict, index: int) -> Drive:
    now = datetime.utcnow()
    status = DriveStatusEnum.approved
    # Keep a mix of states for demo purposes.
    if index == 1:
        status = DriveStatusEnum.pending
    elif index == 2:
        status = DriveStatusEnum.rejected

    application_deadline = now + timedelta(days=14 + index * 4)
    if index == 5:
        application_deadline = now - timedelta(days=3)
        status = DriveStatusEnum.closed

    drive = Drive(
        company_id=company.company_id,
        approval_status=status,
        job_title=seed["job_title"],
        job_description=(
            f"{seed['job_title']} role for the {company.name} engineering team. "
            "Work on scalable systems, APIs, and internal tools."
        ),
        job_location=seed["job_location"],
        application_deadline=application_deadline,
        eligible_branch="ALL",
        min_cgpa=seed["min_cgpa"],
        year=seed["year"],
        no_openings=RNG.randint(3, 8),
        salary=seed["salary"],
        required_skills=seed["required_skills"],
        experience_required=seed["experience_required"],
        benefits=seed["benefits"],
    )
    db.session.add(drive)
    db.session.flush()
    return drive


def create_application(
    student: Student, drive: Drive, status: ApplicationStatusEnum
) -> Application:
    application = Application(
        student_id=student.student_id,
        drive_id=drive.drive_id,
        status=status,
        remarks=(
            "Strong technical profile"
            if status == ApplicationStatusEnum.shortlisted
            else "Selected after interview"
            if status == ApplicationStatusEnum.selected
            else "Good fit for current requirements"
            if status == ApplicationStatusEnum.applied
            else "Not selected in current round"
        ),
    )

    now = datetime.utcnow()
    if status == ApplicationStatusEnum.shortlisted:
        application.interview_date = now + timedelta(days=3 + RNG.randint(0, 5))
        application.interview_type = random_choice(
            [InterviewEnum.online, InterviewEnum.inPerson]
        )
    elif status == ApplicationStatusEnum.selected:
        application.interview_date = now - timedelta(days=1)
        application.interview_type = random_choice(
            [InterviewEnum.online, InterviewEnum.inPerson]
        )

    db.session.add(application)
    db.session.flush()
    return application


def create_placement(
    application: Application, company: Company, drive: Drive, with_offer_letter: bool
) -> Placement:
    placement = Placement(
        application_id=application.application_id,
        salary=drive.salary if drive.salary else RNG.randint(700000, 1400000),
        joining_date=datetime.utcnow() + timedelta(days=30 + RNG.randint(0, 45)),
    )
    db.session.add(placement)
    db.session.flush()

    if with_offer_letter:
        offer_letter_path = (
            OFFER_LETTERS_DIR / f"{placement.placement_id}_offer_letter.pdf"
        )
        write_pdf(
            offer_letter_path,
            f"Offer Letter - {company.name}",
            [
                f"Placement ID: {placement.placement_id}",
                f"Company: {company.name}",
                f"Role: {drive.job_title}",
                f"Salary: {placement.salary}",
                f"Joining Date: {placement.joining_date.date()}",
                "Congratulations! This is a demo offer letter.",
            ],
        )
        placement.offer_letter_path = str(offer_letter_path)

    return placement


def seed_data(students_count: int, companies_count: int, drives_count: int) -> None:
    ensure_admin_user()

    companies: List[Company] = []
    students: List[Student] = []
    drives: List[Drive] = []

    for idx in range(companies_count):
        seed = COMPANY_SEEDS[idx % len(COMPANY_SEEDS)]
        # Make sure extra copies have distinct names/emails if requested.
        if idx >= len(COMPANY_SEEDS):
            seed = dict(seed)
            seed["name"] = f"{seed['name']} {idx + 1}"
            seed["website"] = f"https://{seed['name'].lower().replace(' ', '')}.example"
            seed["contact"] = f"+91 90000 {10000 + idx}"
            seed["status"] = CompanyStatusEnum.approved
        companies.append(create_company(seed, idx))

    for idx in range(students_count):
        students.append(create_student(idx + 1))

    db.session.commit()

    for idx in range(drives_count):
        company = companies[idx % len(companies)]
        seed = DRIVE_SEEDS[idx % len(DRIVE_SEEDS)]
        if idx >= len(DRIVE_SEEDS):
            seed = dict(seed)
            seed["job_title"] = f"{seed['job_title']} {idx + 1}"
            seed["salary"] = int(seed["salary"] * (1 + (idx % 3) * 0.1))
        drive = create_drive(company, seed, idx)
        drives.append(drive)

    db.session.commit()

    # Make every student eligible and create a realistic application pipeline.
    active_drives = [d for d in drives if d.approval_status == DriveStatusEnum.approved]
    statuses_cycle = [
        ApplicationStatusEnum.applied,
        ApplicationStatusEnum.applied,
        ApplicationStatusEnum.shortlisted,
        ApplicationStatusEnum.shortlisted,
        ApplicationStatusEnum.selected,
        ApplicationStatusEnum.rejected,
    ]

    used_pairs = set()
    applications: List[Application] = []

    for drive in active_drives:
        applicants = RNG.sample(students, k=min(4, len(students)))
        for pos, student in enumerate(applicants):
            if (student.student_id, drive.drive_id) in used_pairs:
                continue
            status = statuses_cycle[(pos + len(applications)) % len(statuses_cycle)]
            app = create_application(student, drive, status)
            used_pairs.add((student.student_id, drive.drive_id))
            applications.append(app)

            if status == ApplicationStatusEnum.selected:
                placement = create_placement(
                    app,
                    drive.company,
                    drive,
                    with_offer_letter=((len(applications) + pos) % 2 == 0),
                )

    db.session.commit()

    clear_cache_pattern("admin_")
    clear_cache_pattern("company_")
    clear_cache_pattern("student_")
    clear_cache_pattern("flask_cache_")

    print(f"Created/updated {companies_count} companies.")
    print(f"Created/updated {students_count} students.")
    print(f"Created/updated {drives_count} drives.")
    print(f"Created {len(applications)} applications/placements where applicable.")


def main() -> None:
    args = parse_args()
    app = create_app()

    with app.app_context():
        db.create_all()

        if not args.no_reset:
            print("Resetting existing demo data...")
            reset_database()
            # Re-create tables after deleting data in case the DB was empty/brand new.
            db.create_all()

        seed_data(args.students, args.companies, args.drives)
        print("\nDemo database populated successfully.")
        print(f"Admin login: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
        print(
            f"Student login: auto-generated demo accounts, password = {STUDENT_PASSWORD}"
        )
        print(
            f"Company login: auto-generated demo accounts, password = {COMPANY_PASSWORD}"
        )


if __name__ == "__main__":
    main()
