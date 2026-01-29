from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    text = Column(String)
    option1 = Column(String)
    option2 = Column(String)
    option3 = Column(String)
    option4 = Column(String)
    correct_option = Column(Integer)  # عدد صحیح بین 1 تا 4
    topic = Column(String)
