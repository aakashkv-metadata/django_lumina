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

def generate_ai_response(messages_history):
    """
    messages_history: list of dicts {'role': 'user'/'assistant', 'content': 'text'}
    """

    api_key = os.getenv('PPLX_API_KEY')
    
    # Prepend System Prompt
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}] + messages_history[-10:]
    
    if not api_key:
        return "Error: PPLX_API_KEY not configured."

    url = "https://api.perplexity.ai/chat/completions"
    payload = {
        "model": "sonar",
        "messages": messages,
        "temperature": 0.7
    }
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
        if response is not None:
             print(f"Response: {response.text}")
        return "I'm having trouble connecting to my brain right now. Please try again later."
