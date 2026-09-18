from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..auth import verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=schemas.Token)
def login(body: schemas.LoginIn, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == body.email.lower()).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return schemas.Token(access_token=token, role=user.role, name=user.name, user_id=user.id)


@router.get("/me", response_model=schemas.UserOut)
def me(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    class_name = None
    if user.class_id:
        c = db.query(models.ClassRoom).filter(models.ClassRoom.id == user.class_id).first()
        class_name = c.name if c else None
    return schemas.UserOut(
        id=user.id, email=user.email, name=user.name, role=user.role,
        class_id=user.class_id, class_name=class_name
    )
