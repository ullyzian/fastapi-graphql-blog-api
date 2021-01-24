import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql import GraphQLError

from core.db import Session
from models.post import Post

db = Session.session_factory()


class PostSchema(SQLAlchemyObjectType):
    class Meta:
        model = Post


class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        body = graphene.String(required=True)

    post = graphene.Field(PostSchema)

    @staticmethod
    def mutate(parent, info, title, body):
        user = info.context.get("request").user
        if not user.is_authenticated:
            raise GraphQLError('Not authorized')
        post = Post(body=body, title=title, author_id=user.id)
        db.add(post)
        db.commit()
        db.refresh(post)
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        body = graphene.String()

    post = graphene.Field(PostSchema)
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

    @staticmethod
    def mutate(parent, info, id, title, body):
        user = info.context.get("request").user
        if not user.is_authenticated:
            raise GraphQLError('Not authorized')

        post = db.query(Post).filter_by(id=id, author_id=user.id).first()
        if post is None:
            return UpdatePost(errors=["id", "Post with this id not found"], success=False)
        post.title = title
        post.body = body
        db.add(post)
        db.commit()
        db.refresh(post)
        return UpdatePost(post=post, success=True)


class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    post = graphene.Field(PostSchema)
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

    @staticmethod
    def mutate(parent, info, id):
        user = info.context.get("request").user
        if not user.is_authenticated:
            raise GraphQLError('Not authorized')

        post = db.query(Post).filter_by(id=id, author_id=user.id).first()
        if post is None:
            return DeletePost(errors=["id", "Post with this id not found"], success=False)
        db.delete(post)
        db.commit()
        return DeletePost(post=post, success=True)
