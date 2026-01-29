from pydantic import BaseModel

class QuestionCreate(BaseModel):
    text: str
    correct_answer: str
