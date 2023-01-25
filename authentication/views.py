from random import randint
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .exceptions import (IncorrectPhoneVerificationCodeException,
                         SmsSendingError, InvalidTokenAPIException)
from authentication import serializers, messages
import environ
from rest_framework import generics, status, permissions
from rest_framework.response import Response

env = environ.Env()
environ.Env.read_env()


class RegisterView(generics.GenericAPIView):
    serializer_class = serializers.RegistrationSerializer

    @staticmethod
    def get_access_token(serializer):
        tokens = serializer.data.get('tokens', None)
        token = tokens.get('access', None)
        return token

    def patch(self, request, **kwargs):
        """
        Роут для регистрации пользователя
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = self.kwargs['user_id']
        user = get_object_or_404(get_user_model(), pk=user_id)
        user.email = request.data.get('email', None)
        user.phone_number = request.data.get('phone_number', None)
        user.first_name = request.data.get('first_name', None)
        user.last_name = request.data.get('last_name', None)
        user.gender = request.data.get('gender', None)
        user.date_of_birth = request.data.get('date_of_birth', None)
        user.is_fill = True
        user.save()

        tokens = {
            'access': user.tokens.get('access'),
            'refresh': user.tokens.get('refresh'),
        }

        return Response({'success': True,
                         'tokend': tokens,
                         'is_fill': user.is_fill}, status=status.HTTP_201_CREATED)


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
