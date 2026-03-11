# Healthcare Blockchain - Complete Project Documentation
## From Scratch to Production

---

# 📋 TABLE OF CONTENTS

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [System Architecture](#system-architecture)
4. [Installation & Setup](#installation--setup)
5. [Database Design](#database-design)
6. [Backend Implementation](#backend-implementation)
7. [Frontend Implementation](#frontend-implementation)
8. [Authentication System](#authentication-system)
9. [Blockchain Implementation](#blockchain-implementation)
10. [AI Summarization](#ai-summarization)
11. [Emergency Access System](#emergency-access-system)
12. [API Documentation](#api-documentation)
13. [Security Features](#security-features)
14. [Complete Workflow](#complete-workflow)
15. [Testing Guide](#testing-guide)
16. [Deployment](#deployment)
17. [Troubleshooting](#troubleshooting)

---

# 1. PROJECT OVERVIEW

## What is This System?

A **blockchain-based healthcare records management system** that:
- Stores medical records securely
- Uses blockchain for data integrity
- Provides AI-powered medical summaries
- Enables emergency access to critical patient data
- Implements role-based access control

## Key Features

1. **Blockchain Integrity** - Tamper-proof medical records
2. **AI Summarization** - Automatic report summaries
3. **Emergency Access** - Quick patient lookup in emergencies
4. **Role-Based Access** - Admin, Hospital, Patient, Doctor, Emergency
5. **Google OAuth** - Secure authentication
6. **Local Storage** - Privacy-first file storage
7. **E-Health Card** - Digital patient ID
8. **Audit Logging** - Complete access tracking

## Problem It Solves

- ❌ Medical records easily tampered
- ❌ Long reports hard to understand
- ❌ Emergency access too slow
- ❌ No unified patient ID system
- ❌ Privacy concerns with cloud storage

## Solution

- ✅ Blockchain ensures data integrity
- ✅ AI generates quick summaries
- ✅ Emergency dashboard for fast access
- ✅ Deterministic HealthID generation
- ✅ Local file storage, no cloud

---

# 2. TECHNOLOGY STACK

## Backend Technologies

### Core Framework
- **FastAPI** (Python 3.10+)
  - Modern async web framework
  - Automatic API documentation
  - High performance
  - Type hints support

### Database
- **MongoDB** (NoSQL)
  - Flexible schema
  - Horizontal scaling
  - Document-based storage
  - Fast queries

### Authentication
- **Google OAuth 2.0**
  - Secure login
  - No password management
  - Email verification
  - JWT tokens

### AI/ML
- **Transformers** (HuggingFace)
  - BART model for summarization
  - PyTorch backend
  - Offline processing
  - 1.6GB model size

### Python Libraries
```txt
fastapi==0.104.1          # Web framework
uvicorn==0.24.0           # ASGI server
pymongo==4.6.0            # MongoDB driver
python-multipart==0.0.6   # File uploads
python-dotenv==1.0.0      # Environment variables
google-auth==2.23.4       # Google OAuth
requests==2.31.0          # HTTP client
transformers==4.35.2      # AI models
torch==2.1.1              # Deep learning
sentencepiece==0.1.99     # Tokenization
```

## Frontend Technologies

### Core Framework
- **React 19.2.0**
  - Component-based UI
  - Virtual DOM
  - Hooks for state management
  - Fast rendering

### Build Tool
- **Vite 7.3.1**
  - Lightning-fast HMR
  - Optimized builds
  - ES modules
  - Dev server

### Routing
- **React Router DOM 7.13.1**
  - Client-side routing
  - Nested routes
  - Navigation guards
  - URL parameters

### HTTP Client
- **Axios 1.6.0**
  - Promise-based
  - Interceptors
  - Request/response transformation
  - Error handling

### Authentication
- **@react-oauth/google 0.13.4**
  - Google Sign-In button
  - Credential handling
  - Token management

### Node Packages
```json
{
  "react": "^19.2.0",
  "react-dom": "^19.2.0",
  "react-router-dom": "^7.13.1",
  "axios": "^1.6.0",
  "@react-oauth/google": "^0.13.4",
  "vite": "^7.3.1"
}
```

## Development Tools

- **ESLint** - Code linting
- **Git** - Version control
- **VS Code** - IDE
- **Postman** - API testing

---

# 3. SYSTEM ARCHITECTURE

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER BROWSER                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │         React Frontend (Port 5173)               │  │
│  │  - Login Page                                    │  │
│  │  - Admin Dashboard                               │  │
│  │  - Hospital Dashboard                            │  │
│  │  - Patient Dashboard                             │  │
│  │  - Emergency Dashboard                           │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                         ↓ HTTP/HTTPS
                    (Axios API Calls)
                         ↓
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend (Port 8000)                │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Authentication Layer (Google OAuth + JWT)       │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  API Routes                                      │  │
│  │  - /auth/*        - Authentication               │  │
│  │  - /admin/*       - Admin operations             │  │
│  │  - /register_*    - Registration                 │  │
│  │  - /patient/*     - Patient data                 │  │
│  │  - /record/*      - Medical records              │  │
│  │  - /ai/*          - AI summaries                 │  │
│  │  - /emergency/*   - Emergency access             │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Business Logic                                  │  │
│  │  - Blockchain (SHA-256 hashing)                  │  │
│  │  - AI Summarizer (BART model)                    │  │
│  │  - File Storage (Local filesystem)               │  │
│  │  - Access Control (RBAC)                         │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                         ↓
        ┌────────────────┴────────────────┐
        ↓                                  ↓
┌──────────────────┐            ┌──────────────────┐
│   MongoDB        │            │  Local Storage   │
│   (Database)     │            │  (records/)      │
│                  │            │                  │
│  - patients      │            │  - PDF files     │
│  - hospitals     │            │  - Images        │
│  - records       │            │  - Summaries     │
│  - users         │            │                  │
│  - emergency_*   │            └──────────────────┘
└──────────────────┘
```

## Request Flow Example

```
1. User clicks "Login with Google"
   ↓
2. Google OAuth popup opens
   ↓
3. User authenticates with Google
   ↓
4. Google returns credential token
   ↓
5. Frontend sends token to /auth/google
   ↓
6. Backend verifies with Google API
   ↓
7. Backend checks user in MongoDB
   ↓
8. Backend generates JWT token
   ↓
9. Frontend stores JWT in localStorage
   ↓
10. All subsequent requests include JWT
    ↓
11. Backend validates JWT on each request
    ↓
12. Backend checks user role & permissions
    ↓
13. Backend processes request
    ↓
14. Backend returns response
    ↓
15. Frontend displays data
```

## Component Interaction

```
┌─────────────┐
│   Admin     │
└──────┬──────┘
       │ Creates
       ↓
┌─────────────┐     Registers      ┌─────────────┐
│  Hospital   │ ─────────────────→ │   Patient   │
└──────┬──────┘                    └──────┬──────┘
       │                                  │
       │ Uploads                          │ Views
       ↓                                  ↓
┌─────────────────────────────────────────────┐
│         Medical Record + Blockchain         │
│  ┌────────────┐  ┌────────────┐            │
│  │ File (.pdf)│  │ AI Summary │            │
│  └────────────┘  └────────────┘            │
│  ┌────────────────────────────┐            │
│  │  Blockchain Block          │            │
│  │  - Hash of file            │            │
│  │  - Previous block hash     │            │
│  └────────────────────────────┘            │
└─────────────────────────────────────────────┘
       ↑
       │ Emergency Access
       │
┌──────┴──────┐
│  Emergency  │
│   Staff     │
└─────────────┘
```

---

# 4. INSTALLATION & SETUP

## Prerequisites

### System Requirements
- **OS:** Windows 10/11, Linux, macOS
- **RAM:** 4GB minimum (8GB recommended for AI)
- **Storage:** 5GB free space
- **Python:** 3.10 or higher
- **Node.js:** 18.0 or higher
- **MongoDB:** 6.0 or higher

### Software Installation

#### 1. Install Python
```bash
# Windows
Download from python.org

# Linux
sudo apt install python3.10 python3-pip

# macOS
brew install python@3.10
```

#### 2. Install Node.js
```bash
# Windows
Download from nodejs.org

# Linux
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs

# macOS
brew install node
```

#### 3. Install MongoDB
```bash
# Windows
Download from mongodb.com

# Linux
sudo apt install mongodb

# macOS
brew install mongodb-community
```

## Project Setup

### Step 1: Clone/Create Project
```bash
mkdir healthcare_blockchain
cd healthcare_blockchain
```

### Step 2: Backend Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn pymongo python-multipart python-dotenv google-auth requests transformers torch sentencepiece
```

### Step 3: Frontend Setup
```bash
cd frontend
npm install
```

### Step 4: Environment Configuration
```bash
# Create .env file in root
touch .env
```

Edit `.env`:
```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=healthcare_blockchain
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
AUTH_SECRET_KEY=your-64-character-random-secret-key-here-make-it-long
ADMIN_BOOTSTRAP_EMAILS=admin@example.com
AI_SUMMARY_MODEL_DIR=models/ai_summary/facebook-bart-large-cnn
AI_SUMMARY_OFFLINE_MODE=1
```

### Step 5: Google OAuth Setup
1. Go to https://console.cloud.google.com
2. Create new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized origins: `http://localhost:5173`
6. Add authorized redirect: `http://localhost:5173`
7. Copy Client ID to `.env`

### Step 6: Download AI Model
```bash
# Create model directory
mkdir -p models/ai_summary

# Download model (requires internet)
python -c "from transformers import pipeline; pipeline('summarization', model='facebook/bart-large-cnn')"

# Or manually download from HuggingFace
```

### Step 7: Start MongoDB
```bash
# Windows
net start MongoDB

# Linux
sudo systemctl start mongodb

# macOS
brew services start mongodb-community
```

### Step 8: Initialize Database
```bash
# Backend will auto-create indexes on first run
python main.py
```

---

# 5. DATABASE DESIGN

## MongoDB Collections

### Collection: `patients`
```javascript
{
  _id: ObjectId("..."),
  health_id: "A1B2C3D4E5F6G7H8",  // SHA256(email|dob)[:16]
  name: "John Doe",
  age: 35,
  phone: "1234567890",
  email: "john@example.com",
  dob: "1989-05-15",              // YYYY-MM-DD
  blood_group: "O+",               // A+, A-, B+, B-, AB+, AB-, O+, O-
  photo_url: "data:image/jpeg;base64,...",  // Base64 image
  created_at: ISODate("2024-01-15T10:30:00Z"),
  created_by_hospital_id: "HOSP123ABC",
  updated_at: ISODate("2024-01-15T10:30:00Z")
}
```

**Indexes:**
- `health_id` (unique)
- `phone`
- `email` (unique, sparse)
- `name + dob` (compound)

### Collection: `hospitals`
```javascript
{
  _id: ObjectId("..."),
  hospital_id: "HOSP123ABC",      // SHA256(name|type)[:16]
  hospital_name: "City General Hospital",
  hospital_type: "General",        // General, Specialty, Emergency
  created_at: ISODate("2024-01-15T10:00:00Z")
}
```

**Indexes:**
- `hospital_id` (unique)

### Collection: `records`
```javascript
{
  _id: ObjectId("..."),
  health_id: "A1B2C3D4E5F6G7H8",
  hospital_id: "HOSP123ABC",
  record_type: "X-Ray",
  description: "Chest X-Ray findings...",
  file_name: "xray.pdf",
  stored_file_name: "uuid-123_xray.pdf",
  file_path: "records/uuid-123_xray.pdf",
  summary_file_name: "xray_ai_summary.txt",
  summary_stored_file_name: "uuid-456_xray_ai_summary.txt",
  summary_file_path: "records/uuid-456_xray_ai_summary.txt",
  record_hash: "sha256_hash_of_file",
  timestamp: ISODate("2024-01-15T11:00:00Z")
}
```

**Indexes:**
- `health_id + timestamp` (compound, descending)
- `stored_file_name` (unique)

### Collection: `users`
```javascript
{
  _id: ObjectId("..."),
  email: "user@example.com",
  subject: "google_oauth_sub_123",
  name: "User Name",
  picture: "https://google.com/photo.jpg",
  role: "hospital",               // admin, hospital, patient, doctor, emergency
  health_id: null,                // Only for patients
  hospital_id: "HOSP123ABC",      // Only for hospitals
  is_active: true,
  created_at: ISODate("2024-01-15T09:00:00Z"),
  updated_at: ISODate("2024-01-15T09:00:00Z"),
  last_login_at: ISODate("2024-01-15T10:00:00Z")
}
```

**Indexes:**
- `email` (unique)
- `health_id` (unique, sparse)
- `hospital_id` (unique, sparse)
- `role + is_active` (compound)

### Collection: `emergency_data`
```javascript
{
  _id: ObjectId("..."),
  health_id: "A1B2C3D4E5F6G7H8",
  blood_group: "O+",
  allergies: ["Penicillin", "Peanuts"],
  diseases: ["Diabetes", "Hypertension"],
  surgeries: ["Appendectomy", "Knee Surgery"],
  emergency_contact: "9876543210",
  blockchain_hash: "sha256_hash",  // For integrity verification
  created_at: ISODate("2024-01-15T10:30:00Z"),
  updated_at: ISODate("2024-01-15T10:30:00Z")
}
```

**Indexes:**
- `health_id` (unique)

### Collection: `emergency_logs`
```javascript
{
  _id: ObjectId("..."),
  hospital_id: "HOSP123ABC",
  health_id: "A1B2C3D4E5F6G7H8",
  timestamp: ISODate("2024-01-15T12:00:00Z"),
  action: "Emergency Access"
}
```

**Indexes:**
- `health_id + timestamp` (compound, descending)
- `hospital_id + timestamp` (compound, descending)

## Database Relationships

```
users (email) ──→ patients (email)
users (hospital_id) ──→ hospitals (hospital_id)
patients (health_id) ──→ records (health_id)
hospitals (hospital_id) ──→ records (hospital_id)
patients (health_id) ──→ emergency_data (health_id)
emergency_logs (health_id) ──→ patients (health_id)
```

---

*[Document continues with remaining sections 6-17...]*

**Note:** This is Part 1 of the complete documentation. The file is being created with all sections. Would you like me to continue with the remaining sections?
