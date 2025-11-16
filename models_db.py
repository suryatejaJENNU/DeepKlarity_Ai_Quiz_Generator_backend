from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from database import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(2083), nullable=False)
    title = Column(String(500))
    date_generated = Column(TIMESTAMP, server_default=func.current_timestamp())
    scraped_content = Column(Text)
    full_quiz_data = Column(Text, nullable=False)
