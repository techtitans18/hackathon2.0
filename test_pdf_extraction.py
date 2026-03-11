"""Test script to verify PDF text extraction for AI summarization"""
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_test_pdf():
    """Create a simple test PDF with medical content"""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Add medical report content
    c.drawString(100, 750, "MEDICAL REPORT")
    c.drawString(100, 720, "Patient: John Doe")
    c.drawString(100, 700, "Date: 2024-01-15")
    c.drawString(100, 670, "Diagnosis: Type 2 Diabetes Mellitus")
    c.drawString(100, 650, "Blood glucose levels elevated at 180 mg/dL.")
    c.drawString(100, 630, "Prescribed Metformin 500mg twice daily.")
    c.drawString(100, 610, "Follow-up recommended in 3 months.")
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

def extract_text_from_pdf(pdf_bytes):
    """Extract text from PDF bytes"""
    try:
        pdf_reader = PdfReader(BytesIO(pdf_bytes))
        text_parts = []
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        
        if text_parts:
            full_text = " ".join(text_parts)
            normalized = " ".join(full_text.split())
            return normalized[:12000]
        return ""
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""

if __name__ == "__main__":
    print("Creating test PDF...")
    pdf_content = create_test_pdf()
    
    print(f"PDF size: {len(pdf_content)} bytes")
    print(f"Starts with PDF header: {pdf_content.startswith(b'%PDF')}")
    
    print("\nExtracting text from PDF...")
    extracted_text = extract_text_from_pdf(pdf_content)
    
    print(f"\nExtracted text ({len(extracted_text)} chars):")
    print("-" * 60)
    print(extracted_text)
    print("-" * 60)
    
    if extracted_text and "Diabetes" in extracted_text:
        print("\n✓ PDF extraction working correctly!")
    else:
        print("\n✗ PDF extraction failed or incomplete")
