import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql import GraphQLError

from core.db import Session
from crud import get_post
from models.comment import Comment

db = Session.session_factory()


class CommentSchema(SQLAlchemyObjectType):
    class Meta:
        model = Comment
        exclude_fields = ("author_id", "post_id")


class CreateComment(graphene.Mutation):
    class Arguments:
        body = graphene.String(required=True)
        post_id = graphene.Int(required=True)

    Output = CommentSchema

    @staticmethod
    def mutate(parent, info, body, post_id):
        user = info.context.get("request").user
        if not user.is_authenticated:
            raise GraphQLError('Not authorized')

        post = get_post(post_id)
        if post is None:
            raise GraphQLError('Post not found')
        comment = Comment(body=body, author_id=user.id, post_id=post.id)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment


class UpdateComment(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        body = graphene.String()

    comment = graphene.Field(CommentSchema)
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

    @staticmethod
    def mutate(parent, info, id, body):
        user = info.context.get("request").user
        if not user.is_authenticated:
            raise GraphQLError('Not authorized')
        comment = db.query(Comment).filter_by(id=id, author_id=user.id).first()
        if comment is None:
            return UpdateComment(errors=["id", "Comment with this id not found"], success=False)
        comment.body = body
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return UpdateComment(comment=comment, success=True)


class DeleteComment(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    comment = graphene.Field(CommentSchema)
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

    @staticmethod
    def mutate(parent, info, id):
        user = info.context.get("request").user
        if not user.is_authenticated:
            raise GraphQLError('Not authorized')
        comment = db.query(Comment).filter_by(id=id, author_id=user.id).first()
        if comment is None:
            return DeleteComment(errors=["id", "Comment with this id not found"], success=False)
        return DeleteComment(comment=comment, success=True)
