from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from services.api_client import APIClient
from utils.cache_manager import CacheManager

class PatientRecordsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_client = APIClient()
        self.cache_manager = CacheManager()
        self.dialog = None
    
    def on_enter(self):
        self.load_records()
    
    def load_records(self):
        cached_records = self.cache_manager.get('patient_records')
        if cached_records:
            self.display_records(cached_records)
        else:
            response = self.api_client.get('/patient/me')
            if 'error' in response:
                self.show_dialog("Error", response['error'])
                return
            records = response.get('records', [])
            self.cache_manager.set('patient_records', records)
            self.display_records(records)
    
    def display_records(self, records):
        if hasattr(self.ids, 'records_list'):
            self.ids.records_list.clear_widgets()
        if not records:
            from kivymd.uix.list import OneLineListItem
            self.ids.records_list.add_widget(OneLineListItem(text="No records found."))
            return
        for record in records:
            item = TwoLineListItem(
                text=f"{record.get('record_type', 'Record')} — {record.get('description', 'N/A')}",
                secondary_text=f"Hospital: {record.get('HospitalID', 'N/A')} | {str(record.get('timestamp', 'N/A'))[:10]}",
                on_release=lambda x, r=record: self.view_record_detail(r)
            )
            self.ids.records_list.add_widget(item)
    
    def view_record_detail(self, record):
        msg = (
            f"Type: {record.get('record_type', 'N/A')}\n"
            f"Description: {record.get('description', 'N/A')}\n"
            f"Hospital: {record.get('HospitalID', 'N/A')}\n"
            f"Date: {str(record.get('timestamp', 'N/A'))[:10]}\n"
            f"File: {record.get('file_name', 'N/A')}"
        )
        self.show_dialog("Record Details", msg)
    
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
