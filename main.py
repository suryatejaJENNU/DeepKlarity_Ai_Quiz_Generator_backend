from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

from database import SessionLocal, engine, Base
from models_db import Quiz
from scraper import scrape_wikipedia
from llm_quiz_generator import generate_quiz  

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Wiki Quiz Generator")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    url: str


@app.post("/generate_quiz")
def generate_quiz_endpoint(req: GenerateRequest):
    url = req.url

    # STEP 1: Scrape Wikipedia
    try:
        title, content = scrape_wikipedia(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Scraper failed: {e}")

    # STEP 2: Generate quiz using LLM
    try:
        quiz = generate_quiz(title, content, url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM failed: {e}")

    # STEP 3: Save to DB
    db = SessionLocal()
    record = Quiz(
        url=url,
        title=quiz.get("title", title),
        scraped_content=content,
        full_quiz_data=json.dumps(quiz),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    db.close()

    return {"id": record.id, "quiz": quiz}


@app.get("/history")
def history():
    db = SessionLocal()
    rows = db.query(Quiz).order_by(Quiz.id.desc()).all()
    db.close()

    return [
        {
            "id": r.id,
            "url": r.url,
            "title": r.title
        }
        for r in rows
    ]


@app.get("/quiz/{quiz_id}")
def get_quiz(quiz_id: int):
    db = SessionLocal()
    r = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    db.close()

    if not r:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return {
        "id": r.id,
        "quiz": json.loads(r.full_quiz_data)
    }
