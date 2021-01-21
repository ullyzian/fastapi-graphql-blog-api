from core.db import Session
from models import Post, User

db = Session.session_factory()


def get_user(id):
    return db.query(User).filter_by(id=id).first()


def get_post(id):
    return db.query(Post).filter_by(id=id).first()
