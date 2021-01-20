from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from core.db import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    fullname = Column(String)
    is_superuser = Column(Boolean, default=False)
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")


    def __str__(self):
        return f"User {self.id} - {self.username}"
