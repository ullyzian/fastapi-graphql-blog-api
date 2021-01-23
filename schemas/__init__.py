import graphene
from graphql import GraphQLError

from core.db import Session
from models import Comment, Post, User
from .comment import CommentSchema, CreateComment, DeleteComment, UpdateComment
from .post import CreatePost, DeletePost, PostSchema, UpdatePost
from .user import CreateUser, SignInUser, SignUpUser, UserSchema, AuthenticateUser

db = Session.session_factory()


class Query(graphene.ObjectType):
    say_hello = graphene.String(name=graphene.String(default_value="Test"))
    list_comments = graphene.List(CommentSchema)
    detail_comment = graphene.Field(CommentSchema, id=graphene.Int(required=True))
    list_posts = graphene.List(PostSchema)
    detail_post = graphene.Field(PostSchema, id=graphene.Int(required=True))
    list_users = graphene.List(UserSchema)
    detail_user = graphene.Field(UserSchema, id=graphene.Int(required=True))

    @staticmethod
    def resolve_say_hello(parent, info, name: str):
        return f"Hello {name}"

    @staticmethod
    def resolve_list_comments(parent, info):
        return db.query(Comment).all()

    @staticmethod
    def resolve_list_users(parent, info):
        user = info.context.get("request").user
        if not user.is_authenticated:
            raise GraphQLError('Not authorized')

        if not user.is_superuser:
            raise GraphQLError('Not enough privileges')

        return db.query(User).all()

    @staticmethod
    def resolve_list_posts(parent, info):
        return db.query(Post).all()

    @staticmethod
    def resolve_detail_comment(parent, info, id):
        return db.query(Comment).filter_by(id=id).first()

    @staticmethod
    def resolve_detail_user(parent, info, id):
        user = info.context.get("request").user
        if not user.is_authenticated:
            raise GraphQLError('Not authorized')

        if user.is_superuser:
            db_user = db.query(User).filter_by(id=id).first()
        else:
            db_user = db.query(User).filter_by(id=user.id).first()

        if db_user is None:
            raise GraphQLError('User not found')

        return db_user

    @staticmethod
    def resolve_detail_post(parent, info, id):
        return db.query(Post).filter_by(id=id).first()


class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()
    update_comment = UpdateComment.Field()
    delete_comment = DeleteComment.Field()
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    create_user = CreateUser.Field()
    sign_up_user = SignUpUser.Field()
    sign_in_user = SignInUser.Field()
    authenticate_user = AuthenticateUser.Field()
