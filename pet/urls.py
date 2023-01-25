from django.urls import path
from .views import *

urlpatterns = [
    path('pet_create/',
         PetCreateAPIView.as_view(),
         name='pet_create'),


]