import datetime

import jwt

from rest_framework import authentication, exceptions
from rest_framework.exceptions import AuthenticationFailed

from .models import User


class CustomAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        request.user = None

        token = request.headers.get('Authorization').split()[-1]

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        exp = payload.get('exp')
        current_time = datetime.datetime.utcnow().timestamp()

        if current_time > exp:
            raise AuthenticationFailed('JWT Token expired!')

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        return user, token



