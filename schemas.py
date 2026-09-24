from typing import List

from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=5000)


class QuizRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=5000)
    level: str = Field(default="Beginner", max_length=100)


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(..., min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    questions: List[QuizQuestion] = Field(..., min_length=3, max_length=3)
