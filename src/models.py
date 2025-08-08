from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Column, Table, ForeignKey, Integer
from typing import List

db = SQLAlchemy()

followers = Table(
    'followers',
    db.metadata,
    Column('follower_id', ForeignKey('user.id'), primary_key=True),
    Column('followed_id', ForeignKey('user.id'), primary_key=True)
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(
        String(32), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(20), nullable=False)
    lastname: Mapped[str] = mapped_column(String(20), nullable=False)
    followed: Mapped[List["User"]] = relationship("User", foreign_keys="user_id", back_populates="user")
    followers: Mapped[List["User"]] = relationship("User", foreign_keys="user.id", back_populates="user")
    followed: Mapped[List["User"]] = relationship("User", secondary = followers, primaryjoin = id == followers.c.follower_id, secondaryjoin = id == followers.c.followed_id, back_populates = "followers"
    )
    followers: Mapped[List["User"]] = relationship("User", secondary = followers, primaryjoin = id == followers.c.followed_id, secondaryjoin = id == followers.c.follower_id, back_populates = "followed"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "followed": [user.id for user in self.followed.all()],
            "followers": [user.id for user in self.followers.all()]
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }
