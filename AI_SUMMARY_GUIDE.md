# AI Summary Issue - Repetitive Output

## Problem
You're getting repetitive summaries like:
- "Record type: Kidney Stone. Clinical description: Kidneys Stone."
- "Record type: kidney stone. Clinical description: kidney."

## Root Cause
The AI model (BART) is receiving **insufficient content** to generate meaningful summaries. When you upload files with minimal text like:
- Record Type: "Kidney Stone"
- Description: "kidney"
- File Content: "kidney stone report"

The total input is only ~90 characters. The BART model simply rephrases this minimal input, resulting in repetitive output.

## Solution

### Option 1: Upload Detailed Medical Reports (RECOMMENDED)
Upload actual medical reports with comprehensive content:
- Lab results with values
- Diagnosis details
- Treatment plans
- Clinical observations
- Patient history

**Example**: Use the provided `sample_kidney_stone_report.txt` file which contains:
- Patient information
- Clinical history
- Physical examination findings
- Laboratory results
- Imaging study results
- Diagnosis
- Treatment plan
- Patient education
- Prognosis

This file has ~2000 characters and will generate meaningful AI summaries.

### Option 2: Write Comprehensive Descriptions
When uploading, write detailed clinical descriptions (at least 150 characters):

**Bad Example:**
- Record Type: "Kidney Stone"
- Description: "kidney"

**Good Example:**
- Record Type: "Kidney Stone"
- Description: "Patient presented with severe right flank pain and hematuria. CT scan revealed 7mm calculus in right proximal ureter with moderate hydronephrosis. Started on tamsulosin and pain management. Follow-up in 2 weeks."

## Technical Details

### Minimum Content Requirement
The system now enforces a **150-character minimum** for AI summarization. If your content is too short, you'll receive:

```
HTTP 400 Bad Request
"Insufficient content for AI summarization. Please provide detailed medical reports (at least 150 characters) or write comprehensive clinical descriptions."
```

### How It Works
1. System extracts text from uploaded file (PDF or text)
2. Combines: Record Type + Description + File Content
3. Checks if total length >= 150 characters
4. If too short: Returns error
5. If sufficient: Generates AI summary using BART model

### Content Extraction
- **PDF files**: Extracts text from all pages using PyPDF2
- **Text files**: Reads content directly
- **Maximum**: First 12,000 characters used for summarization

## Testing

### Test with Sample File
1. Use `sample_kidney_stone_report.txt` provided in project root
2. Upload via Hospital Dashboard → Add Medical Record
3. Fill in:
   - Record Type: "Kidney Stone Diagnosis"
   - Description: "Emergency department visit for acute renal colic with confirmed ureteral calculus"
   - File: Select `sample_kidney_stone_report.txt`
4. Submit and check the AI summary

### Expected Result
You should get a meaningful summary like:
"Patient presented with severe right flank pain and hematuria. CT scan revealed 7mm calculus in right proximal ureter causing moderate hydronephrosis. Treatment includes pain management, IV fluids, tamsulosin therapy, and urology follow-up. Stone has 70% chance of spontaneous passage within 4 weeks."

## Best Practices

1. **Always upload actual medical documents** (lab reports, discharge summaries, imaging reports)
2. **Write detailed clinical descriptions** even if file has good content
3. **Include specific medical details**: measurements, test results, medications, procedures
4. **Avoid single-word descriptions** like "kidney" or "test"
5. **Use complete sentences** in the description field

## Files Changed
- `routes/record_routes.py`: Added 150-character minimum check in `_build_ai_summary_source_text()`
- Error handling improved to return HTTP 400 for insufficient content
