from pydantic import BaseModel, EmailStr, field_validator
from datetime import date

class PatientCreate(BaseModel):
    full_name:   str
    dob:         str
    email:       EmailStr
    glucose:     float
    haemoglobin: float
    cholesterol: float

    @field_validator("full_name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Full name cannot be empty")
        return v.strip()

    @field_validator("dob")
    @classmethod
    def dob_not_future(cls, v):
        try:
            dob_date = date.fromisoformat(v)
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        if dob_date >= date.today():
            raise ValueError("Date of birth cannot be today or a future date")
        return v

    @field_validator("glucose", "haemoglobin", "cholesterol")
    @classmethod
    def values_positive(cls, v):
        if v <= 0:
            raise ValueError("Blood test values must be positive numbers")
        return v


class PatientOut(PatientCreate):
    id:      int
    remarks: str

    class Config:
        from_attributes = True
