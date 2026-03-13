import qrcode
from io import BytesIO
from PIL import Image

class QRCodeUtil:
    @staticmethod
    def generate_qr(data: str, size: int = 300) -> Image:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        return img.resize((size, size))
    
    @staticmethod
    def save_qr(data: str, file_path: str, size: int = 300):
        img = QRCodeUtil.generate_qr(data, size)
        img.save(file_path)
        return file_path
    
    @staticmethod
    def qr_to_bytes(data: str, size: int = 300) -> bytes:
        img = QRCodeUtil.generate_qr(data, size)
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return buffer.getvalue()
