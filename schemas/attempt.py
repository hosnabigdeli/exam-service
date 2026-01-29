from pydantic import BaseModel
from typing import Dict

class SubmitAttempt(BaseModel):
    answers: Dict[str, str]
