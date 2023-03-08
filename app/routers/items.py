from fastapi import APIRouter,Depends,HTTPException,status
from schemas import ItemCreate,ShowItem
from models import Items,User
from services import get_db
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from routers.login import oauth2_scheme
from jose import jwt
from config import setting

router=APIRouter()


def get_user_using_token(token,db):
    try:
        payload = jwt.decode(token, setting.SECRET_KEY,algorithms=setting.ALGORITHM)

        username = payload.get("sub")
      
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")

        user = db.query(User).filter(User.email == username).first()
     
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
        
        return user
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unable to verify credentials")
    



@router.post("/items",response_model=ShowItem)
def create_item(item:ItemCreate,db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    user=get_user_using_token(token,db)
    
    db_item = db.query(Items).filter(Items.title == item.title, Items.description == item.description, Items.owner_id==user.id).first()

    if db_item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item Already Exists With This Title and Description")
    
    date_posted=datetime.now()
    
    item=Items(**item.dict(),date_posted=date_posted,owner_id=user.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/items")
def retrieve_all_items(db: Session = Depends(get_db)):
    items = db.query(Items).all()
    return items


@router.get("/items/{id}")
def retrieve_item_by_id(id:str,db:Session=Depends(get_db)):
    db_item=db.query(Items).filter(Items.id==id).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {id} does not exists")
    
    return db_item

@router.put("/items/update/{id}")
def update_item_by_id(id: str, item: ItemCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user=get_user_using_token(token,db)
    
    existing_item=db.query(Items).filter(Items.id==id,Items.owner_id==user.id)
    if not existing_item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Item {id} does not exists or you're not authorized")

    existing_item.update(jsonable_encoder(item))
    db.commit()
    
    return {"Message":f"Details Of {id} Successfully Updated"}


@router.delete("/items/delete/{id}")
def delete_item_by_id(id: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user=get_user_using_token(token,db)
    
    existing_item=db.query(Items).filter(Items.id==id,Items.owner_id==user.id)
    
    if not existing_item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {id} does not exists or you're not authorized")
    
    existing_item.delete()
    db.commit()

    return {"Message":f"Item {id} Deleted Successfully"}