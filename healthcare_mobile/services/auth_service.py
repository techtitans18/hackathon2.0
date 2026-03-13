import keyring
import jwt
from datetime import datetime
from typing import Optional, Dict
from config import TOKEN_KEY, REFRESH_TOKEN_KEY

class AuthService:
    SERVICE_NAME = 'HealthcareApp'
    
    def __init__(self):
        self.current_user = None
    
    def save_token(self, token: str, refresh_token: Optional[str] = None):
        try:
            keyring.set_password(self.SERVICE_NAME, TOKEN_KEY, token)
            if refresh_token:
                keyring.set_password(self.SERVICE_NAME, REFRESH_TOKEN_KEY, refresh_token)
        except Exception as e:
            print(f"Error saving token: {e}")
    
    def get_token(self) -> Optional[str]:
        try:
            return keyring.get_password(self.SERVICE_NAME, TOKEN_KEY)
        except Exception as e:
            print(f"Error getting token: {e}")
            return None
    
    def get_refresh_token(self) -> Optional[str]:
        try:
            return keyring.get_password(self.SERVICE_NAME, REFRESH_TOKEN_KEY)
        except Exception as e:
            print(f"Error getting refresh token: {e}")
            return None
    
    def clear_tokens(self):
        try:
            keyring.delete_password(self.SERVICE_NAME, TOKEN_KEY)
            keyring.delete_password(self.SERVICE_NAME, REFRESH_TOKEN_KEY)
        except Exception:
            pass
        self.current_user = None
    
    def decode_token(self, token: str) -> Optional[Dict]:
        try:
            return jwt.decode(token, options={"verify_signature": False})
        except Exception as e:
            print(f"Error decoding token: {e}")
            return None
    
    def is_token_valid(self) -> bool:
        token = self.get_token()
        if not token:
            return False
        
        decoded = self.decode_token(token)
        if not decoded:
            return False
        
        exp = decoded.get('exp')
        if not exp:
            return False
        
        return datetime.fromtimestamp(exp) > datetime.now()
    
    def get_user_role(self) -> Optional[str]:
        token = self.get_token()
        if not token:
            return None
        
        decoded = self.decode_token(token)
        return decoded.get('role') if decoded else None
    
    def set_current_user(self, user_data: Dict):
        self.current_user = user_data
    
    def get_current_user(self) -> Optional[Dict]:
        return self.current_user
