from pydantic import BaseModel

class ExamCreate(BaseModel):
    title: str
