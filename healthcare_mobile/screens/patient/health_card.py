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

        qr_data = json.dumps({
            'health_id': user.get('health_id'),
            'name': user.get('name'),
            'type': 'health_card'
        })

        qr_bytes = QRCodeUtil.qr_to_bytes(qr_data, size=400)
        data = BytesIO(qr_bytes)
        img = CoreImage(data, ext='png')
        self.ids.qr_image.texture = img.texture

        self.ids.patient_name.text = user.get('name', 'N/A')
        self.ids.patient_id.text = f"Health ID: {user.get('health_id', 'N/A')}"
