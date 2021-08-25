from .serializers import UserSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.


# Register API


class RegisterAPI(APIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            data = dict()
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                account = serializer.create(serializer.validated_data)
                account.is_active = True
                account.save()
                token = Token.objects.get_or_create(user=account)[0].key
                data["email"] = account.email
                data["id"] = account.id
                data["token"] = token

            else:
                data = serializer.errors

            return Response(data)

        except IntegrityError as e:
            account = User.objects.get(username='')
            account.delete()
            raise ValidationError({"400": f'{str(e)}'})

        except KeyError as e:
            print(e)
            raise ValidationError({"400": f'Field {str(e)} missing'})


class LoginAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = dict()
        try:
            current_user = User.objects.get(email=request.data.get('username'))
        except BaseException as e:
            raise ValidationError({"400": f'{str(e)}'})

        token = Token.objects.get_or_create(user=current_user)[0].key
        print(token)
        if not current_user.check_password(request.data['password']):
            raise ValidationError({"message": "Incorrect Login credentials"})

        if current_user:
            if current_user.is_active:
                print(request.user)
                login(request, current_user)
                data["message"] = "user logged in"
                data["email_address"] = current_user.email
                data["id"] = current_user.id

                Res = {"data": data, "token": token}

                return Response(Res)

            else:
                raise ValidationError({"400": f'Account not active'})

        else:
            raise ValidationError({"400": f'Account doesnt exist'})
