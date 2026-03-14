from kivymd.uix.screen import MDScreen
from services.api_client import APIClient
from services.auth_service import AuthService

class AdminDashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_client = APIClient()
        self.auth_service = AuthService()
    
    def on_enter(self):
        self.load_statistics()
    
    def load_statistics(self):
        users_resp = self.api_client.get('/admin/users')
        hospitals_resp = self.api_client.get('/hospitals')
        blockchain_resp = self.api_client.get('/blockchain')

        users = users_resp.get('users', []) if 'error' not in users_resp else []
        hospitals = hospitals_resp.get('hospitals', []) if 'error' not in hospitals_resp else []
        patients = [u for u in users if u.get('role') == 'patient']
        blocks = blockchain_resp.get('length', 0) if 'error' not in blockchain_resp else 0

        self.ids.stats_text.text = (
            f"Total Users: {len(users)}\n"
            f"Total Hospitals: {len(hospitals)}\n"
            f"Total Patients: {len(patients)}\n"
            f"Blockchain Blocks: {blocks}"
        )
    
    def manage_users(self):
        self.manager.current = 'user_management'
    
    def manage_hospitals(self):
        self.manager.current = 'hospital_management'
    
    def view_blockchain(self):
        self.manager.current = 'blockchain_viewer'
    
    def view_logs(self):
        self.manager.current = 'system_logs'
    
    def logout(self):
        self.auth_service.clear_tokens()
        self.manager.current = 'login'
