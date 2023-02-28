from .models import Pet, PetType
from rest_framework import serializers


class PetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetType
        fields = ['title', ]


class PetCreateSerializer(serializers.ModelSerializer):
    pet_type = serializers.CharField()

    class Meta:
        model = Pet
        fields = ['name', 'age', 'pet_type']
        read_only_fields = ['user', ]


class PetListSerializer(serializers.ModelSerializer):
    pet_type = PetTypeSerializer()

    class Meta:
        model = Pet
        fields = ['id', 'name', 'age', 'pet_type']
        read_only_fields = ['user', ]


class PetUpdateSerializer(serializers.ModelSerializer):
    pet_type = serializers.CharField()

    class Meta:
        model = Pet
        fields = ['name', 'age', 'pet_type']
        read_only_fields = ['user', ]
