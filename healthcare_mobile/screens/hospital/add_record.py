from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.pickers import MDDatePicker
from services.api_client import APIClient
from utils.validators import Validator
from plyer import camera
import os

class AddRecordScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_client = APIClient()
        self.dialog = None
        self.selected_date = None
        self.photo_path = None
    
    def select_date(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_selected)
        date_dialog.open()
    
    def on_date_selected(self, instance, value, date_range):
        self.selected_date = value.strftime('%Y-%m-%d')
        self.ids.date_field.text = self.selected_date
    
    def take_photo(self):
        try:
            self.photo_path = os.path.join('temp', 'record_photo.jpg')
            camera.take_picture(self.photo_path, self.on_photo_taken)
        except Exception as e:
            self.show_dialog("Error", f"Camera error: {str(e)}")
    
    def on_photo_taken(self, filepath):
        self.photo_path = filepath
        self.ids.photo_status.text = "Photo captured"
    
    def submit_record(self):
        patient_id = self.ids.patient_id_field.text
        diagnosis = self.ids.diagnosis_field.text
        treatment = self.ids.treatment_field.text
        doctor_name = self.ids.doctor_field.text
        
        # Validate
        is_valid, error = Validator.validate_required(patient_id, "Patient ID")
        if not is_valid:
            self.show_dialog("Error", error)
            return
        
        is_valid, error = Validator.validate_required(diagnosis, "Diagnosis")
        if not is_valid:
            self.show_dialog("Error", error)
            return
        
        # Submit
        data = {
            'patient_id': patient_id,
            'diagnosis': diagnosis,
            'treatment': treatment,
            'doctor_name': doctor_name,
            'date': self.selected_date or ''
        }
        
        if self.photo_path and os.path.exists(self.photo_path):
            response = self.api_client.upload_file('/hospital/records', self.photo_path, data)
        else:
            response = self.api_client.post('/hospital/records', data)
        
        if 'error' in response:
            self.show_dialog("Error", response['error'])
            return
        
        self.show_dialog("Success", "Medical record added successfully")
        self.clear_form()
    
    def clear_form(self):
        self.ids.patient_id_field.text = ""
        self.ids.diagnosis_field.text = ""
        self.ids.treatment_field.text = ""
        self.ids.doctor_field.text = ""
        self.ids.date_field.text = ""
        self.ids.photo_status.text = ""
        self.photo_path = None
    
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
