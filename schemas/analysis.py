# schemas/analysis.py
from pydantic import BaseModel
from typing import List

class AnalysisResult(BaseModel):
    weak_topics: List[str]
    suggested_course: str
    mentor_level: str
