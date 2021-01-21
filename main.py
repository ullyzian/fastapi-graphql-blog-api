import graphene
import uvicorn
from fastapi import FastAPI
from starlette.graphql import GraphQLApp
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from core.auth import BasicAuthBackend
from schemas import Mutation, Query

middleware = [
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
]

app = FastAPI(middleware=middleware)

app.add_route('/graphql', GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutation)))

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
