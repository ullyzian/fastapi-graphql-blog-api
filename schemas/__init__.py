import graphene

from core.db import get_db
from models.comment import Comment
from .comment import CommentSchema, CreateComment


class Query(graphene.ObjectType):
    say_hello = graphene.String(name=graphene.String(default_value="Test"))
    list_comments = graphene.List(CommentSchema)

    @staticmethod
    def resolve_say_hello(parent, info, name: str):
        return f"Hello {name}"

    @staticmethod
    def resolve_list_comments(parent, info):
        db = get_db()
        return db.query(Comment).all()


class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()
