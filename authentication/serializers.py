from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from pet.models import PetType
from .exceptions import (TokenErrorAPIException,
                         AuthenticationFailedAPIException,
                         AuthenticationFailedIsActiveAPIException)
# from .models import User, Pet, PetType, UserProfile
from rest_framework.exceptions import AuthenticationFailed


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class RegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        max_length=255, min_length=3,
        required=True,
        error_messages={"blank": "Введите имя"})

    last_name = serializers.CharField(
        max_length=255, min_length=3,
        required=True,
        error_messages={"blank": "Введите фамилию"})

    gender = serializers.ChoiceField(
        choices=get_user_model().GENDER_CHOICES,
        required=True,
        error_messages={"blank": "Введите пол"})

    date_of_birth = serializers.DateField(
        required=True,
        error_messages={"blank": "Введите дату рождения"})

    email = serializers.EmailField(
        max_length=255, min_length=3,
        validators=[UniqueValidator(queryset=get_user_model().objects.all(),
                                    message='Данный email уже зарегистрирован в нашей системе')],
        error_messages={"blank": "Введите E-mail адрес"})

    tokens = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'email', 'tokens', 'phone_number',
            'first_name', 'last_name',
            'gender', 'date_of_birth',
        )

    def validate(self, data):
        return super().validate(data)

    def get_tokens(self, obj):
        self.user = get_user_model().objects.get(phone_number=obj['phone_number'])

        return {
            'access': self.user.tokens.get('access'),
            'refresh': self.user.tokens.get('refresh'),
        }


class LoginSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        required=True, min_length=3,
        error_messages={"blank": "Введите Номер телефона."})
    tokens = serializers.SerializerMethodField()

    phone_verified = serializers.SerializerMethodField()

    def get_phone_verified(self, obj):
        return self.user.phone_verified

    def get_tokens(self, obj):
        self.user = get_user_model().objects.get(phone_number=obj['phone_number'])

        return {
            'access': self.user.tokens.get('access'),
            'refresh': self.user.tokens.get('refresh'),
        }

    class Meta:
        model = get_user_model()
        fields = ['phone_number', 'tokens', 'phone_verified']

    def validate(self, attrs):  # noqa
        phone_number = attrs.get('phone_number', None)
        self.user = authenticate(phone_number=phone_number, )

        user = get_user_model().objects.filter(phone_number=phone_number).exists()
        if user:
            user_in_db = get_user_model().objects.get(phone_number=phone_number)

            if user_in_db.blocked:
                raise AuthenticationFailedAPIException('Пользователь с таким номером телефона заблокирован!')
            if not user_in_db.is_active:
                raise AuthenticationFailedIsActiveAPIException('Аккаунт отключен, обратитесь к администратору')

        if not user:
            raise AuthenticationFailed('Такого пользователя не существует!')

        return super().validate(attrs)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email',
                  'is_superuser', 'is_active', 'is_staff',
                  'phone_number', 'phone_verified', 'first_name', 'last_name',
                  'gender', 'date_of_birth', 'add_pet_status',
                  'reason_for_blocking', 'loyalty_level', 'is_fill',
                  'blocked', 'reason_for_blocking')


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        error_messages={"blank": "Введите refresh токен"}
    )

    default_error_messages = {
        "bad_token": ("Ваша сессия авторизации устарела. "
                      "Необходимо Войти в личный кабинет")
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise TokenErrorAPIException()


class PhoneVerificationSerializer(serializers.ModelSerializer):
    phone_verification_code = serializers.CharField(
        required=True,
        error_messages={"blank": "Введите 4-х значный Код подтверждения"})

    class Meta:
        model = get_user_model()
        fields = ['phone_verification_code', ]


class UpdateProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, min_length=3, required=False, )
    last_name = serializers.CharField(max_length=255, min_length=3, required=False, )
    gender = serializers.ChoiceField(choices=get_user_model().GENDER_CHOICES, required=False, )
    date_of_birth = serializers.DateField(required=False, )
    email = serializers.EmailField(max_length=255, min_length=3, required=False, )

    class Meta:
        model = get_user_model()
        fields = ('email',
                  'first_name', 'last_name',
                  'gender', 'date_of_birth',
                  )


class DeleteUserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = []

