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
        response = self.api_client.get('/admin/statistics')
        
        if 'error' not in response:
            stats = response.get('statistics', {})
            stats_text = f"""
Total Users: {stats.get('total_users', 0)}
Total Hospitals: {stats.get('total_hospitals', 0)}
Total Patients: {stats.get('total_patients', 0)}
Total Records: {stats.get('total_records', 0)}
            """
            self.ids.stats_text.text = stats_text.strip()
    
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
