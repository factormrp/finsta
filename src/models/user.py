# Finsta imports
from .base_model import BaseModel
from ..database import db

class User(BaseModel):
    user_id = db.Column(db.Integer, primary_key=True)
    followers = db.Column(db.Integer, nullable=False)
    following = db.Column(db.Integer, nullable=False)
