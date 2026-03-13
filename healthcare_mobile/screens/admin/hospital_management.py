from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from services.api_client import APIClient

class HospitalManagementScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_client = APIClient()
        self.dialog = None
    
    def on_enter(self):
        self.load_hospitals()
    
    def load_hospitals(self):
        response = self.api_client.get('/admin/hospitals')
        
        if 'error' in response:
            self.show_dialog("Error", response['error'])
            return
        
        hospitals = response.get('hospitals', [])
        self.display_hospitals(hospitals)
    
    def display_hospitals(self, hospitals):
        if hasattr(self.ids, 'hospitals_list'):
            self.ids.hospitals_list.clear_widgets()
        
        for hospital in hospitals:
            item = TwoLineListItem(
                text=hospital.get('name', 'N/A'),
                secondary_text=f"{hospital.get('address', 'N/A')} | License: {hospital.get('license_number', 'N/A')}",
                on_release=lambda x, h=hospital: self.view_hospital_detail(h)
            )
            self.ids.hospitals_list.add_widget(item)
    
    def view_hospital_detail(self, hospital):
        message = f"""
Name: {hospital.get('name', 'N/A')}
Address: {hospital.get('address', 'N/A')}
Phone: {hospital.get('phone', 'N/A')}
Email: {hospital.get('email', 'N/A')}
License: {hospital.get('license_number', 'N/A')}
        """
        self.show_dialog("Hospital Details", message.strip())
    
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
