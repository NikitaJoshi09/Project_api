from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.services.auth_service import hash_password, verify_password, create_access_token
from app.services.product_service import get_current_user


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(email: str, password: str, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=email, hashed_password=hash_password(password))
    session.add(user)
    session.commit()
    return {"message": "Registration successful"}


@router.post("/login")
def login(email: str, password: str, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email}