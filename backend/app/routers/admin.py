from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..auth import require_roles, hash_password

router = APIRouter(prefix="/api/admin", tags=["admin"], dependencies=[Depends(require_roles("admin"))])


@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    return {
        "users": db.query(models.User).count(),
        "students": db.query(models.User).filter(models.User.role == "student").count(),
        "teachers": db.query(models.User).filter(models.User.role == "teacher").count(),
        "classes": db.query(models.ClassRoom).count(),
        "subjects": db.query(models.Subject).count(),
        "quizzes": db.query(models.Quiz).count(),
        "attempts": db.query(models.Attempt).count(),
        "questions": db.query(models.Question).count(),
    }


@router.get("/users")
def users(db: Session = Depends(get_db)):
    rows = db.query(models.User).order_by(models.User.role, models.User.name).all()
    out = []
    for u in rows:
        cname = None
        if u.class_id:
            c = db.query(models.ClassRoom).filter(models.ClassRoom.id == u.class_id).first()
            cname = c.name if c else None
        out.append({
            "id": u.id, "email": u.email, "name": u.name, "role": u.role,
            "class_id": u.class_id, "class_name": cname,
        })
    return out


@router.post("/users")
def create_user(body: schemas.UserCreate, db: Session = Depends(get_db)):
    if body.role not in ("admin", "teacher", "student"):
        raise HTTPException(400, "Invalid role")
    if db.query(models.User).filter(models.User.email == body.email.lower()).first():
        raise HTTPException(400, "Email already exists")
    u = models.User(
        email=body.email.lower(),
        name=body.name,
        hashed_password=hash_password(body.password),
        role=body.role,
        class_id=body.class_id,
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return {"id": u.id, "email": u.email, "name": u.name, "role": u.role}


@router.get("/classes")
def classes(db: Session = Depends(get_db)):
    rows = db.query(models.ClassRoom).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "grade": c.grade,
            "student_count": db.query(models.User).filter(models.User.class_id == c.id, models.User.role == "student").count(),
        }
        for c in rows
    ]


@router.post("/classes")
def create_class(name: str, grade: str, db: Session = Depends(get_db)):
    c = models.ClassRoom(name=name, grade=grade)
    db.add(c)
    db.commit()
    db.refresh(c)
    return {"id": c.id, "name": c.name, "grade": c.grade}


@router.get("/subjects")
def subjects(db: Session = Depends(get_db)):
    rows = db.query(models.Subject).all()
    out = []
    for s in rows:
        c = db.query(models.ClassRoom).filter(models.ClassRoom.id == s.class_id).first()
        out.append({
            "id": s.id, "name": s.name, "class_id": s.class_id,
            "teacher_id": s.teacher_id, "class_name": c.name if c else None,
        })
    return out
