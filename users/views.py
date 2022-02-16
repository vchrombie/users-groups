import datetime
import jwt

from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .serializers import UserSerializer

User = get_user_model()


@api_view(['GET'])
@permission_classes((permissions.AllowAny, ))
@authentication_classes(())
def api_root(request):
    return Response(
        {
            'register': reverse(viewname='register', request=request),
            'login': reverse(viewname='login', request=request),
            'logout': reverse(viewname='logout', request=request),
            'user': reverse(viewname='user', request=request),
        },
        status=status.HTTP_200_OK
    )


class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):

    permission_classes = [
        permissions.AllowAny,
    ]

    authentication_classes = []

    def post(self, request):
        phone_number = request.data['phone_number']
        password = request.data['password']

        user = User.objects.filter(phone_number=phone_number).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        # response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            "jwt": token,
        }
        return response


class UserView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request):
        user = User.objects.filter(id=request.user.id).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

