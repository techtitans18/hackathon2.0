from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from services.api_client import APIClient
from services.auth_service import AuthService

class HospitalDashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_client = APIClient()
        self.auth_service = AuthService()
        self.dialog = None
    
    def on_enter(self):
        user = self.auth_service.get_current_user()
        if user:
            self.ids.hospital_name.text = user.get('name', 'Hospital')
    
    def register_patient(self):
        self.manager.current = 'register_patient'
    
    def add_record(self):
        self.manager.current = 'add_record'
    
    def scan_qr(self):
        self.manager.current = 'qr_scanner'
    
    def emergency_access(self):
        self.manager.current = 'emergency_access'
    
    def view_patients(self):
        self.manager.current = 'hospital_patients'
    
    def logout(self):
        self.auth_service.clear_tokens()
        self.manager.current = 'login'
    
    def show_dialog(self, title, message):
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
