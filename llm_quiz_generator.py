import os
import json
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI

load_dotenv()

def generate_quiz(title, text, url):
  
    model = GoogleGenerativeAI(
        model="gemini-2.5-flash"   
    )

    prompt = f"""
You are an AI that generates structured quizzes from Wikipedia text.
Return ONLY JSON — no markdown, no explanation outside JSON.

JSON format:
{{
  "title": "",
  "summary": "",
  "questions": [
    {{
      "question_text": "",
      "choices": [],
      "correct_answer": "",
      "explanation": ""
    }}
  ],
  "key_entities": [],
  "source_url": "{url}"
}}

TITLE: {title}

CONTENT:
{text}
"""

 
    raw = model.invoke(prompt)

  
    try:
        return json.loads(raw)
    except:
       
        start = raw.find("{")
        end = raw.rfind("}") + 1
        cleaned = raw[start:end]
        return json.loads(cleaned)
