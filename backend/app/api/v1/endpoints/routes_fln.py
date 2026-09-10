"""FLN Curriculum & Lessons Route."""

from typing import Optional
from fastapi import APIRouter, HTTPException
from app.services.fln_service import fln_service

router = APIRouter()


@router.get("/fln/grades", tags=["Curriculum"])
async def get_grades():
    """List available grades and enrolled subjects."""
    return fln_service.get_grades()


@router.get("/fln/outcomes", tags=["Curriculum"])
async def get_learning_outcomes(grade: Optional[int] = None, subject: Optional[str] = None):
    """Retrieve official NIPUN Bharat learning outcomes filtered by grade and subject."""
    return fln_service.get_outcomes(grade=grade, subject=subject)


@router.get("/fln/lessons", tags=["Curriculum"])
async def get_lessons(
    grade: Optional[int] = None,
    subject: Optional[str] = None,
    outcome_id: Optional[str] = None
):
    """Retrieve structured lessons matching curriculum parameters."""
    return fln_service.get_lessons(grade=grade, subject=subject, outcome_id=outcome_id)


@router.get("/fln/lessons/{lesson_id}", tags=["Curriculum"])
async def get_lesson_detail(lesson_id: str):
    """Retrieve full structured lesson with explanation, activity, and assessment."""
    lesson = fln_service.get_lesson_by_id(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found.")
    return lesson
