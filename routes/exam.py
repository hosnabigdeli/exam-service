from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.exam import Exam
from models.question import Question
import csv, io
from pydantic import BaseModel

router = APIRouter(prefix="/exams", tags=["Exams"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schema برای ایجاد آزمون
class ExamCreate(BaseModel):
    title: str

# ایجاد آزمون
@router.post("/")
def create_exam(data: ExamCreate, db: Session = Depends(get_db)):
    exam = Exam(title=data.title)
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return {"id": exam.id, "title": exam.title}

# آپلود سوالات CSV
@router.post("/{exam_id}/questions/upload")
def upload_questions_csv(exam_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    exam = db.query(Exam).get(exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))

    question_objects = []
    for row in reader:
        if not row.get("text") or not row.get("correct_option"):
            continue
        question_objects.append(
            Question(
                exam_id=exam_id,
                text=row["text"],
                option1=row.get("option1"),
                option2=row.get("option2"),
                option3=row.get("option3"),
                option4=row.get("option4"),
                correct_option=int(row["correct_option"]),
                topic=row.get("topic")
            )
        )

    if question_objects:
        db.add_all(question_objects)
        db.commit()

    return {"message": f"{len(question_objects)} questions uploaded successfully"}

# لیست سوالات یک آزمون
@router.get("/{exam_id}/questions")
def list_questions(exam_id: int, db: Session = Depends(get_db)):
    questions = db.query(Question).filter(Question.exam_id == exam_id).all()
    return [
        {
            "id": q.id,
            "text": q.text,
            "option1": q.option1,
            "option2": q.option2,
            "option3": q.option3,
            "option4": q.option4,
            "correct_option": q.correct_option,
            "topic": q.topic
        } for q in questions
    ]
