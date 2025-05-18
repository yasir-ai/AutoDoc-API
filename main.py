# filename: main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from docx import Document
from tempfile import NamedTemporaryFile
import shutil
import uvicorn
import json
import os
from docx.shared import RGBColor

app = FastAPI()

@app.post("/modify-docx")
async def modify_docx(
    file: UploadFile = File(...),
    edits: str = Form(...)  # expects a JSON string
):
    edits = json.loads(edits)
    replacements = edits.get("replacements", {})
    highlight_sections = edits.get("highlightSections", [])
    inline_notes = edits.get("inlineNotes", {})

    # Save uploaded docx to temp file
    with NamedTemporaryFile(delete=False, suffix=".docx") as temp:
        shutil.copyfileobj(file.file, temp)
        temp_path = temp.name

    # Load and modify document
    doc = Document(temp_path)

    # Apply replacements
    for para in doc.paragraphs:
        for key, val in replacements.items():
            if key in para.text:
                para.text = para.text.replace(key, val)

    # Highlight specified sections
    for para in doc.paragraphs:
        if any(section in para.text for section in highlight_sections):
            run = para.add_run("  ← [highlighted section]")
            run.bold = True
            run.font.color.rgb = RGBColor(0, 0, 255)  # blue

    # Add inline notes
    for para in doc.paragraphs:
        for trigger, note in inline_notes.items():
            if trigger in para.text:
                para.text += f"  *{note}*"

    # Save final output file (same directory)
    output_path = temp_path.replace(".docx", "_modified.docx")
    doc.save(output_path)

    # ✅ Make sure the file exists and return it
    if os.path.exists(output_path):
        return FileResponse(
            path=output_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="Modified_Territory_Plan.docx"
        )
    else:
        return {"error": "Modified file could not be found or saved properly"}
