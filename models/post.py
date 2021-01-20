from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.db import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

    def __str__(self):
        return f"Post {self.id} - {self.title}"
