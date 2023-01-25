from authentication.views import (
    RegisterView, LoginAPIView,
    UserDetailView, LogoutAPIView, VerifyPhoneView,
)

from django.urls import path

urlpatterns = [
    path('register/<int:user_id>/',
         RegisterView.as_view(),
         name='user_registration'),

    path('login/',
         LoginAPIView.as_view(),
         name='user_login'),

    path('user_detail/',
         UserDetailView.as_view(),
         name='user_detail'),

    path('logout/',
         LogoutAPIView.as_view(),
         name='logout'),

    path('phone_verify/',
         VerifyPhoneView.as_view(),
         name='phone_verify'),
]
