from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import exceptions
from firebase_admin import auth, initialize_app

initialize_app()


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.META.get("HTTP_AUTHORIZATION")
        if not authorization_header:
            raise exceptions.AuthenticationFailed('Учетные данные авторизации не предоставлены')
        id_token = authorization_header.split(" ").pop()
        if not id_token:
            raise exceptions.AuthenticationFailed('Учетные данные авторизации не предоставлены')
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise exceptions.AuthenticationFailed('Недействительный ID Token')
        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise exceptions.AuthenticationFailed('Такого пользователя не существует')

        user, created = get_user_model().objects.get_or_create(username=uid)

        # if ((not user.first_name or not hasattr(user, 'userprofile'))
        #         and not (request.method == 'PUT'
        #                  and request.path.startswith("/api/users/"))):
        #     raise exceptions.PermissionDenied('Профиль пользователя неполный. Пожалуйста, обновите данные профиля')
        # разрешить пользователям совершать вызовы API только после завершения профиля
        return (user, None)
        pass