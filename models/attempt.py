from sqlalchemy import Column, Integer, ForeignKey
from models.base import Base

class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    score = Column(Integer, default=0)
