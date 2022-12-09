from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .exceptions import TokenErrorAPIException, InvalidSizeAPIException, InvalidFormatAPIException
from .models import User
from rest_framework.exceptions import AuthenticationFailed


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=255, min_length=3,
        validators=[UniqueValidator(queryset=get_user_model().objects.all(),
                                    message='Введите E-mail')],
        error_messages={"blank": "Введите E-mail адрес"})

    password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
        error_messages={"blank": "Введите пароль"}
    )

    tokens = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'email', 'password', 'tokens', 'phone_number',
            'first_name', 'last_name',
            'gender', 'date_of_birth',
        )

    # def validate(self, data):
    #     phone_number = str(data.get('phone_number', None)).strip()
    #     validate_phone_number(phone_number=phone_number)
    #     return super().validate(data)

    """
    Создание объекта. Данные в конструктор передаются уже проверенными
    """

    def create(self, validated_data):
        self.user = get_user_model().objects.create_user(**validated_data)
        self.user.username = validated_data.get('email', None)
        self.user.save()
        return self.user

    """
    Генерация токенов для пользователя.
    """

    def get_tokens(self, obj):
        user = get_user_model().objects.get(email=self.user.email)

        tokens = {
            'access': user.tokens.get('access'),
            'refresh': user.tokens.get('refresh'),
        }

        return tokens

class LoginSerializer(serializers.ModelSerializer):
    # phone_number = serializers.CharField(
    #     required=True, min_length=3,
    #     error_messages={"blank": "Введите Номер телефона."})

    def get_tokens(self, obj):
        user = get_user_model().objects.get(phone_number=obj['phone_number'])
        print(user)

        return {
            'access': user.tokens.get('access'),
            'refresh': user.tokens.get('refresh'),
        }

    class Meta:
        model = get_user_model()
        fields = ['phone_number', 'tokens',]

    def validate(self, attrs):  # noqa
        phone_number = attrs.get('phone_number', None)
        user = get_user_model().objects.get(phone_number=phone_number)

        self.user = authenticate(email=user.email, password=user.password)
        print(self.user)

        if not self.user:
            raise AuthenticationFailed('Такого пользователя не существует!')

        if not self.user.is_active:
            raise AuthenticationFailed('Аккаунт отключен, обратитесь к администратору')

        if self.user.is_deleted:
            raise AuthenticationFailed('Пользователь с таким номером телефона заблокирован!')
        return super().validate(attrs)

