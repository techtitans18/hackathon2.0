from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from services.api_client import APIClient
from utils.validators import Validator

class RegisterPatientScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_client = APIClient()
        self.dialog = None
    
    def register_patient(self):
        name = self.ids.name_field.text
        email = self.ids.email_field.text
        phone = self.ids.phone_field.text
        dob = self.ids.dob_field.text
        blood_group = self.ids.blood_group_field.text
        
        # Validate
        is_valid, error = Validator.validate_required(name, "Name")
        if not is_valid:
            self.show_dialog("Error", error)
            return
        
        is_valid, error = Validator.validate_email(email)
        if not is_valid:
            self.show_dialog("Error", error)
            return
        
        is_valid, error = Validator.validate_phone(phone)
        if not is_valid:
            self.show_dialog("Error", error)
            return
        
        # Submit
        response = self.api_client.post('/hospital/patients', {
            'name': name,
            'email': email,
            'phone': phone,
            'date_of_birth': dob,
            'blood_group': blood_group
        })
        
        if 'error' in response:
            self.show_dialog("Error", response['error'])
            return
        
        patient_id = response.get('patient_id', 'N/A')
        self.show_dialog("Success", f"Patient registered successfully!\nPatient ID: {patient_id}")
        self.clear_form()
    
    def clear_form(self):
        self.ids.name_field.text = ""
        self.ids.email_field.text = ""
        self.ids.phone_field.text = ""
        self.ids.dob_field.text = ""
        self.ids.blood_group_field.text = ""
    
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
