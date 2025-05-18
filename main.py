# filename: main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from docx import Document
from docx.shared import RGBColor
import json
import requests
import os

app = FastAPI()

@app.post("/modify-docx")
async def modify_docx(file: UploadFile = File(...), edits: str = Form(...)):
    try:
        edits = json.loads(edits)
    except json.JSONDecodeError:
        return JSONResponse(content={"error": "Invalid JSON in 'edits'"}, status_code=400)

    # Save uploaded file to /tmp
    input_path = "/tmp/uploaded.docx"
    output_path = "/tmp/modified_output.docx"

    with open(input_path, "wb") as buffer:
        buffer.write(await file.read())

    # Load and modify document
    doc = Document(input_path)

    replacements = edits.get("replacements", {})
    highlight_sections = edits.get("highlightSections", [])
    inline_notes = edits.get("inlineNotes", {})

    # Apply replacements
    for para in doc.paragraphs:
        for key, val in replacements.items():
            if key in para.text:
                para.text = para.text.replace(key, val)

    # Highlight sections
    for para in doc.paragraphs:
        if any(section in para.text for section in highlight_sections):
            run = para.add_run("  ← [highlighted section]")
            run.bold = True
            run.font.color.rgb = RGBColor(0, 0, 255)  # Blue

    # Add inline notes
    for para in doc.paragraphs:
        for trigger, note in inline_notes.items():
            if trigger in para.text:
                para.text += f"  *{note}*"

    # Save output
    doc.save(output_path)

    # Upload to file.io
    with open(output_path, "rb") as f:
        response = requests.post("https://file.io", files={"file": f})

    if response.status_code == 200 and response.json().get("success"):
        download_url = response.json().get("link")
        return {"downloadUrl": download_url}
    else:
        return JSONResponse(content={"error": "File upload failed", "details": response.text}, status_code=500)
