import graphene
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.graphql import GraphQLApp
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from core.auth import BasicAuthBackend
from schemas import Mutation, Query

middleware = [
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
]
origins = [
    "http://localhost:8080",
    "http://localhost:3000"
]

app = FastAPI(middleware=middleware)
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.add_route('/graphql', GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutation)))

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
