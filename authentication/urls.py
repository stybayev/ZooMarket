from authentication.views import (
    RegisterView, LoginAPIView,
    PetCreateAPIView, UserDetailView, LogoutAPIView,
)
from django.urls import path

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

]
