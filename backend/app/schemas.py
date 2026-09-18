from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    name: str
    user_id: int

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    name: str
    role: str
    class_id: Optional[int] = None
    class_name: Optional[str] = None
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: str
    class_id: Optional[int] = None

class QuizCreate(BaseModel):
    title: str
    subject_id: int
    question_ids: List[int]
    due_date: Optional[datetime] = None

class AttemptSubmit(BaseModel):
    answers: dict

class PracticeRequest(BaseModel):
    subject_id: Optional[int] = None
    count: int = 6
    focus_weak: bool = True
