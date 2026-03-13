from .login_screen import LoginScreen
from .patient import PatientDashboardScreen, PatientRecordsScreen, HealthCardScreen
from .hospital import HospitalDashboardScreen, AddRecordScreen, RegisterPatientScreen
from .admin import AdminDashboardScreen, UserManagementScreen, HospitalManagementScreen

__all__ = [
    'LoginScreen',
    'PatientDashboardScreen', 'PatientRecordsScreen', 'HealthCardScreen',
    'HospitalDashboardScreen', 'AddRecordScreen', 'RegisterPatientScreen',
    'AdminDashboardScreen', 'UserManagementScreen', 'HospitalManagementScreen'
]
