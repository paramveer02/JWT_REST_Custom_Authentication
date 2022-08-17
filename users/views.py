import datetime

import jwt
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import RegisterSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LogInView(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("user not found".title())

        if not user.check_password(password):
            raise AuthenticationFailed("incorrect password".title())

        # we define a payload to create a jwt token
        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(
                minutes=60
            ),  # we will keep the token valid for 60 minutes after login
            "iat": datetime.datetime.utcnow(),
        }

        # now we create a jwt token using the payload data,that will be converted to json,
        # HS256 is the signature algorithm,
        # the decode function converts the binary string into a unicode string

        # this token will be used to login our user
        token = jwt.encode(payload, "secret", algorithm="HS256").decode("utf-8")

        # Lets return this token using cookies
        response = Response()

        response.set_cookie(key="jwt", value=token, httponly=True)

        response.data = {
            "jwt": token,
        }

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("unauthenticated user".title())
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!!")
        user = User.objects.get(id=payload["id"])
        print(user)
        serialzer = RegisterSerializer(user)
        return Response(serialzer.data)


class LogOutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {"message": f" you have been successfully logged out!!".title()}
        return response
