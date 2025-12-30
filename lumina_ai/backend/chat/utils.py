import os
import requests
import json
from django.conf import settings

SYSTEM_PROMPT = """You are Lumina AI, a professional, calm, and factual AI assistant.
You provide clear, structured, and accurate responses.
Use headings and bullet points where helpful.
Avoid hallucinations.
If you do not know something, state it clearly.
Maintain conversational context within the chat."""


from pathlib import Path
from PIL import Image
from pypdf import PdfReader
import docx

def extract_text_from_file(file_obj):
    """
    Extracts text from a file object (Django UploadedFile or FieldFile).
    Supported formats: .txt, .pdf, .png, .jpg, .jpeg, .docx
    """
    filename = file_obj.name.lower()
    text = ""

    try:
        if filename.endswith('.pdf'):
            reader = PdfReader(file_obj)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        elif filename.endswith('.docx'):
            doc = docx.Document(file_obj)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            # Basic placeholder for OCR or image description if desired.
            try:
                img = Image.open(file_obj)
                text = f"[Image File: {filename}, Size: {img.size}]"
            except Exception:
                 text = "[Image Processing Failed]"
        else:
            # Assume text/code
            try:
                # If it's a file path (FieldFile), open it. If it's a handle, read it.
                if hasattr(file_obj, 'read'):
                    file_obj.seek(0)
                    content = file_obj.read()
                else:
                    with open(file_obj.path, 'rb') as f:
                        content = f.read()
                
                text = content.decode('utf-8', errors='ignore')
            except Exception:
                 text = "[Binary or Unsupported File Content]"

    except Exception as e:
        print(f"Error extracting text: {e}")
        text = f"[Error extracting text from {filename}: {e}]"

    return text.strip()

def generate_ai_response(messages_history, file_context=""):
    """
    messages_history: list of dicts {'role': 'user'/'assistant', 'content': 'text'}
    file_context: string containing text from uploaded files
    """

    api_key = os.getenv('PPLX_API_KEY')
    
    current_system_prompt = SYSTEM_PROMPT
    if file_context:
        current_system_prompt += f"\n\nCONTEXT FROM UPLOADED FILES:\n{file_context}"
    
    # Prepend System Prompt
    messages = [{'role': 'system', 'content': current_system_prompt}] + messages_history[-10:]
    
    if not api_key:
        return "Error: PPLX_API_KEY not configured."

    url = "https://api.perplexity.ai/chat/completions"
    payload = {
        "model": "minimax-01",  # Fixed model name for file issues or general better performance if sonar fails
        "messages": messages,
        "temperature": 0.7
    }
    # Perplexity actually suggests 'sonar' models. Let's stick to what was there or default 'sonar'.
    # Retaining 'sonar' as in original code.
    payload['model'] = 'sonar' 

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        print(f"LLM Error: {e}")
        if 'response' in locals() and response is not None:
             print(f"Response: {response.text}")
        return "I'm having trouble connecting to my brain right now. Please try again later."
