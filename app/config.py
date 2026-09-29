import os

from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "TacketSmart AI")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "tacketsmart-secret-key-change-this"
)