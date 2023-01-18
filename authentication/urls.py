from authentication.views import (
    RegisterView, LoginAPIView,
    PetCreateAPIView, UserDetailView, LogoutAPIView, VerifyPhoneView,
)
from django.urls import path
from django.urls import path, include
from .views import UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('register/',
         RegisterView.as_view(),
         name='user_registration'),

    path('login/',
         LoginAPIView.as_view(),
         name='user_login'),

    path('pet_create/',
         PetCreateAPIView.as_view(),
         name='pet_create'),

    path('user_detail/',
         UserDetailView.as_view(),
         name='user_detail'),

    path('logout/',
         LogoutAPIView.as_view(),
         name='logout'),

    path('phone_verify/',
         VerifyPhoneView.as_view(),
         name='phone_verify'),

    path('login_firebase/', include(router.urls)),

]
