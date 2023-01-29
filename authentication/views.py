import os
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


"""
Представление для изменения данных пользователя 
"""


class UpdateProfileView(generics.UpdateAPIView):
    """
    Роут для изменения данных пользователя
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UpdateProfileSerializer
    http_method_names = ["patch", ]

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        user.email = serializer.data.get('email')
        user.phone_number = serializer.data.get('phone_number')
        user.first_name = serializer.data.get('first_name')
        user.last_name = serializer.data.get('last_name')
        user.gender = serializer.data.get('gender')
        user.date_of_birth = serializer.data.get('date_of_birth')
        user.save()

        return Response(
            {'success': True, 'message': f'{messages.UPDATE_SUCCESS}'},
            status=status.HTTP_200_OK)


class DeleteUserView(generics.GenericAPIView):
    '''
    Представление для удаления пользователя.
    На самом деле, мы не удаляем аккаунты.
    Мы просто затираем всю персональную информацию о пользователе.
    Все заполненные поля, перезаписываем стандартными данными
    для удаленных аккаунтов.
    '''
    queryset = get_user_model().objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.DeleteUserViewSerializer
    http_method_names = ['delete', ]

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.email = f'z{user.id}@deleted.account'
        user.set_password(os.getenv('REMOTE_USER_PASSWORD'))
        user.is_active = False
        user.username = None
        user.phone_number = None
        user.phone_verified = False
        user.first_name = None
        user.last_name = None
        user.save()

        return Response({'success': f'{messages.TEXT_SUCCESSFUL_USER_DELETE}'},
                        status=status.HTTP_200_OK)
