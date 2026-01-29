from fastapi import FastAPI
from database import engine
from models.base import Base
from routes.exam import router as exam_router
from routes.attempt import router as attempt_router

app = FastAPI(title="Exam Service MVP")

# ساخت جداول
Base.metadata.create_all(bind=engine)

# ثبت مسیرها
app.include_router(exam_router)
app.include_router(attempt_router)

@app.get("/")
def root():
    return {"status": "exam service running"}
