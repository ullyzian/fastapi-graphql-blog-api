import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from core.db import get_db
from models.comment import Comment


class CommentSchema(SQLAlchemyObjectType):
    class Meta:
        model = Comment
        exclude_fields = ("author_id", "post_id")


class CreateComment(graphene.Mutation):
    class Arguments:
        body = graphene.String(required=True)

    Output = CommentSchema

    @staticmethod
    def mutate(parent, info, body):
        db = get_db()
        comment = Comment(body=body)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment
