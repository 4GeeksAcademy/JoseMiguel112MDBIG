from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Column, Table, ForeignKey, Integer
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(20), nullable=False)
    lastname: Mapped[str] = mapped_column(String(20), nullable=False)
    
    

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
        }
    
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id
        }
    
class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user = relationship("User", foreign_keys=[user_id])
    follower = relationship("User", foreign_keys=[follower_id])

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "follower_id": self.follower_id
        }