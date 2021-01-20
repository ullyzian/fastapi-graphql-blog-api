import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from core.db import get_db
from models.post import Post


class PostSchema(SQLAlchemyObjectType):
    class Meta:
        model = Post
        exclude = ("author_id",)


class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        body = graphene.String(required=True)

    Output = PostSchema

    @staticmethod
    def mutate(parent, info, title, body):
        db = get_db()
        post = Post(body=body, title=title)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post
