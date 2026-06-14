# Placement Portal Application

> Full-stack placement management platform built using Flask, Vue.js, Docker, Redis, and Celery.

## Overview

The Placement Portal Application is a web platform designed to streamline the campus placement process by connecting students, recruiters, and placement administrators through a unified system.

The platform provides role-based access for:

* Students
* Companies
* Placement Administrators

and supports the complete placement workflow from job posting to offer letter distribution.

**Note:** The source code repository is currently private due to academic evaluation requirements. It will be made public after project evaluation is completed.

---

## Key Features

### Student Portal

* Student registration and authentication
* Profile management
* Resume upload
* Browse and search placement drives
* Apply for job opportunities
* Track application status
* View interview schedules
* Download offer letters

### Company Portal

* Company registration
* Placement drive creation
* Applicant management
* Candidate shortlisting
* Interview scheduling
* Placement management
* Offer letter upload

### Admin Portal

* Company approval workflow
* Placement drive approval workflow
* Student and company management
* Search functionality
* User blacklisting/deactivation
* System-wide monitoring dashboard

---

## Technology Stack

### Backend

* Flask
* SQLAlchemy
* JWT Authentication
* SQLite

### Frontend

* Vue.js

### Infrastructure

* Docker
* Redis
* Celery

---

## System Architecture

```mermaid
flowchart TD

    U[Student]
    C[Company]
    A[Admin]

    U --> V[Vue Frontend]
    C --> V
    A --> V

    V --> F[Flask REST API]

    F --> JWT[JWT Authentication]
    F --> ORM[SQLAlchemy ORM]

    ORM --> DB[(SQLite Database)]

    F --> R[(Redis)]
    R --> CELERY[Celery Workers]

    CELERY --> CSV[CSV Export Jobs]
    CELERY --> REM[Interview Reminder Jobs]
    CELERY --> REP[Placement Report Jobs]
```
## Database ER Diagram

```mermaid
erDiagram

    USER ||--o| STUDENT : has
    USER ||--o| COMPANY : has

    COMPANY ||--o{ DRIVE : creates

    STUDENT ||--o{ APPLICATION : submits
    DRIVE ||--o{ APPLICATION : receives

    APPLICATION ||--o| PLACEMENT : generates

    USER {
        string user_id PK
        string email
        string password
        string role
        bool is_active
    }

    STUDENT {
        string student_id PK
        string user_id FK
        string name
        string roll_no
        string department
        float cgpa
        int year
    }

    COMPANY {
        string company_id PK
        string user_id FK
        string name
        string industry
        string location
    }

    DRIVE {
        string drive_id PK
        string company_id FK
        string job_title
        string salary
        string approval_status
    }

    APPLICATION {
        string application_id PK
        string student_id FK
        string drive_id FK
        string status
    }

    PLACEMENT {
        string placement_id PK
        string application_id FK
        int salary
        datetime joining_date
    }
```

## Placement Workflow

```mermaid
flowchart TD

    SR[Student Registration]
    SP[Complete Profile]
    RU[Upload Resume]

    JD[Browse Placement Drives]
    AP[Apply to Drive]

    RV[Company Reviews Application]
    SL[Shortlist Candidate]

    INT[Schedule Interview]

    SEL[Select Candidate]

    PLC[Create Placement Record]

    OFF[Upload Offer Letter]

    DL[Student Downloads Offer Letter]

    SR --> SP
    SP --> RU
    RU --> JD
    JD --> AP
    AP --> RV
    RV --> SL
    SL --> INT
    INT --> SEL
    SEL --> PLC
    PLC --> OFF
    OFF --> DL
```

---

## Current Status

* Backend APIs implemented
* Authentication and RBAC completed
* Admin workflows completed
* Company workflows completed
* Student workflows completed
* Placement tracking completed
* Frontend currently under development
* Redis and Celery integration in progress

---

## Future Enhancements

* Redis caching
* Background task processing using Celery
* Automated interview reminders
* Placement analytics dashboard
* Resume screening (ATS)
* Cloud deployment

```
```
