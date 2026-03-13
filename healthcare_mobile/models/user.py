from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: str
    email: str
    role: str
    name: str
    phone: Optional[str] = None
    hospital_id: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            email=data.get('email'),
            role=data.get('role'),
            name=data.get('name'),
            phone=data.get('phone'),
            hospital_id=data.get('hospital_id')
        )
