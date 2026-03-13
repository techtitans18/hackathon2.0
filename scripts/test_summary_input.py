"""Test what text is being fed to the AI summarizer"""
from pathlib import Path

# Simulate the function
def _build_ai_summary_source_text(record_type: str, description: str, file_content: bytes) -> str:
    # Simulate extraction (simplified)
    extracted = file_content.decode('utf-8', errors='ignore')[:500]
    
    parts = [
        f"Record type: {record_type.strip()}",
        f"Clinical description: {description.strip()}",
    ]
    if extracted:
        parts.append(f"Report content: {extracted}")
    return "\n".join(parts)

# Test with minimal input (what you're probably uploading)
record_type = "Kidney Stone"
description = "kidney"
file_content = b"Kidney stone report"

result = _build_ai_summary_source_text(record_type, description, file_content)
print("INPUT TO AI MODEL:")
print("=" * 60)
print(result)
print("=" * 60)
print(f"\nTotal length: {len(result)} characters")
print("\nThis is too short! The AI model just rephrases this minimal text.")
print("You need to upload actual medical reports with detailed content.")
