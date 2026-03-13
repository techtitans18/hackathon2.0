import re
from typing import Tuple

class Validator:
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True, ""
        return False, "Invalid email format"
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        pattern = r'^\+?1?\d{10,15}$'
        if re.match(pattern, phone.replace('-', '').replace(' ', '')):
            return True, ""
        return False, "Invalid phone number"
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain lowercase letter"
        if not re.search(r'\d', password):
            return False, "Password must contain a number"
        return True, ""
    
    @staticmethod
    def validate_otp(otp: str) -> Tuple[bool, str]:
        if len(otp) == 6 and otp.isdigit():
            return True, ""
        return False, "OTP must be 6 digits"
    
    @staticmethod
    def validate_required(value: str, field_name: str) -> Tuple[bool, str]:
        if value and value.strip():
            return True, ""
        return False, f"{field_name} is required"
