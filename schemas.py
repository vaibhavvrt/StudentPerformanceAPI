# app/schemas.py

import re
from pydantic import BaseModel, Field, validator


class StudentFeatures(BaseModel):

    student_id: str = Field(
        ...,
        description="Student ID (3–20 chars). Allowed: letters, numbers, underscore (_), hyphen (-). No spaces."
    )
    
    attendance_pct: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Attendance percentage (0–100)"
    )

    study_time_hrs: float = Field(
        ...,
        ge=0.0,
        le=8.0,
        description="Average study time per day (0–8 hours)"
    )

    behavior_score: int = Field(
        ...,
        ge=1,
        le=5,
        description="Behavior score (1 = poor, 5 = excellent)"
    )

    midterm_marks: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Midterm exam marks (0–100)"
    )

    assignment_marks: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Assignment marks (0–100)"
    )

    extracurricular_sports: int = Field(
        ...,
        ge=0,
        le=1,
        description="Extracurricular sports participation (1 = Yes, 0 = No)"
    )

 

    @validator("student_id")
    def validate_student_id(cls, value):
        """
        Ensures student_id follows the required pattern
        """
        pattern = r"^[A-Za-z0-9_-]{3,20}$"
        if not re.fullmatch(pattern, value):
            raise ValueError(
                "student_id must be 3–20 characters long and contain only letters, numbers, '_' or '-' (no spaces)"
            )
        return value

    @validator("extracurricular_sports")
    def validate_extracurricular(cls, value):
        """
        Ensures extracurricular_sports is binary (0 or 1)
        """
        if value not in (0, 1):
            raise ValueError("extracurricular_sports must be 0 (No) or 1 (Yes)")
        return value
