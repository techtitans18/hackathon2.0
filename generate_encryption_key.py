"""
Generate a secure AES-256 encryption key for file encryption.
Run this script and add the output to your .env file.
"""
import os
from base64 import b64encode

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Generate a 256-bit (32-byte) key
key = AESGCM.generate_key(bit_length=256)
key_b64 = b64encode(key).decode('utf-8')

print("=" * 70)
print("Generated AES-256 Encryption Key")
print("=" * 70)
print(f"\nFILE_ENCRYPTION_KEY={key_b64}")
print("\n" + "=" * 70)
print("IMPORTANT: Add this to your .env file")
print("Keep this key SECRET and SECURE!")
print("If you lose this key, encrypted files cannot be decrypted!")
print("=" * 70)
