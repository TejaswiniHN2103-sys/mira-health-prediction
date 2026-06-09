from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List
import httpx
import os
from dotenv import load_dotenv

from database import SessionLocal, engine, Base
import models
import schemas

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MIRA - Health Prediction Application")

app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def generate_health_remarks(glucose: float, haemoglobin: float, cholesterol: float) -> str:
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return "API key not configured. Please add GROQ_API_KEY to your .env file."

    prompt = (
        f"You are a medical AI assistant. Based on the following blood test results, "
        f"provide a brief health assessment in 2-3 sentences. "
        f"Mention possible health risks if values are abnormal, or confirm if normal.\n\n"
        f"- Glucose: {glucose} mg/dL (Normal: 70-99)\n"
        f"- Haemoglobin: {haemoglobin} g/dL (Normal: 12-17.5)\n"
        f"- Cholesterol: {cholesterol} mg/dL (Normal: below 200)\n\n"
        f"Give only a concise clinical remark. No bullet points."
    )

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150,
        "temperature": 0.3
    }

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            data = response.json()
            if "error" in data:
                return f"API Error: {data['error'].get('message', 'Unknown error')}"
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Could not generate remarks: {str(e)}"


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", "r") as f:
        return f.read()


@app.post("/patients/", response_model=schemas.PatientOut)
async def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_patient = models.Patient(**patient.dict(), remarks="Generating...")
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    remarks = await generate_health_remarks(patient.glucose, patient.haemoglobin, patient.cholesterol)
    db_patient.remarks = remarks
    db.commit()
    db.refresh(db_patient)
    return db_patient


@app.get("/patients/", response_model=List[schemas.PatientOut])
def get_patients(db: Session = Depends(get_db)):
    return db.query(models.Patient).order_by(models.Patient.id.desc()).all()


@app.get("/patients/{patient_id}", response_model=schemas.PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@app.put("/patients/{patient_id}", response_model=schemas.PatientOut)
async def update_patient(patient_id: int, patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    for key, value in patient.dict().items():
        setattr(db_patient, key, value)
    remarks = await generate_health_remarks(patient.glucose, patient.haemoglobin, patient.cholesterol)
    db_patient.remarks = remarks
    db.commit()
    db.refresh(db_patient)
    return db_patient


@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(db_patient)
    db.commit()
    return {"message": "Patient record deleted successfully"}


@app.get("/test-api")
async def test_api():
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return {"status": "ERROR", "message": "No GROQ_API_KEY found in .env"}
    return {"status": "OK", "key_starts_with": api_key[:8] + "..."}
