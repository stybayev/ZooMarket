from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from firebase.services import firebase_validation

'''
Представление на основе классов для регистрации и входа в систему
с помощью идентификатора токена.
'''


class CheckUserStatusAPIView(GenericAPIView):
    serializer_class = None
    """
    API для проверки пользователя в БД
    """

    def post(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if auth_header:
            id_token = auth_header.split(" ").pop()
            validate = firebase_validation(id_token)

            if validate:
                user = get_user_model().objects.filter(phone_number=validate["phone_number"]).first()
                if user:
                    if user.blocked:
                        return Response({
                            "status": "Blocked",
                            "message": f"{user.reason_for_blocking}"
                        })
                    data = {
                        "id": user.id,
                        "email": user.email,
                        "name": user.first_name,
                        "type": "Существующий пользователь",
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
                    })

                else:
                    user = get_user_model()(uid=validate['uid'],
                                            phone_number=validate['phone_number'])
                    user.save()

                    tokens = {
                        'access': user.tokens.get('access'),
                        'refresh': user.tokens.get('refresh'),
                    }

                    data = {
                        "id": user.id,
                        "type": "Пустой пользователь",
                        "provider": validate['provider'],
                        "uid": user.uid,
                        "is_fill": user.is_fill
                    }

                    return Response({"data": data,
                                     "tokens": tokens})

            else:
                return Response({"message": "Недействительный токен"}, status=400)

        else:
            return Response({"message": "Токен не предоставлен"}, status=400)
