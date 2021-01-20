from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.db import Base


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, index=True)
    body = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship("User", back_populates="comments")
    post_id = Column(Integer, ForeignKey("post.id"))
    post = relationship("Post", back_populates="comments")

    def __str__(self):
        return f"Comment {self.id} - {self.body}"
