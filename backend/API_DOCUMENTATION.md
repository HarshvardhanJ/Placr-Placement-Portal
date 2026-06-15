# Backend API Documentation

This document covers all Flask APIs currently defined in `backend/app/api`.
The API base path is `/api`.

## Quick Reference

| Area | Prefix | Main Users |
| --- | --- | --- |
| Authentication | `/api/auth` | Public, all logged-in users |
| Admin | `/api/admin` | Admin |
| Student | `/api/student` | Student |
| Company | `/api/company` | Company |

## Authentication

Protected endpoints use JWT bearer auth.

```http
Authorization: Bearer <token>
```

The token is returned by `POST /api/auth/login`.

Role-protected endpoints return:

```json
{ "error": "Forbidden" }
```

when the logged-in user has the wrong role.

Some endpoints also require the account to be active or the company to be approved:

| Requirement | Failure Response |
| --- | --- |
| Active account | `403 { "error": "Account has been disabled" }` |
| Approved company | `403 { "error": "Company approval pending" }` |

## Common Data Shapes

### User Roles

```json
"admin" | "student" | "company"
```

### Company Approval Status

```json
"approved" | "not_approved"
```

### Drive Approval Status

```json
"pending" | "approved" | "closed" | "rejected"
```

### Application Status

```json
"applied" | "shortlisted" | "selected" | "rejected"
```

### Interview Type

```json
"online" | "inPerson"
```

### Student Object

Returned by student profile APIs and admin student list.

```json
{
  "student_id": "uuid",
  "user_id": "uuid",
  "name": "Student Name",
  "roll_no": "ROLL001",
  "phone_number": "9999999999",
  "department": "CSE",
  "cgpa": 8.5,
  "year": 3,
  "skills": "Python, React",
  "experience": "Internship details",
  "created_at": "2026-06-15 10:00:00"
}
```

Admin student list additionally includes:

```json
{ "is_active": true }
```

### Company Object

```json
{
  "company_id": "uuid",
  "user_id": "uuid",
  "name": "Acme Ltd",
  "contact": "hr@acme.com",
  "website": "https://example.com",
  "approval_status": "approved",
  "industry": "Software",
  "description": "Company description",
  "location": "Bengaluru",
  "created_at": "2026-06-15 10:00:00"
}
```

Admin company list additionally includes:

```json
{ "is_active": true }
```

### Drive Object

```json
{
  "company_name": "Acme Ltd",
  "drive_id": "uuid",
  "company_id": "uuid",
  "job_title": "Software Engineer",
  "job_description": "Role details",
  "job_location": "Bengaluru",
  "application_deadline": "2026-07-01 23:59:00",
  "min_cgpa": 7.0,
  "required_skills": "Python, Flask, React",
  "experience_required": "0-1 years",
  "benefits": "Health insurance",
  "approval_status": "pending",
  "year": 4,
  "no_openings": 5,
  "salary": 1200000,
  "created_at": "2026-06-15 10:00:00"
}
```

Note: `eligible_branch` is accepted when creating/updating drives and is used for eligibility checks, but it is not currently included in `Drive.to_dict()` responses.

### Application Object

```json
{
  "application_id": "uuid",
  "student_id": "uuid",
  "drive_id": "uuid",
  "application_date": "2026-06-15 10:00:00",
  "status": "applied",
  "remarks": null,
  "interview_date": null,
  "interview_type": null,
  "drive": {
    "company_name": "Acme Ltd",
    "drive_id": "uuid"
  }
}
```

## Auth APIs

### Login

`POST /api/auth/login`

Auth: public

Request:

```json
{
  "email": "user@example.com",
  "password": "password"
}
```

Success `200`:

```json
{
  "token": "jwt-token",
  "user": {
    "email": "user@example.com",
    "role": "student"
  }
}
```

Errors:

| Status | Response |
| --- | --- |
| 400 | `{ "error": "Missing email or password in request body" }` |
| 401 | `{ "error": "Wrong email or password!" }` |
| 403 | `{ "error": "Your account has been deactivated. Please contact the administrator." }` |
| 404 | `{ "error": "User does not exist" }` |

### Register Student

`POST /api/auth/register/student`

Auth: public

Request:

```json
{
  "email": "student@example.com",
  "password": "password",
  "repeat_password": "password",
  "name": "Student Name",
  "roll_no": "ROLL001"
}
```

Success `201`:

```json
{ "success": "User created successfully!" }
```

Errors:

| Status | Response |
| --- | --- |
| 400 | `{ "error": "Missing data fields" }` |
| 400 | `{ "error": "Password do not match" }` |
| 409 | `{ "error": "User already exists" }` |
| 409 | `{ "error": "Student with this roll number already exists" }` |
| 500 | `{ "error": "Registration failed", "details": "..." }` |

### Register Company

`POST /api/auth/register/company`

Auth: public

Request:

```json
{
  "email": "company@example.com",
  "password": "password",
  "repeat_password": "password",
  "name": "Acme Ltd"
}
```

Success `201`:

```json
{ "success": "User created successfully!" }
```

Errors:

| Status | Response |
| --- | --- |
| 400 | `{ "error": "Missing data fields" }` |
| 400 | `{ "error": "Password do not match" }` |
| 409 | `{ "error": "User already exists" }` |
| 409 | `{ "error": "Company with this name already exists" }` |
| 500 | `{ "error": "Registration failed", "details": "..." }` |

### Current User

`GET /api/auth/me`

Auth: any logged-in user

Success `200` for admin:

```json
{
  "email": "admin@example.com",
  "role": "admin"
}
```

Success `200` for student:

```json
{
  "email": "student@example.com",
  "role": "student",
  "name": "Student Name",
  "roll_no": "ROLL001",
  "department": "CSE"
}
```

Success `200` for company:

```json
{
  "email": "company@example.com",
  "role": "company",
  "name": "Acme Ltd",
  "approval_status": "approved"
}
```

## Admin APIs

All admin APIs require:

```http
Authorization: Bearer <admin-token>
```

### Admin Dashboard

`GET /api/admin/dashboard`

Success `200`:

```json
{
  "total_students": 10,
  "total_companies": 4,
  "total_drives": 8,
  "total_applications": 20
}
```

### List Companies

`GET /api/admin/companies`

Query params:

| Name | Type | Description |
| --- | --- | --- |
| `search` | string | Optional. Searches company name and industry. |

Success `200`:

```json
[
  {
    "company_id": "uuid",
    "name": "Acme Ltd",
    "approval_status": "not_approved",
    "industry": "Software",
    "is_active": true
  }
]
```

### Approve Company

`PUT /api/admin/companies/<company_id>/approve`

Success `200`:

```json
{ "success": "Company Acme Ltd approved" }
```

Errors:

| Status | Response |
| --- | --- |
| 404 | `{ "error": "Company not found!" }` |
| 500 | `{ "error": "Failed to update company <id>", "details": "..." }` |

### Reject Company

`PUT /api/admin/companies/<company_id>/reject`

Sets `approval_status` to `not_approved`.

Success `200`:

```json
{ "success": "Company Acme Ltd rejected" }
```

### Blacklist Company

`PUT /api/admin/companies/<company_id>/blacklist`

Sets the linked user account `is_active` to `false`.

Success `200`:

```json
{ "success": "Company Acme Ltd blacklisted" }
```

### List Students

`GET /api/admin/students`

Query params:

| Name | Type | Description |
| --- | --- | --- |
| `search` | string | Optional. Searches student name, roll number, and phone number. |

Success `200`:

```json
[
  {
    "student_id": "uuid",
    "name": "Student Name",
    "roll_no": "ROLL001",
    "department": "CSE",
    "cgpa": 8.5,
    "year": 3,
    "is_active": true
  }
]
```

### Blacklist Student

`PUT /api/admin/students/<student_id>/blacklist`

Sets the linked user account `is_active` to `false`.

Success `200`:

```json
{ "success": "Student Student Name blacklisted" }
```

### List Drives

`GET /api/admin/drives`

Success `200`:

```json
[
  {
    "drive_id": "uuid",
    "company_name": "Acme Ltd",
    "job_title": "Software Engineer",
    "approval_status": "pending"
  }
]
```

### Approve Drive

`PUT /api/admin/drives/<drive_id>/approve`

Success `200`:

```json
{ "success": "Drive <drive_id> approved" }
```

### Reject Drive

`PUT /api/admin/drives/<drive_id>/reject`

Success `200`:

```json
{ "success": "Drive <drive_id> rejected" }
```

### List Applications

`GET /api/admin/applications`

Success `200`:

```json
[
  {
    "application_id": "uuid",
    "student_name": "Student Name",
    "roll_no": "ROLL001",
    "company": "Acme Ltd",
    "job_title": "Software Engineer",
    "status": "applied",
    "application_date": "2026-06-15 10:00:00"
  }
]
```

## Student APIs

Student APIs require:

```http
Authorization: Bearer <student-token>
```

Endpoints marked active-only also require the user account to be active.

### Student Dashboard

`GET /api/student/dashboard`

Auth: student, active-only

Success `200`:

```json
{
  "counts": {
    "eligible": 3,
    "applied": 2,
    "shortlisted": 1,
    "selected": 0
  },
  "eligible_drives": [
    {
      "drive_id": "uuid",
      "job_title": "Software Engineer",
      "status": "eligible"
    }
  ],
  "applied_drives": [
    {
      "application_id": "uuid",
      "application_date": "2026-06-15 10:00:00",
      "status": "applied",
      "drive": {}
    }
  ],
  "shortlisted_drives": [
    {
      "application_id": "uuid",
      "status": "shortlisted",
      "remarks": "Good profile",
      "interview_date": "2026-06-20 10:00:00",
      "interview_type": "online",
      "drive": {}
    }
  ],
  "selected_drives": [],
  "upcoming_interviews": [
    {
      "application_id": "uuid",
      "company": "Acme Ltd",
      "job_title": "Software Engineer",
      "interview_date": "2026-06-20 10:00:00",
      "interview_type": "online"
    }
  ]
}
```

Errors:

| Status | Response |
| --- | --- |
| 400 | `{ "error": "Complete your profile (department, CGPA, year) before viewing eligible drives" }` |
| 404 | `{ "error": "Student not found" }` |

### Get Student Profile

`GET /api/student/profile`

Auth: student

Success `200`: student object.

### Update Student Profile

`PUT /api/student/profile`

Auth: student, active-only

Allowed request fields:

```json
{
  "name": "Student Name",
  "department": "CSE",
  "cgpa": 8.5,
  "year": 3,
  "phone_number": "9999999999",
  "skills": "Python, React",
  "experience": "Internship details"
}
```

Validation:

| Field | Rule |
| --- | --- |
| `cgpa` | Number from `0` to `10` |
| `year` | One of `1`, `2`, `3`, `4` |
| `skills` | String, max 2000 chars |
| `experience` | String, max 2000 chars |

Success `200`:

```json
{
  "message": "Profile updated successfully",
  "student": {}
}
```

Errors:

| Status | Response |
| --- | --- |
| 400 | `{ "error": "Request body is required" }` |
| 400 | `{ "error": "Field '<field>' cannot be updated" }` |
| 400 | `{ "error": "CGPA must be between 0 and 10" }` |
| 400 | `{ "error": "Year must be between 1 and 4" }` |

### Upload Resume

`POST /api/student/profile/resume`

Auth: student, active-only

Content-Type: `multipart/form-data`

Form fields:

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `resume` | file | Yes | Must be a PDF file. |

Success `200`:

```json
{
  "message": "Resume uploaded successfully",
  "resume_path": "/absolute/or/runtime/path/uploads/resumes/file.pdf"
}
```

Errors:

| Status | Response |
| --- | --- |
| 400 | `{ "error": "Resume file is required" }` |
| 400 | `{ "error": "Only PDF files are allowed" }` |

### List Available Drives

`GET /api/student/drives`

Auth: student, active-only

Query params:

| Name | Type | Description |
| --- | --- | --- |
| `search` | string | Optional. Searches company name, job title, job description, and required skills. |

Only returns drives that:

- are approved
- have not passed their application deadline
- match the student's CGPA, year, and department
- have not already been applied to by the student

Success `200`:

```json
{
  "count": 2,
  "drives": [
    {
      "drive_id": "uuid",
      "company_name": "Acme Ltd",
      "job_title": "Software Engineer"
    }
  ]
}
```

Errors:

| Status | Response |
| --- | --- |
| 400 | `{ "error": "Complete your profile (department, CGPA, year) before viewing drives" }` |

### Get Drive Details

`GET /api/student/drives/<drive_id>`

Auth: student, active-only

Only approved drives can be fetched through this endpoint.

Success `200`: drive object.

Errors:

| Status | Response |
| --- | --- |
| 404 | `{ "error": "Drive not found" }` |

### Apply To Drive

`POST /api/student/drives/<drive_id>/apply`

Auth: student, active-only

Request body: none required.

Success `201`:

```json
{
  "message": "Application submitted successfully",
  "application_id": "uuid"
}
```

Rules:

- Student profile must include `department`, `cgpa`, and `year`.
- Student must have uploaded a resume.
- Drive must be approved and deadline must not have passed.
- Student must satisfy CGPA, year, and eligible branch requirements.
- Student cannot apply twice to the same drive.

Errors:

| Status | Response |
| --- | --- |
| 400 | `{ "error": "Complete your profile before applying" }` |
| 400 | `{ "error": "Upload your resume before applying" }` |
| 400 | `{ "error": "Application deadline has passed" }` |
| 403 | `{ "error": "Minimum CGPA required is <min_cgpa>" }` |
| 403 | `{ "error": "Only year <year> students can apply" }` |
| 403 | `{ "error": "You are not eligible for this drive" }` |
| 409 | `{ "error": "You have already applied to this drive" }` |

### List Student Applications

`GET /api/student/applications`

Auth: student

Success `200`:

```json
{
  "count": 2,
  "applications": [
    {
      "application_id": "uuid",
      "status": "applied",
      "drive": {}
    }
  ]
}
```

### List Student Placements

`GET /api/student/placements`

Auth: student, active-only

Success `200`:

```json
{
  "count": 1,
  "placements": [
    {
      "placement_id": "uuid",
      "company": "Acme Ltd",
      "job_title": "Software Engineer",
      "salary": 1200000,
      "joining_date": "2026-08-01 09:00:00",
      "offer_letter_available": true,
      "created_at": "2026-06-15 10:00:00"
    }
  ]
}
```

### Get Student Placement Details

`GET /api/student/placements/<placement_id>`

Auth: student, active-only

Success `200`:

```json
{
  "placement_id": "uuid",
  "company": "Acme Ltd",
  "job_title": "Software Engineer",
  "salary": 1200000,
  "joining_date": "2026-08-01 09:00:00",
  "offer_letter_available": true,
  "created_at": "2026-06-15 10:00:00"
}
```

### Download Offer Letter

`GET /api/student/placements/<placement_id>/offer-letter`

Auth: student, active-only

Success `200`: PDF file download.

Errors:

| Status | Response |
| --- | --- |
| 404 | `{ "error": "Placement not found" }` |
| 404 | `{ "error": "Offer letter not available" }` |
| 404 | `{ "error": "Offer letter file missing" }` |

## Company APIs

Company APIs require:

```http
Authorization: Bearer <company-token>
```

Most company APIs require the company to be approved by an admin. `GET /api/company/profile` can be used before approval.

### Company Dashboard

`GET /api/company/dashboard`

Auth: company, approved-only

Success `200`:

```json
{
  "company": {
    "company_id": "uuid",
    "name": "Acme Ltd",
    "industry": "Software",
    "location": "Bengaluru",
    "description": "Company description",
    "approval_status": "approved"
  },
  "counts": {
    "drives": 3,
    "applications": 20,
    "shortlisted": 5,
    "selected": 2,
    "upcoming_interviews": 3
  },
  "recent_drives": [
    {
      "drive_id": "uuid",
      "job_title": "Software Engineer",
      "required_skills": "Python",
      "experience_required": "0-1 years",
      "benefits": "Health insurance",
      "approval_status": "approved",
      "application_deadline": "2026-07-01 23:59:00",
      "applications": 10
    }
  ],
  "recent_applications": [
    {
      "application_id": "uuid",
      "student_name": "Student Name",
      "roll_no": "ROLL001",
      "job_title": "Software Engineer",
      "status": "applied",
      "applied_on": "2026-06-15 10:00:00"
    }
  ],
  "shortlisted_candidates": [],
  "upcoming_interviews": []
}
```

### Get Company Profile

`GET /api/company/profile`

Auth: company

Success `200`: company object.

### Update Company Profile

`PUT /api/company/profile`

Auth: company, approved-only

Allowed request fields:

```json
{
  "contact": "hr@acme.com",
  "website": "https://example.com",
  "industry": "Software",
  "description": "Company description",
  "location": "Bengaluru"
}
```

Success `200`:

```json
{
  "message": "Profile updated successfully",
  "company": {}
}
```

Errors:

| Status | Response |
| --- | --- |
| 400 | `{ "error": "Request body is required" }` |
| 400 | `{ "message": "Invalid field: <field>" }` |

### List Company Drives

`GET /api/company/drives`

Auth: company, approved-only

Success `200`:

```json
{
  "drives": [
    {
      "drive_id": "uuid",
      "job_title": "Software Engineer",
      "approval_status": "pending"
    }
  ]
}
```

### Create Drive

`POST /api/company/drives`

Auth: company, approved-only

Required fields:

- `job_title`
- `application_deadline`

Allowed request fields:

```json
{
  "job_title": "Software Engineer",
  "job_location": "Bengaluru",
  "job_description": "Role details",
  "application_deadline": "2026-07-01T23:59:00",
  "eligible_branch": "CSE,ECE",
  "min_cgpa": 7.0,
  "year": 4,
  "no_openings": 5,
  "salary": 1200000,
  "required_skills": "Python, React",
  "experience_required": "0-1 years",
  "benefits": "Health insurance"
}
```

Use `"ALL"` in `eligible_branch` to make the drive eligible for all departments.

Validation:

| Field | Rule |
| --- | --- |
| `application_deadline` | ISO date/time string accepted by Python `datetime.fromisoformat` |
| `required_skills` | String, max 2000 chars |
| `experience_required` | String, max 2000 chars |
| `benefits` | String, max 2000 chars |
| `min_cgpa` | Database constraint: 0 to 10 |
| `no_openings` | Database constraint: greater than 0 |

Success `201`:

```json
{
  "message": "Drive created successfully",
  "drive_id": "uuid"
}
```

Errors:

| Status | Response |
| --- | --- |
| 400 | `{ "error": "Missing data fields" }` |
| 400 | `{ "message": "Invalid field: <field>" }` |
| 400 | `{ "error": "Invalid application_deadline format" }` |

### Get Company Drive

`GET /api/company/drives/<drive_id>`

Auth: company, approved-only

Only returns drives owned by the logged-in company.

Success `200`: drive object.

Errors:

| Status | Response |
| --- | --- |
| 404 | `{ "error": "Failed to find drive with id <drive_id>" }` |

### Update Drive

`PUT /api/company/drives/<drive_id>`

Auth: company, approved-only

Approved or closed drives cannot be modified.

Allowed request fields are the same as create drive.

Success `200`:

```json
{
  "message": "Drive updated successfully",
  "drive": {}
}
```

Errors:

| Status | Response |
| --- | --- |
| 400 | `{ "error": "Request body is required" }` |
| 400 | `{ "error": "Field '<field>' cannot be updated" }` |
| 400 | `{ "error": "Invalid application_deadline format" }` |
| 404 | `{ "error": "Failed to find drive with id <drive_id>" }` |
| 409 | `{ "error": "Approved or closed drives cannot be modified" }` |

### Close Drive

`PUT /api/company/drives/<drive_id>/close`

Auth: company, approved-only

Success `200`:

```json
{
  "message": "Drive closed successfully",
  "drive_id": "uuid",
  "status": "closed"
}
```

Errors:

| Status | Response |
| --- | --- |
| 404 | `{ "error": "Drive not found" }` |
| 409 | `{ "error": "Drive is already closed" }` |

### List Drive Applications

`GET /api/company/drives/<drive_id>/applications`

Auth: company, approved-only

Only returns applications for a drive owned by the logged-in company.

Success `200`:

```json
{
  "drive_id": "uuid",
  "job_title": "Software Engineer",
  "required_skills": "Python",
  "experience_required": "0-1 years",
  "benefits": "Health insurance",
  "applications": [
    {
      "application_id": "uuid",
      "student_id": "uuid",
      "drive_id": "uuid",
      "status": "applied",
      "drive": {}
    }
  ]
}
```

### Update Application Status

`PUT /api/company/drives/<drive_id>/applications/<application_id>`

Auth: company, approved-only

Request for rejecting:

```json
{
  "status": "rejected",
  "remarks": "Does not match requirements"
}
```

Request for shortlisting:

```json
{
  "status": "shortlisted",
  "remarks": "Good profile",
  "interview_date": "2026-06-20T10:00:00",
  "interview_type": "online"
}
```

Request for selecting:

```json
{
  "status": "selected",
  "remarks": "Selected"
}
```

Rules:

- `status` must be one of `shortlisted`, `selected`, or `rejected`.
- Status cannot be changed back to `applied`.
- Shortlisted applications require `interview_date` and `interview_type`.
- Selecting an application creates a placement if one does not already exist.

Success `200`:

```json
{
  "message": "Application updated successfully",
  "application": {
    "application_id": "uuid",
    "status": "shortlisted",
    "remarks": "Good profile"
  }
}
```

Errors:

| Status | Response |
| --- | --- |
| 400 | `{ "error": "Request body is required" }` |
| 400 | `{ "error": "Invalid status" }` |
| 400 | `{ "error": "Cannot change status back to applied" }` |
| 400 | `{ "error": "Selected applications require interview details" }` |
| 404 | `{ "error": "Failed to find drive with id <drive_id>" }` |
| 404 | `{ "error": "Failed to find application with id <application_id>" }` |

Frontend note: the backend message says "Selected applications require interview details" while the check is for shortlisted applications.

### List Company Placements

`GET /api/company/placements`

Auth: company, approved-only

Success `200`:

```json
{
  "count": 1,
  "placements": [
    {
      "placement_id": "uuid",
      "student_name": "Student Name",
      "roll_no": "ROLL001",
      "job_title": "Software Engineer",
      "salary": 1200000,
      "joining_date": "2026-08-01 09:00:00",
      "offer_letter_uploaded": true,
      "created_at": "2026-06-15 10:00:00"
    }
  ]
}
```

### Update Placement

`PUT /api/company/placements/<placement_id>`

Auth: company, approved-only

Request:

```json
{
  "salary": 1200000,
  "joining_date": "2026-08-01T09:00:00"
}
```

Validation:

- `salary` is required and must be greater than `0`.
- `joining_date` is required and must be ISO format.

Success `200`:

```json
{
  "message": "Placement updated successfully",
  "placement": {
    "placement_id": "uuid",
    "application_id": "uuid",
    "student_name": "Student Name",
    "job_title": "Software Engineer",
    "salary": 1200000,
    "joining_date": "2026-08-01 09:00:00",
    "offer_letter_uploaded": false,
    "created_at": "2026-06-15 10:00:00"
  }
}
```

Errors:

| Status | Response |
| --- | --- |
| 400 | `{ "error": "Request body is required" }` |
| 400 | `{ "error": "salary is required" }` |
| 400 | `{ "error": "salary must be greater than 0" }` |
| 400 | `{ "error": "joining_date is required" }` |
| 400 | `{ "error": "Invalid joining_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)" }` |
| 404 | `{ "error": "Placement not found" }` |

### Upload Offer Letter

`POST /api/company/placements/<placement_id>/offer-letter`

Auth: company, approved-only

Content-Type: `multipart/form-data`

Form fields:

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `offer_letter` | file | Yes | Must be a PDF file. |

Success `200`:

```json
{
  "message": "Offer letter uploaded successfully",
  "placement_id": "uuid",
  "offer_letter_path": "/absolute/or/runtime/path/uploads/offer_letters/file.pdf"
}
```

Errors:

| Status | Response |
| --- | --- |
| 400 | `{ "error": "Offer letter file is required" }` |
| 400 | `{ "error": "Only PDF files are allowed" }` |
| 404 | `{ "error": "Placement not found" }` |

## Frontend Integration Notes

- Store the JWT from login and send it in the `Authorization` header for protected requests.
- Use `/api/auth/me` after app load to restore the current user and route them by role.
- Company users may register successfully but still receive `403 Company approval pending` until an admin approves them.
- Student dashboard and drive listing require a completed profile: `department`, `cgpa`, and `year`.
- Student apply requires a resume upload before submitting an application.
- File uploads must use `FormData`; do not send JSON for resume or offer letter uploads.
- Date/time inputs should send ISO strings such as `2026-07-01T23:59:00`.
- Backend date responses are plain stringified Python datetimes, usually like `YYYY-MM-DD HH:MM:SS`.
- `eligible_branch` should be sent as a comma-separated string, for example `CSE,ECE` or `ALL`.
- Some error responses use `message` instead of `error` for invalid fields. Frontend error handling should check both keys.
