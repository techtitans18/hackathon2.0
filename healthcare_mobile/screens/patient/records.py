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
        # Try to get from cache first
        cached_records = self.cache_manager.get('patient_records')
        
        if cached_records:
            self.display_records(cached_records)
        else:
            # Fetch from API
            response = self.api_client.get('/patient/records')
            
            if 'error' in response:
                self.show_dialog("Error", response['error'])
                return
            
            records = response.get('records', [])
            self.cache_manager.set('patient_records', records)
            self.display_records(records)
    
    def display_records(self, records):
        # Clear existing list
        if hasattr(self.ids, 'records_list'):
            self.ids.records_list.clear_widgets()
        
        for record in records:
            item = TwoLineListItem(
                text=record.get('diagnosis', 'No diagnosis'),
                secondary_text=f"Date: {record.get('date', 'N/A')} | Dr. {record.get('doctor_name', 'Unknown')}",
                on_release=lambda x, r=record: self.view_record_detail(r)
            )
            self.ids.records_list.add_widget(item)
    
    def view_record_detail(self, record):
        self.manager.get_screen('record_detail').set_record(record)
        self.manager.current = 'record_detail'
    
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
