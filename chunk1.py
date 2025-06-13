import fitz  # PyMuPDF
import re
import json

# Step 1: Read PDF and extract text
pdf_path = "file1.pdf"  # Replace with your file path
doc = fitz.open(pdf_path)

raw_text = ""
for page in doc:
    raw_text += page.get_text()

# Step 2: Chunk the raw text
chunks = [chunk.strip() for chunk in re.split(r'\n+', raw_text) if chunk.strip()]

# Step 3: Structure rule/example pairs
structured_chunks = []
for chunk in chunks:
    if 'eg.' in chunk:
        rule, example = chunk.split('eg.', 1)
        structured_chunks.append({
            "rule": rule.strip(),
            "example": example.strip()
        })
    elif 'such as' in chunk:
        rule, example = chunk.split('such as', 1)
        structured_chunks.append({
            "rule": rule.strip(),
            "example": 'such as ' + example.strip()
        })
    else:
        structured_chunks.append({
            "rule": chunk.strip(),
            "example": ""
        })

# Step 4: Save to JSON
with open("crop_rotation_chunks.json", "w", encoding="utf-8") as f:
    json.dump(structured_chunks, f, indent=2, ensure_ascii=False)
