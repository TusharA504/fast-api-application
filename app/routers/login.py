from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ItemCreate, ShowItem
from models import User
from services import get_db
from sqlalchemy.orm import Session
from hashing import Hasher
from jose import jwt
from config import setting

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login/token")

router=APIRouter()

@router.post("/login/token")
def retrieve_token_after_authentication(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==form_data.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Username")
    
    if not Hasher.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Password")
    
    data={"sub":form_data.username}
    jwt_token=jwt.encode(data,setting.SECRET_KEY,algorithm=setting.ALGORITHM)

    return {"access_token":jwt_token,"token_type":"bearer"}