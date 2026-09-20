#cert-aai-2026-06-0038

import requests

from config import MODEL, OLLAMA_URL, REQUEST_TIMEOUT


def call_ollama(messages, tools=None):
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.3}
    }

    if tools is not None:
        payload["tools"] = tools

    response = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()["message"]