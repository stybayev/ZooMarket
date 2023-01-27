from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from authentication import messages
from pet import serializers
import environ
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from pet.models import PetType, Pet

env = environ.Env()
environ.Env.read_env()


class PetCreateAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
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

        pet_type = PetType.objects.filter(title=serializer.data.get('pet_type')).exists()

        try:
            if not pet_type:
                raise ValueError('Указанного типа питомца не существует')
            pet_type = PetType.objects.get(title=serializer.data.get('pet_type'))
            Pet.objects.create(
                user=user,
                name=name,
                age=age,
                pet_type=pet_type)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as message:
            return Response({'message': 'Указанного типа питомца не существует'},
                            status=status.HTTP_404_NOT_FOUND)


'''
Представление для получения списка питомцев текущего пользователя
'''


class PetListViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    '''
    Представление для получения списка питомцев текущего пользователя
    '''
    http_method_names = ['get', 'delete']
    queryset = Pet.objects.all()
    serializer_class = serializers.PetListSerializer

    def get_queryset(self):
        user = self.request.user
        return Pet.objects.filter(user=user)


"""
ля изменения данных питомцев пользователя.
"""


class PetUpdateView(generics.UpdateAPIView):
    """
    Роут для изменения данных питомцев пользователя.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.PetUpdateSerializer
    http_method_names = ["patch", ]

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        pet = get_object_or_404(Pet, pk=self.kwargs['pet_id'])
        if not pet in Pet.objects.filter(user=request.user):
            raise Http404()
        pet_type = PetType.objects.filter(title=serializer.data.get('pet_type')).exists()
        if not pet_type:
            raise Http404()

        pet.name = serializer.data.get('name')
        pet.age = serializer.data.get('age')
        pet.pet_type = PetType.objects.get(title=serializer.data.get('pet_type'))
        pet.save()

        return Response(
            {'success': True, 'message': f'{messages.UPDATE_SUCCESS}'},
            status=status.HTTP_200_OK)
