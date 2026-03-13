import requests
import json
from typing import Optional, Dict, Any
from config import API_BASE_URL, API_TIMEOUT
from services.auth_service import AuthService

class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.timeout = API_TIMEOUT
        self.auth_service = AuthService()
    
    def _get_headers(self) -> Dict[str, str]:
        headers = {'Content-Type': 'application/json'}
        token = self.auth_service.get_token()
        if token:
            headers['Authorization'] = f'Bearer {token}'
        return headers
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        try:
            response = requests.get(
                f"{self.base_url}{endpoint}",
                headers=self._get_headers(),
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = requests.post(
                f"{self.base_url}{endpoint}",
                headers=self._get_headers(),
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = requests.put(
                f"{self.base_url}{endpoint}",
                headers=self._get_headers(),
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        try:
            response = requests.delete(
                f"{self.base_url}{endpoint}",
                headers=self._get_headers(),
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def upload_file(self, endpoint: str, file_path: str, additional_data: Optional[Dict] = None) -> Dict[str, Any]:
        try:
            headers = {'Authorization': f'Bearer {self.auth_service.get_token()}'}
            files = {'file': open(file_path, 'rb')}
            response = requests.post(
                f"{self.base_url}{endpoint}",
                headers=headers,
                files=files,
                data=additional_data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
