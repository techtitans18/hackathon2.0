from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from services.api_client import APIClient
from services.auth_service import AuthService
from utils.validators import Validator

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_client = APIClient()
        self.auth_service = AuthService()
        self.dialog = None
    
    def on_login(self):
        email = self.ids.email_field.text
        password = self.ids.password_field.text
        
        # Validate inputs
        is_valid, error = Validator.validate_email(email)
        if not is_valid:
            self.show_error(error)
            return
        
        is_valid, error = Validator.validate_required(password, "Password")
        if not is_valid:
            self.show_error(error)
            return
        
        # Call API
        response = self.api_client.post('/auth/login', {
            'email': email,
            'password': password
        })
        
        if 'error' in response:
            self.show_error(response['error'])
            return
        
        # Save tokens
        self.auth_service.save_token(
            response.get('access_token'),
            response.get('refresh_token')
        )
        
        # Save user data
        self.auth_service.set_current_user(response.get('user'))
        
        # Navigate based on role
        role = response.get('user', {}).get('role')
        self.navigate_to_dashboard(role)
    
    def navigate_to_dashboard(self, role):
        if role == 'patient':
            self.manager.current = 'patient_dashboard'
        else:
            self.show_error("Access denied. This app is for patients only.")
    
    def show_error(self, message):
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()
    
    def go_to_register(self):
        pass  # Registration handled at hospital
