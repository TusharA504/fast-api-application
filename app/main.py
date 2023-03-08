from fastapi import FastAPI,Depends
from config import setting

from routers import users,items,login
from database import Base,engine

Base.metadata.create_all(bind=engine)

# creats app
app =FastAPI(title=setting.TITLE,
version=setting.VERSION,
description=setting.DESCRIPTION,
contact={"name":setting.NAME,"email":setting.EMAIL})

# creats database
app.include_router(users.router)
app.include_router(items.router)
app.include_router(login.router)

