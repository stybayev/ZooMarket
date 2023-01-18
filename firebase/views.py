from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from firebase.auth_fiebase import firebase_validation


class SocialSignupAPIView(GenericAPIView):
    """
    API для создания пользователя из социальных сетей
    """

    def post(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if auth_header:
            id_token = auth_header.split(" ").pop()
            validate = firebase_validation(id_token)
            # print(id_token)
            # print(validate)
            # return Response({"data": "ok"})

            if validate:
                user = get_user_model().objects.filter(uid=validate["uid"]).first()

                if user:
                    data = {
                        "id": user.id,
                        "email": user.email,
                        "name": user.name,
                        "image": user.image,
                        "type": "existing_user",
                        "provider": validate['provider']
                    }

                    return Response({"data": data, "message": "Login Successful"})

                else:
                    # user = get_user_model()(email=validate['email'],
                    #                         name=validate['name'],
                    #                         uid=validate['uid'],
                    #                         image=validate['image'])
                    # user.save()
                    #
                    # data = {
                    #     "id": user.id,
                    #     "email": obj.email,
                    #     "name": obj.name,
                    #     "image": obj.image,
                    #     "type": "new_user",
                    #     "provider": validate['provider']
                    # }

                    return Response({"data": "ok",
                                     "message": "Необходимо зарегаться"})

        else:
            return Response({"message": "invalid token"})
            # else:
            #     return Response({"message": "token not provided"})
