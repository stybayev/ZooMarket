from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from firebase.services import firebase_validation

'''
Представление на основе классов для регистрации и входа в систему
с помощью идентификатора токена.
'''


class CheckUserStatusAPIView(GenericAPIView):
    """
    API для создания пользователя из социальных сетей
    """

    def post(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if auth_header:
            id_token = auth_header.split(" ").pop()
            validate = firebase_validation(id_token)

            if validate:
                user = get_user_model().objects.filter(uid=validate["uid"]).first()
                if user:
                    data = {
                        "id": user.id,
                        "email": user.email,
                        "name": user.first_name,
                        "type": "existing_user",
                        "provider": validate['provider'],
                        "is_fill": user.is_fill
                    }

                    tokens = {
                        'access': user.tokens.get('access'),
                        'refresh': user.tokens.get('refresh'),
                    }

                    return Response({
                        "data": data,
                        "tokens": tokens,
                        "status": True
                    })

                else:
                    print(validate)
                    user = get_user_model()(
                        # password=validate['uid'],
                        uid=validate['uid'],
                    )
                    user.save()

                    data = {
                        "id": user.id,
                        "type": "Пустой пользователь",
                        "provider": validate['provider'],
                        "uid": user.uid
                    }

                    return Response({"data": data,
                                     "status": False})

            else:
                return Response({"message": "Недействительный токен"})

        else:
            return Response({"message": "Токен не предоставлен"})
