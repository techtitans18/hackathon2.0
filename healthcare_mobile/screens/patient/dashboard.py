from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from services.api_client import APIClient
from services.auth_service import AuthService
from utils.cache_manager import CacheManager

class PatientDashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_client = APIClient()
        self.auth_service = AuthService()
        self.cache_manager = CacheManager()
        self.dialog = None
    
    def on_enter(self):
        """Load patient data when screen is displayed"""
        user = self.auth_service.get_current_user()
        if user:
            self.ids.patient_name.text = user.get('name', 'Patient')
            health_id = user.get('health_id', 'Not Assigned')
            self.ids.health_id.text = f"Health ID: {health_id}"
            
            # Load patient statistics
            self.load_statistics()
    
    def load_statistics(self):
        """Load patient statistics from API"""
        try:
            response = self.api_client.get('/patient/me')
            
            if 'error' not in response:
                records = response.get('records', [])
                self.ids.total_records.text = str(len(records))
                
                # Count unique hospitals
                hospitals = set()
                for record in records:
                    hospital_id = record.get('hospital_id')
                    if hospital_id:
                        hospitals.add(hospital_id)
                
                self.ids.hospitals_visited.text = str(len(hospitals))
                
                # Show last activity
                if records:
                    last_record = records[0]
                    last_date = last_record.get('timestamp', 'Unknown')
                    self.ids.last_activity.text = f"Last record: {last_date[:10]}"
        except Exception as e:
            print(f"Error loading statistics: {e}")
    
    def open_menu(self):
        """Open navigation menu"""
        self.show_dialog("Menu", "Navigation menu coming soon!")
    
    def open_profile(self):
        """Open profile screen"""
        self.go_to_profile()
    
    def view_records(self):
        """Navigate to records screen"""
        self.manager.current = 'patient_records'
    
    def show_health_card(self):
        """Navigate to health card screen"""
        self.manager.current = 'health_card'
    
    def download_records(self):
        """Download records for offline access"""
        response = self.api_client.get('/patient/me')
        
        if 'error' in response:
            self.show_dialog("Error", response['error'])
            return
        
        # Cache records for offline access
        records = response.get('records', [])
        self.cache_manager.set('patient_records', records)
        self.show_dialog("Success", f"{len(records)} records downloaded for offline access")
    
    def go_to_profile(self):
        """Navigate to profile screen"""
        self.show_dialog("Profile", "Profile screen coming soon!")
    
    def logout(self):
        """Logout and return to login screen"""
        self.auth_service.clear_tokens()
        self.cache_manager.clear_all()
        self.manager.current = 'login'
    
    def show_dialog(self, title, message):
        """Show dialog with message"""
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()
