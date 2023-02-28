from django.urls import path, include

from authentication.views import PetTypeApiView
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', PetListViewSet)

urlpatterns = [
    path('pet_create/',
         PetCreateAPIView.as_view(),
         name='pet_create'),

    path('', include(router.urls)),

    path('pet_update/<int:pet_id>/',
         PetUpdateView.as_view(),
         name='pet_update'),

    path('pet_type_list/',
         PetTypeApiView.as_view(),
         name='pet_type_list'),

]
