import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from core.db import get_db
from core.security import hash_password
from models.user import User


class UserSchema(SQLAlchemyObjectType):
    class Meta:
        model = User
        exclude = ("is_superuser", "password")


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        fullname = graphene.String()

    Output = UserSchema

    @staticmethod
    def mutate(parent, info, username, password, fullname):
        db = get_db()
        user = User(username=username, fullname=fullname, password=hash_password(password))
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
