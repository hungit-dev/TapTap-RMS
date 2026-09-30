from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from firebase_admin import auth

from .models import User


class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        try:
            token = auth_header.split(" ")[1]
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token["uid"]
            user = User.objects.get(firebase_uid=uid)
            return (user, token)
        except Exception:
            raise AuthenticationFailed("Invalid Firebase token")