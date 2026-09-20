#cert-aai-2026-06-0038

import os
from pathlib import Path


def load_env_file():
    env_file = Path(__file__).with_name(".env")

    if not env_file.exists():
        return None

    with open(env_file, "r") as f:
        content = f.read().splitlines()

    for line in content:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env_file()

MODEL = os.getenv("MODEL", "gemma4:e4b")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))
