from fastapi import FastAPI, HTTPException
from app.schemas import StudentFeatures
from pydantic import BaseModel
from pathlib import Path
import joblib
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "model" / "student_rf_pipeline.pkl"

app = FastAPI(title="Student Performance Analyzer (Pass/Fail)")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Model load error: {e}")

class PredictionResponse(BaseModel):
    student_id: str
    predicted_label: str
    probability: float
    final_score_estimated: float

def compute_final_score(midterm, assignment, attendance, study_hours, behavior_score):
    final_score = (
        0.40 * midterm
        + 0.25 * assignment
        + 0.15 * attendance
        + 0.10 * (study_hours / 8.0 * 100.0)
        + 0.10 * (behavior_score / 5.0 * 100.0)
    )
    return round(final_score, 2)

@app.post("/predict", response_model=PredictionResponse)
def predict(features: StudentFeatures):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    X = [[
        features.attendance_pct,
        features.study_time_hrs,
        features.behavior_score,
        features.midterm_marks,
        features.assignment_marks,
        features.extracurricular_sports
    ]]

    probs = model.predict_proba(X)[0]
    classes = model.classes_
    pred_idx = int(np.argmax(probs))
    pred_class = int(classes[pred_idx])
    label = "Pass" if pred_class == 1 else "Fail"

    final_score = compute_final_score(
        features.midterm_marks,
        features.assignment_marks,
        features.attendance_pct,
        features.study_time_hrs,
        features.behavior_score
    )

    return PredictionResponse(
        student_id=features.student_id,
        predicted_label=label,
        probability=float(probs[pred_idx]),
        final_score_estimated=final_score
    )
