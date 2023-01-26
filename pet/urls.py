from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', PetListViewSet)

urlpatterns = [
    path('pet_create/',
         PetCreateAPIView.as_view(),
         name='pet_create'),

    path('', include(router.urls))
]
