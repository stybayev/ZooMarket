from random import randint

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
from authentication import serializers, messages
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
        """
        Роут для регистрации пользователя
        """
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        """
        Роут для логина, после которого сразу генерируется токен
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)  # TODO Убрать проверку, если нет пользоваеля (Вопрос Вове!!!)

        phone_number = serializer.data.get('phone_number', None)
        user = get_user_model().objects.get(phone_number=phone_number)
        phone_verification_code = str(randint(1000, 9999))
        user.phone_verification_code = phone_verification_code
        user.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyPhoneView(generics.GenericAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.PhoneVerificationSerializer

    def post(self, request, *args, **kwargs):  # noqa
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = request.user
            phone_verification_code = serializer.data.get('phone_verification_code', None)

            if not user.phone_verified and (
                    phone_verification_code == user.phone_verification_code):
                user.phone_verified = True
                user.save()

            elif not user.phone_verified and (phone_verification_code != user.phone_verification_code):
                raise IncorrectPhoneVerificationCodeException('Incorrect code')
            return Response(
                {'phone': f'{messages.MOBILE_VERIFY_SUCCESS} {user.phone_number}'},
                status=status.HTTP_200_OK)

        except IncorrectPhoneVerificationCodeException:
            return Response(
                {'error': {
                    'field': 'phone_verification_code',
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': f'{messages.INCORRECT_PHONE}',
                }},
                status=status.HTTP_400_BAD_REQUEST)

        except Exception as message:
            error_type = type(message).__name__
            return Response(
                {'error': {'error_type': f'{error_type}',
                           'message': f'{message}',
                           'status_code': status.HTTP_400_BAD_REQUEST},

                 },
                status=status.HTTP_400_BAD_REQUEST)


class PetCreateAPIView(generics.GenericAPIView):
    serializer_class = serializers.PetCreateSerializer

    def post(self, request):
        """
        Роут для создания питомцев покупателя
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        name = serializer.data.get('name')
        age = serializer.data.get('age')
        pet_type, created = PetType.objects.get_or_create(title=serializer.data.get('pet_type')['title'])

        Pet.objects.create(
            user=user,
            name=name,
            age=age,
            pet_type=pet_type)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserDetailSerializer
    http_method_names = ['get', ]

    def get(self, request):
        """
        Роут для просмотра данных пользователя
        """
        try:
            user = request.user
            serializer = self.serializer_class(user, )

            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as message:
            error_type = type(message).__name__
            return Response(
                {'error': {'error_type': f'{error_type}',
                           'message': f'{message}',
                           'status_code': status.HTTP_400_BAD_REQUEST},
                 },
                status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(generics.GenericAPIView):
    """
    Роут для логаута
    """
    serializer_class = serializers.LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status.HTTP_204_NO_CONTENT)
