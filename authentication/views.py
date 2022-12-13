from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from .exceptions import (IncorrectPhoneVerificationCodeException,
                         SmsSendingError, InvalidTokenAPIException)
from authentication import serializers
import environ
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponsePermanentRedirect, FileResponse, HttpResponse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, smart_bytes
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from authentication import services
from phonenumbers.phonenumberutil import region_code_for_number
import phonenumbers

from .models import Pet, PetType

env = environ.Env()
environ.Env.read_env()


class RegisterView(generics.GenericAPIView):
    serializer_class = serializers.RegistrationSerializer

    @staticmethod
    def get_access_token(serializer):
        tokens = serializer.data.get('tokens', None)
        token = tokens.get('access', None)
        return token

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PetCreateAPIView(generics.GenericAPIView):
    serializer_class = serializers.PetCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        name = serializer.data.get('name')
        age = serializer.data.get('age')
        pet_type, created = PetType.objects.get_or_create(title=serializer.data.get('pet_type')['title'])

        pet = Pet.objects.create(
            user=user,
            name=name,
            age=age,
            pet_type=pet_type)

        return Response(serializer.data, status=status.HTTP_200_OK)