# API Integration Guide

## Base URL
```
Production: https://api.healthcare.com/api
Development: http://localhost:8000/api
```

## Authentication

All authenticated requests require Bearer token in header:
```
Authorization: Bearer <access_token>
```

## Endpoints

### Authentication

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

Response:
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "user": {
    "id": "123",
    "email": "user@example.com",
    "role": "patient",
    "name": "John Doe"
  }
}
```

#### Refresh Token
```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ..."
}

Response:
{
  "access_token": "eyJ..."
}
```

### Patient Endpoints

#### Get Medical Records
```http
GET /patient/records
Authorization: Bearer <token>

Response:
{
  "records": [
    {
      "id": "rec123",
      "patient_id": "pat123",
      "hospital_id": "hosp123",
      "diagnosis": "Common cold",
      "treatment": "Rest and fluids",
      "date": "2024-01-15",
      "doctor_name": "Dr. Smith",
      "files": ["file1.pdf", "file2.jpg"]
    }
  ]
}
```

#### Get Patient Profile
```http
GET /patient/profile
Authorization: Bearer <token>

Response:
{
  "id": "pat123",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "date_of_birth": "1990-01-01",
  "blood_group": "O+",
  "address": "123 Main St"
}
```

### Hospital Endpoints

#### Register Patient
```http
POST /hospital/patients
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "+1234567890",
  "date_of_birth": "1995-05-15",
  "blood_group": "A+"
}

Response:
{
  "patient_id": "pat456",
  "message": "Patient registered successfully"
}
```

#### Add Medical Record
```http
POST /hospital/records
Authorization: Bearer <token>
Content-Type: multipart/form-data

patient_id: pat123
diagnosis: Flu
treatment: Antiviral medication
doctor_name: Dr. Johnson
date: 2024-01-20
file: <binary>

Response:
{
  "record_id": "rec456",
  "message": "Record added successfully"
}
```

#### List Patients
```http
GET /hospital/patients
Authorization: Bearer <token>

Response:
{
  "patients": [
    {
      "id": "pat123",
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1234567890"
    }
  ]
}
```

### Admin Endpoints

#### List Users
```http
GET /admin/users
Authorization: Bearer <token>

Response:
{
  "users": [
    {
      "id": "user123",
      "name": "John Doe",
      "email": "john@example.com",
      "role": "patient",
      "status": "active"
    }
  ]
}
```

#### List Hospitals
```http
GET /admin/hospitals
Authorization: Bearer <token>

Response:
{
  "hospitals": [
    {
      "id": "hosp123",
      "name": "City Hospital",
      "address": "456 Health Ave",
      "phone": "+1234567890",
      "email": "info@cityhospital.com",
      "license_number": "LIC123456"
    }
  ]
}
```

#### System Statistics
```http
GET /admin/statistics
Authorization: Bearer <token>

Response:
{
  "statistics": {
    "total_users": 1500,
    "total_hospitals": 50,
    "total_patients": 1200,
    "total_records": 5000
  }
}
```

## Error Responses

All errors follow this format:
```json
{
  "error": "Error message description"
}
```

Common HTTP status codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Rate Limiting

- 100 requests per minute per user
- 1000 requests per hour per user

## File Upload

Maximum file size: 10MB
Supported formats: PDF, JPG, PNG, DOCX
