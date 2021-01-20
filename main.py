import graphene
import uvicorn
from fastapi import FastAPI
from starlette.graphql import GraphQLApp

from schemas import Mutation, Query

app = FastAPI()

app.add_route('/graphql', GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutation)))

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
