# 📝 AutoDoc API

A FastAPI based docx editor. Edit, highlight, and annotate `.docx` files in seconds with literally a simple & fast API. Super good for programmatic document review or edits.

[![FastAPI](https://img.shields.io/badge/FastAPI-🔋%20Fast%20&%20Simple-brightgreen)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-beta-yellow)](https://github.com/YOUR_USERNAME/fastapi-docx-editor)
[![Built By](https://img.shields.io/badge/Made%20By-Yasir%20Ahmed-orange)](https://github.com/YOUR_USERNAME/fastapi-docx-editor)

---

## 🚀 Features

Allows any Custom GPT to call it and process documents at scale to:

- 🔄 Replace, inject, and edit text in `.docx` files
- 🎯 Highlight key sections
- 💬 Append inline notes dynamically
- ☁️ Uploads the modified files to `file.io` and returns a public download link

## 📦 Quickstart

#### 1-Click Deploy (Cloud)
[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yasir-ai/fastapi-docx-editor)

#### Local Deployment

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
Then go to: http://localhost:8000/docs

Upload a .docx and your edits JSON, and boom -> instant doc enhancement

### Example JSON

```json
{
  "replacements": {
    "Hello": "Hi",
    "world": "Earth"
  },
  "highlightSections": [
    "important",
    "note"
  ],
  "inlineNotes": {
    "FYI": "This was added per client request."
  }
}
```

### 🧪 API Sauce

| Field   | Type     | Description                   |
| ------- | -------- | ----------------------------- |
| `file`  | `File`   | `.docx` file to be edited     |
| `edits` | `string` | JSON string with instructions |

Returns: {"downloadUrl": "https://file.io/abc123"}


# How to send requests to this jawn

## cURL request example
```bash
curl -X POST https://your-vercel-url.vercel.app/modify-docx \
  -F "file=@example.docx" \
  -F 'edits={
    "replacements": {"Hello": "Hi"},
    "highlightSections": ["important"],
    "inlineNotes": {"FYI": "This is a note"}
  }'
```
Make sure:
1) Your docx file is named example.docx
2) You format your edits as a valid JSON string

## Python request example
```python
import requests

url = "https://your-vercel-url.vercel.app/modify-docx"
files = {"file": open("example.docx", "rb")}
data = {
    "edits": '''
    {
        "replacements": {"Hello": "Hi"},
        "highlightSections": ["important"],
        "inlineNotes": {"FYI": "This is a note"}
    }
    '''
}

response = requests.post(url, files=files, data=data)

print(response.json())
```

---

## pro tip
If you're using a custom GPT to send JSON instructions… you're already ahead of the game. Add OpenAI or LLM support and you've got a document editing co pilot
