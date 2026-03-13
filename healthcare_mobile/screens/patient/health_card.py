from kivymd.uix.screen import MDScreen
from kivy.core.image import Image as CoreImage
from io import BytesIO
from services.auth_service import AuthService
from utils.qr_utils import QRCodeUtil
import json

class HealthCardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = AuthService()
    
    def on_enter(self):
        self.generate_qr_code()
    
    def generate_qr_code(self):
        user = self.auth_service.get_current_user()
        
        if not user:
            return
        
        # Create QR data
        qr_data = json.dumps({
            'patient_id': user.get('id'),
            'name': user.get('name'),
            'type': 'health_card'
        })
        
        # Generate QR code
        qr_bytes = QRCodeUtil.qr_to_bytes(qr_data, size=400)
        
        # Display QR code
        data = BytesIO(qr_bytes)
        img = CoreImage(data, ext='png')
        self.ids.qr_image.texture = img.texture
        
        # Set patient info
        self.ids.patient_name.text = user.get('name', 'N/A')
        self.ids.patient_id.text = f"ID: {user.get('id', 'N/A')}"
