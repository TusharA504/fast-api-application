from fastapi import APIRouter, Depends, HTTPException
from schemas import UserCreate, ShowUser
from sqlalchemy.orm import Session
from hashing import Hasher
from services import get_db
from models import User

router = APIRouter()


@router.post('/user', response_model=ShowUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=user.email,
                password=Hasher.get_hash_password(user.password))

   
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user
