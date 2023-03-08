from database import Base
import uuid
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE


class User(Base):
    __tablename__ = "users"

    # id = Column(String(100), primary_key=True, default=str(uuid.uuid4()))
    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    email = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)

    items = relationship("Items", back_populates="owner")


class Items(Base):
    __tablename__ = "items"

    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    title = Column(String(100), nullable=False)
    description = Column(String(150))
    date_posted = Column(Date)
    owner_id = Column(GUID, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
