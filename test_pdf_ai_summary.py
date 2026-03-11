"""
Test PDF Extraction and AI Summary
"""
from io import BytesIO
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Create test PDF
def create_test_pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    c.drawString(100, 750, "MEDICAL REPORT")
    c.drawString(100, 720, "Patient: John Doe")
    c.drawString(100, 700, "Date: 2024-01-15")
    c.drawString(100, 670, "Diagnosis: Type 2 Diabetes Mellitus")
    c.drawString(100, 650, "Blood glucose levels elevated at 180 mg/dL.")
    c.drawString(100, 630, "HbA1c: 8.5% (target <7%)")
    c.drawString(100, 610, "Prescribed Metformin 500mg twice daily.")
    c.drawString(100, 590, "Dietary modifications recommended.")
    c.drawString(100, 570, "Follow-up recommended in 3 months.")
    c.drawString(100, 550, "Monitor blood sugar levels daily.")
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

# Test PDF extraction
print("="*60)
print("TEST 1: PDF Text Extraction")
print("="*60)

pdf_content = create_test_pdf()
print(f"[OK] PDF created: {len(pdf_content)} bytes")
print(f"[OK] Starts with PDF header: {pdf_content.startswith(b'%PDF')}")

# Extract text
try:
    pdf_reader = PdfReader(BytesIO(pdf_content))
    text_parts = []
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)
    
    full_text = " ".join(text_parts)
    normalized = " ".join(full_text.split())
    
    print(f"\n[OK] Extracted text ({len(normalized)} chars):")
    print("-"*60)
    print(normalized)
    print("-"*60)
    
    if "Diabetes" in normalized:
        print("\n[OK] PDF extraction working correctly!")
    else:
        print("\n[ERROR] PDF extraction incomplete")
        
except Exception as e:
    print(f"\n[ERROR] PDF extraction failed: {e}")

# Test AI Summary
print("\n" + "="*60)
print("TEST 2: AI Summary Generation")
print("="*60)

try:
    from app.ai_summary.summarizer import (
        is_summarizer_ready,
        load_summarizer_model,
        generate_medical_summary
    )
    
    print("Checking AI model status...")
    if not is_summarizer_ready():
        print("Loading AI model (this may take a minute)...")
        load_summarizer_model()
    
    print("[OK] AI model loaded")
    
    # Generate summary
    test_text = f"""
    Record type: Lab Report
    Clinical description: Blood test results for diabetes monitoring
    Report content: {normalized}
    """
    
    print("\nGenerating summary...")
    summary = generate_medical_summary(test_text)
    
    print(f"\n[OK] Summary generated ({len(summary)} chars):")
    print("-"*60)
    print(summary)
    print("-"*60)
    
    if summary and len(summary) > 0:
        print("\n[OK] AI summary working correctly!")
    else:
        print("\n[ERROR] AI summary empty")
        
except Exception as e:
    print(f"\n[ERROR] AI summary failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
