from database import SessionLocal
import sqlalchemy.orm as orm



def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


