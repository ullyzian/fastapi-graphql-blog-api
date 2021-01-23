import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql import GraphQLError

from core.db import Session
from core.security import create_jwt_token, hash_password, verify_password, verify_token
from models.user import User

db = Session.session_factory()


class ErrorSchema(graphene.ObjectType):
    error = graphene.String()


class UserSchema(SQLAlchemyObjectType):
    class Meta:
        model = User
        exclude_fields = ("is_superuser", "password")


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        fullname = graphene.String()
        is_superuser = graphene.Boolean(default_value=False)

    user = graphene.Field(UserSchema)
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

    @staticmethod
    def mutate(parent, info, username, password, fullname, is_superuser):
        user = info.context.get("request").user
        if not user.is_authenticated:
            raise GraphQLError('Not authorized')

        if not user.is_superuser:
            raise GraphQLError('Not enough privileges')
        try:
            user = User(username=username, fullname=fullname, password=hash_password(password),
                        is_superuser=is_superuser)
            db.add(user)
            db.commit()
            db.refresh(user)
            return CreateUser(user=user, success=True)
        except Exception:
            errors = ["username", "This username already taken"]
            return CreateUser(errors=errors, success=False)


class AuthenticateUser(graphene.Mutation):

    user = graphene.Field(UserSchema)
    success = graphene.Boolean()

    @staticmethod
    def mutate(parent, info):
        user = info.context.get("request").user
        if not user.is_authenticated:
            raise GraphQLError('Not authorized')
        return AuthenticateUser(user=user, success=True)


class SignUpUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        fullname = graphene.String()

    user = graphene.Field(UserSchema)
    errors = graphene.List(ErrorSchema)
    success = graphene.Boolean()

    @staticmethod
    def mutate(parent, info, username, password, fullname):
        try:
            user = User(username=username, fullname=fullname, password=hash_password(password))
            db.add(user)
            db.commit()
            db.refresh(user)
            return SignUpUser(user=user, success=True)
        except Exception:
            errors = [{"error": "This username already taken"}]
            return SignUpUser(errors=errors, success=False)


class SignInUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    errors = graphene.List(ErrorSchema)
    success = graphene.Boolean()

    @staticmethod
    def mutate(parent, info, username, password):
        user = db.query(User).filter_by(username=username).first()
        if user is None or not verify_password(password, user.password):
            errors = [{"error": "Can't validate username or password"}]
            return SignInUser(errors=errors, success=False)
        token = create_jwt_token(data={"sub": user.username, "id": user.id})
        return SignInUser(token=token, success=True)
