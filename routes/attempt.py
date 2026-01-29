from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.attempt import Attempt
from models.question import Question

router = APIRouter(prefix="/attempts", tags=["Attempts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# شروع آزمون
@router.post("/start/{exam_id}")
def start_attempt(exam_id: int, db: Session = Depends(get_db)):
    attempt = Attempt(exam_id=exam_id)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return {"attempt_id": attempt.id, "exam_id": exam_id}

# تحلیل AI
def analyze_attempt(questions, answers):
    topic_errors = []
    for q in questions:
        user_answer = answers.get(q.id)
        if user_answer is None:
            continue
        if int(user_answer) != int(q.correct_option):
            topic_errors.append(q.topic)

    weak_topics = list(set(topic_errors))
    suggested_course = "Advanced " + weak_topics[0].capitalize() if weak_topics else "None"
    mentor_level = "Junior" if weak_topics else "Expert"

    return {
        "weak_topics": weak_topics,
        "suggested_course": suggested_course,
        "mentor_level": mentor_level
    }

# submit + تحلیل
@router.post("/{attempt_id}/submit-analyze")
def submit_and_analyze(
    attempt_id: int,
    answers: dict[int, int],  # {question_id: selected_option_number}
    db: Session = Depends(get_db)
):
    attempt = db.query(Attempt).get(attempt_id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    questions = db.query(Question).filter_by(exam_id=attempt.exam_id).all()

    # محاسبه نمره
    score = 0
    for q in questions:
        user_answer = answers.get(q.id)
        if user_answer is None:
            continue
        if int(user_answer) == int(q.correct_option):
            score += 1

    attempt.score = score
    db.commit()

    # تحلیل AI
    analysis = analyze_attempt(questions, answers)

    return {
        "score": score,
        "total": len(questions),
        "analysis": analysis
    }
