from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .exceptions import TokenErrorAPIException, InvalidSizeAPIException, InvalidFormatAPIException, \
    AuthenticationFailedAPIException, AuthenticationFailedIsActiveAPIException
from .models import User, Pet, PetType
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

    def validate(self, data):
        return super().validate(data)

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


class PetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetType
        fields = ['title']


class PetCreateSerializer(serializers.ModelSerializer):
    pet_type = PetTypeSerializer()

    class Meta:
        model = Pet
        fields = ['name', 'age', 'pet_type']
        read_only_fields = ['user', ]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email',
                  'is_superuser', 'is_active', 'is_staff',
                  'phone_number', 'phone_verified', 'first_name', 'last_name',
                  'gender', 'date_of_birth', 'add_pet_status',
                  'reason_for_blocking', 'loyalty_level',)


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
