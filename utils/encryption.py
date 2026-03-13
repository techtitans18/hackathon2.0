"""
File encryption utilities for secure medical record storage and transfer.
Uses AES-256-GCM for authenticated encryption.
"""
from __future__ import annotations

import os
from base64 import b64decode, b64encode
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

BASE_DIR = Path(__file__).resolve().parent.parent
if load_dotenv is not None:
    load_dotenv(BASE_DIR / ".env", override=False)

# Get encryption key from environment or generate one
ENCRYPTION_KEY_B64 = os.getenv("FILE_ENCRYPTION_KEY")

if not ENCRYPTION_KEY_B64:
    # Generate a new key if not configured (for development only)
    new_key = AESGCM.generate_key(bit_length=256)
    ENCRYPTION_KEY_B64 = b64encode(new_key).decode('utf-8')
    print(f"WARNING: No FILE_ENCRYPTION_KEY found. Generated temporary key: {ENCRYPTION_KEY_B64}")
    print("Add this to your .env file: FILE_ENCRYPTION_KEY=" + ENCRYPTION_KEY_B64)

ENCRYPTION_KEY = b64decode(ENCRYPTION_KEY_B64)


def encrypt_file(file_content: bytes) -> bytes:
    """
    Encrypt file content using AES-256-GCM.
    
    Returns: nonce (12 bytes) + ciphertext + auth_tag (16 bytes)
    """
    aesgcm = AESGCM(ENCRYPTION_KEY)
    nonce = os.urandom(12)  # 96-bit nonce for GCM
    ciphertext = aesgcm.encrypt(nonce, file_content, None)
    return nonce + ciphertext


def decrypt_file(encrypted_content: bytes) -> bytes:
    """
    Decrypt file content using AES-256-GCM.
    
    Expects: nonce (12 bytes) + ciphertext + auth_tag (16 bytes)
    """
    aesgcm = AESGCM(ENCRYPTION_KEY)
    nonce = encrypted_content[:12]
    ciphertext = encrypted_content[12:]
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext


def encrypt_file_to_base64(file_content: bytes) -> str:
    """Encrypt and encode to base64 for JSON transfer."""
    encrypted = encrypt_file(file_content)
    return b64encode(encrypted).decode('utf-8')


def decrypt_file_from_base64(encrypted_b64: str) -> bytes:
    """Decode from base64 and decrypt."""
    encrypted = b64decode(encrypted_b64)
    return decrypt_file(encrypted)
