from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from screens.login_screen import LoginScreen
from screens.patient.dashboard import PatientDashboardScreen
from screens.patient.records import PatientRecordsScreen
from screens.patient.health_card import HealthCardScreen
from screens.hospital.dashboard import HospitalDashboardScreen
from screens.hospital.add_record import AddRecordScreen
from screens.hospital.register_patient import RegisterPatientScreen
from screens.admin.dashboard import AdminDashboardScreen
from screens.admin.user_management import UserManagementScreen
from screens.admin.hospital_management import HospitalManagementScreen
import os

# Set window size for desktop testing (comment out for mobile)
Window.size = (400, 700)

class HealthcareApp(MDApp):
    def build(self):
        # Modern theme configuration
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.accent_palette = "Teal"
        self.theme_cls.accent_hue = "500"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M3"  # Material Design 3
        
        # Set app title and icon
        self.title = "Healthcare Blockchain"
        self.icon = "assets/images/logo.png" if os.path.exists("assets/images/logo.png") else ""
        
        # Load KV files
        kv_path = os.path.join(os.path.dirname(__file__), 'kv')
        for kv_file in os.listdir(kv_path):
            if kv_file.endswith('.kv'):
                Builder.load_file(os.path.join(kv_path, kv_file))
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(PatientDashboardScreen(name='patient_dashboard'))
        sm.add_widget(PatientRecordsScreen(name='patient_records'))
        sm.add_widget(HealthCardScreen(name='health_card'))
        sm.add_widget(HospitalDashboardScreen(name='hospital_dashboard'))
        sm.add_widget(AddRecordScreen(name='add_record'))
        sm.add_widget(RegisterPatientScreen(name='register_patient'))
        sm.add_widget(AdminDashboardScreen(name='admin_dashboard'))
        sm.add_widget(UserManagementScreen(name='user_management'))
        sm.add_widget(HospitalManagementScreen(name='hospital_management'))
        
        return sm

if __name__ == '__main__':
    HealthcareApp().run()
