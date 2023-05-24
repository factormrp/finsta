from sqlalchemy.types import Integer, String
from models.base_model import BaseModel
from sqlalchemy import Column


class User(BaseModel):
    __tablename__ = 'User'
    
    name = Column(String, nullable=False)
    followers = Column(Integer, nullable=False)
    following = Column(Integer, nullable=False)
    posts = Column(Integer, nullable=False)
