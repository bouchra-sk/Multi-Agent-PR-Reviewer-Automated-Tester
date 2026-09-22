# backend/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH, override=True)

LLM_API_KEY = os.getenv("LLM_API_KEY") or os.getenv("Secret_Key", "")
LLM_API_URL = os.getenv("LLM_API_URL", "https://api.lablab.ai/v1")