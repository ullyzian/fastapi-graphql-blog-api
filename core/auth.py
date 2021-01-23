import os

import jwt
from starlette.authentication import AuthCredentials, AuthenticationBackend

from crud import get_user


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]
        if auth is None or auth == '':
            return
        header, token = auth.split()

        try:
            payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms="HS256")
        except Exception:
            return

        user = get_user(payload.get("id"))
        if user is None:
            return
        user.is_authenticated = True
        return AuthCredentials(["authenticated"]), user
