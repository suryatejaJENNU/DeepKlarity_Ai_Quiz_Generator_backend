import os
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise Exception("GEMINI_API_KEY is missing. Add it to backend/.env")

url = "https://generativelanguage.googleapis.com/v1beta/models"
params = {"key": API_KEY}

resp = requests.get(url, params=params)
resp.raise_for_status()

data = resp.json()

print("\n=== AVAILABLE MODELS FOR YOUR API KEY ===")
for model in data.get("models", []):
    print(model["name"])
