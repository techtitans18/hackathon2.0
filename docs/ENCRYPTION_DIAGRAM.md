# File Encryption Visual Structure

## Encrypted File Binary Structure

```
Byte Position:    0                    12                                    N-16              N
                  ↓                    ↓                                     ↓                 ↓
                  ┌────────────────────┬─────────────────────────────────────┬─────────────────┐
Encrypted File:   │   Nonce (12 B)    │      Ciphertext (Variable)          │  Auth Tag (16 B)│
                  └────────────────────┴─────────────────────────────────────┴─────────────────┘
                   Random IV            Encrypted Medical Data                 Integrity Check
                   (Never reused)       (Unreadable without key)              (Tamper detection)
```

## Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           HOSPITAL UPLOADS FILE                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        ↓
                    ┌───────────────────────────────────┐
                    │   Original Medical File           │
                    │   report.pdf                      │
                    │   [Plain Text - Readable]         │
                    └───────────────────────────────────┘
                                        ↓
                    ┌───────────────────────────────────┐
                    │   Calculate SHA-256 Hash          │
                    │   record_hash = SHA256(file)      │
                    │   Used for blockchain integrity   │
                    └───────────────────────────────────┘
                                        ↓
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         ENCRYPTION PROCESS (Server-Side)                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  Step 1: Load Encryption Key                                                    │
│  ┌────────────────────────────────────────────────────────────┐                │
│  │  .env file                                                  │                │
│  │  FILE_ENCRYPTION_KEY=Xj8kL2mP9qR5sT7vW0yZ3aB6cD8eF1g...    │                │
│  │  (Base64-encoded 32-byte key)                              │                │
│  └────────────────────────────────────────────────────────────┘                │
│                           ↓                                                      │
│  Step 2: Generate Random Nonce                                                  │
│  ┌────────────────────────────────────────────────────────────┐                │
│  │  nonce = os.urandom(12)                                    │                │
│  │  Result: b'\x8a\x3f\x7c\x2e\x9d\x1b\x4f\x6a\x8c\x5e\x3d\x7f'│                │
│  │  (12 random bytes - unique for this file)                 │                │
│  └────────────────────────────────────────────────────────────┘                │
│                           ↓                                                      │
│  Step 3: Encrypt with AES-256-GCM                                               │
│  ┌────────────────────────────────────────────────────────────┐                │
│  │  Input:  Plain file (100 KB)                              │                │
│  │  Key:    256-bit encryption key                           │                │
│  │  Nonce:  12-byte random IV                                │                │
│  │  ────────────────────────────────────────────────────────  │                │
│  │  Output: Ciphertext (100 KB) + Auth Tag (16 bytes)       │                │
│  └────────────────────────────────────────────────────────────┘                │
│                           ↓                                                      │
│  Step 4: Combine Components                                                     │
│  ┌────────────────────────────────────────────────────────────┐                │
│  │  encrypted_file = nonce + ciphertext + tag                │                │
│  │  Total size: 12 + 100,000 + 16 = 100,028 bytes           │                │
│  └────────────────────────────────────────────────────────────┘                │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        ↓
                    ┌───────────────────────────────────┐
                    │   Save to Disk                    │
                    │   records/uuid_report.pdf         │
                    │   [Encrypted - Unreadable]        │
                    └───────────────────────────────────┘
                                        ↓
                    ┌───────────────────────────────────┐
                    │   Store Metadata in MongoDB       │
                    │   - health_id                     │
                    │   - hospital_id                   │
                    │   - stored_file_name              │
                    │   - record_hash (SHA-256)         │
                    └───────────────────────────────────┘
                                        ↓
                    ┌───────────────────────────────────┐
                    │   Add Block to Blockchain         │
                    │   - HealthID                      │
                    │   - HospitalID                    │
                    │   - RecordHash                    │
                    │   - Timestamp                     │
                    └───────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────────┐
│                        PATIENT/ADMIN DOWNLOADS FILE                              │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        ↓
                    ┌───────────────────────────────────┐
                    │   Verify User Permissions         │
                    │   - Check JWT token               │
                    │   - Verify role (admin/patient)   │
                    │   - Check HealthID match          │
                    └───────────────────────────────────┘
                                        ↓
                    ┌───────────────────────────────────┐
                    │   Read Encrypted File from Disk   │
                    │   records/uuid_report.pdf         │
                    │   [Encrypted - Unreadable]        │
                    └───────────────────────────────────┘
                                        ↓
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         DECRYPTION PROCESS (Server-Side)                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Step 1: Load Encryption Key                                                    │
│  ┌────────────────────────────────────────────────────────────┐                 │
│  │  .env file                                                 │                 │
│  │  FILE_ENCRYPTION_KEY=Xj8kL2mP9qR5sT7vW0yZ3aB6cD8eF1g...    │                 │
│  │  (Same key used for encryption)                            │                 │
│  └────────────────────────────────────────────────────────────┘                 │
│                           ↓                                                     │
│  Step 2: Parse Encrypted File                                                   │
│  ┌────────────────────────────────────────────────────────────┐                │
│  │  encrypted_bytes = file.read_bytes()                       │                │
│  │  nonce = encrypted_bytes[:12]                              │                │
│  │  ciphertext = encrypted_bytes[12:]  (includes auth tag)    │                │
│  └────────────────────────────────────────────────────────────┘                │
│                           ↓                                                    │
│  Step 3: Decrypt with AES-256-GCM                                              │
│  ┌────────────────────────────────────────────────────────────┐                │
│  │  Input:  Ciphertext (100 KB) + Auth Tag (16 bytes)         │                │
│  │  Key:    256-bit encryption key (same as encryption)       │                │
│  │  Nonce:  12-byte IV (extracted from file)                  │                │
│  │  ────────────────────────────────────────────────────────  │                │
│  │  Process:                                                  │                │
│  │  1. Verify authentication tag (detect tampering)           │                │
│  │  2. Decrypt ciphertext to plaintext                        │                │
│  │  ────────────────────────────────────────────────────────  │                │
│  │  Output: Original file (100 KB) [Plain Text]               │                │
│  └────────────────────────────────────────────────────────────┘                │
│                           ↓                                                    │
│  Step 4: Write to Temporary File                                               │
│  ┌────────────────────────────────────────────────────────────┐                │
│  │  temp_file = records/temp_uuid_report.pdf                  │                │
│  │  temp_file.write_bytes(plaintext)                          │                │
│  │  [Plain Text - Readable]                                   │                │
│  └────────────────────────────────────────────────────────────┘                │
│                                                                                │
└────────────────────────────────────────────────────────────────────────────────┘
                                        ↓
                    ┌───────────────────────────────────┐
                    │   Send File to User               │
                    │   HTTP FileResponse               │
                    │   Content-Type: application/pdf   │
                    │   [Plain Text - Readable]         │
                    └───────────────────────────────────┘
                                        ↓
                    ┌───────────────────────────────────┐
                    │   Clean Up Temporary File         │
                    │   Delete temp_uuid_report.pdf     │
                    │   (After response sent)           │
                    └───────────────────────────────────┘
                                        ↓
                    ┌───────────────────────────────────┐
                    │   User Downloads Original File    │
                    │   report.pdf (100 KB)             │
                    │   [Plain Text - Readable]         │
                    └───────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════════

## Storage Comparison

### WITHOUT Encryption (OLD - INSECURE)
```
records/
├── uuid1_report.pdf          ← Plain text (anyone can read)
├── uuid2_xray.jpg            ← Plain text (anyone can read)
└── uuid3_summary.txt         ← Plain text (anyone can read)

Risk: File system access = full data breach
```

### WITH Encryption (NEW - SECURE)
```
records/
├── uuid1_report.pdf          ← Encrypted (unreadable without key)
├── uuid2_xray.jpg            ← Encrypted (unreadable without key)
└── uuid3_summary.txt         ← Encrypted (unreadable without key)

Protection: File system access = encrypted gibberish
```

## Key Security Model

```
┌─────────────────────────────────────────────────────────────────┐
│                    Encryption Key Hierarchy                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Master Key (FILE_ENCRYPTION_KEY)                               │
│  ┌────────────────────────────────────────────────────┐         │
│  │  - Stored in .env file (server only)               │         │
│  │  - 256-bit (32 bytes) random key                   │         │
│  │  - Base64-encoded for storage                      │         │
│  │  - Never transmitted over network                  │         │
│  │  - Never stored in database                        │         │
│  │  - Never logged or displayed                       │         │
│  └────────────────────────────────────────────────────┘         │
│                           ↓                                      │
│  Per-File Nonce (Random IV)                                     │
│  ┌────────────────────────────────────────────────────┐         │
│  │  - Generated for each file encryption              │         │
│  │  - 96-bit (12 bytes) random value                  │         │
│  │  - Stored with encrypted file                      │         │
│  │  - Ensures unique ciphertext per file              │         │
│  │  - Safe to store publicly                          │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Attack Resistance

```
┌──────────────────────────────────────────────────────────────────┐
│                      Threat Model                                 │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ❌ Attacker gains file system access                            │
│     → Files are encrypted (unreadable)                           │
│     → Needs encryption key to decrypt                            │
│                                                                   │
│  ❌ Attacker steals database backup                              │
│     → Metadata only (no file content)                            │
│     → Encrypted files stored separately                          │
│                                                                   │
│  ❌ Attacker intercepts network traffic                          │
│     → HTTPS encrypts transmission (production)                   │
│     → JWT tokens expire after session                            │
│                                                                   │
│  ❌ Attacker modifies encrypted file                             │
│     → Authentication tag verification fails                      │
│     → Decryption throws error                                    │
│     → Tampering detected                                         │
│                                                                   │
│  ❌ Attacker tries brute force                                   │
│     → AES-256: 2^256 possible keys                               │
│     → Would take billions of years                               │
│                                                                   │
│  ✅ Authorized user with valid JWT                               │
│     → Server decrypts file                                       │
│     → User receives original file                                │
│     → Access logged in blockchain                                │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

## Performance Metrics

```
┌─────────────────────────────────────────────────────────────────┐
│              Encryption Performance (Typical)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  File Size    │ Encrypt Time │ Decrypt Time │ Storage Overhead │
│  ────────────────────────────────────────────────────────────── │
│  100 KB       │    ~1 ms     │    ~1 ms     │    +28 bytes     │
│  1 MB         │    ~5 ms     │    ~5 ms     │    +28 bytes     │
│  10 MB        │   ~50 ms     │   ~50 ms     │    +28 bytes     │
│  100 MB       │  ~500 ms     │  ~500 ms     │    +28 bytes     │
│                                                                  │
│  CPU Usage: 5-10% (hardware-accelerated AES)                    │
│  Memory: Minimal (streaming possible)                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

This encryption structure ensures that all medical files are protected at rest and only accessible to authorized users through proper authentication and decryption.
