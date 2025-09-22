import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class JWTUser:
    """Lightweight user object that DRF will treat as authenticated."""

    def __init__(self, user_id, username, role="user"):
        self.id = user_id
        self.username = username
        self.role = role

    @property
    def is_authenticated(self):
        return True 


class CommonJWTAuthentication(BaseAuthentication):
    """
    Custom JWT authentication for microservices.
    Verifies token but does not require auth_user table.
    """

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
                token,
                settings.SIMPLE_JWT["SIGNING_KEY"],  # must match user_backend
                algorithms=[settings.SIMPLE_JWT["ALGORITHM"]],
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        user = JWTUser(
            user_id=payload.get("user_id"),
            username=payload.get("username", f"user_{payload.get('user_id')}"),
            role=payload.get("role", "user"),
        )

        return (user, None)
