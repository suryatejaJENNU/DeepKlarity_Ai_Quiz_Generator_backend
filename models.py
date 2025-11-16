
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class Question(BaseModel):
    question_text: str
    choices: List[str]
    correct_answer: str
    explanation: Optional[str] = None

class QuizOutput(BaseModel):
    title: Optional[str]
    summary: Optional[str]
    questions: List[Question]
    key_entities: Optional[List[str]] = []
    source_url: Optional[str]
    generated_at: Optional[datetime]
