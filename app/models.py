from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base
from redis import Redis

redis = Redis(host='redis', port=6379)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")



class PrivateMessage(Base):
    __tablename__ = "private_messages"
    id = Column(Integer, primary_key=True, index=True)
    from_userid = Column(String, index=True)
    to_userid = Column(String, index=True)
    subject = Column(String)
    message = Column(String)
    folder = Column(String, default="inbox")
    unread = Column(String, default="Y")

    def isOwner(self):
        #not implemented
        return True
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    
    
 