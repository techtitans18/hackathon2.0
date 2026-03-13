from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os

class EncryptionService:
    def __init__(self, password: str = None):
        self.password = password or os.urandom(32).hex()
        self.key = self._generate_key()
        self.cipher = Fernet(self.key)
    
    def _generate_key(self) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'healthcare_salt',
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password.encode()))
        return key
    
    def encrypt_file(self, file_path: str, output_path: str = None) -> str:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        encrypted_data = self.cipher.encrypt(data)
        
        output_path = output_path or f"{file_path}.encrypted"
        with open(output_path, 'wb') as f:
            f.write(encrypted_data)
        
        return output_path
    
    def decrypt_file(self, encrypted_path: str, output_path: str = None) -> str:
        with open(encrypted_path, 'rb') as f:
            encrypted_data = f.read()
        
        decrypted_data = self.cipher.decrypt(encrypted_data)
        
        output_path = output_path or encrypted_path.replace('.encrypted', '')
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
        
        return output_path
    
    def encrypt_text(self, text: str) -> str:
        return self.cipher.encrypt(text.encode()).decode()
    
    def decrypt_text(self, encrypted_text: str) -> str:
        return self.cipher.decrypt(encrypted_text.encode()).decode()
