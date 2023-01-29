from authentication.views import (
    RegisterView, LoginAPIView,
    UserDetailView, LogoutAPIView, UpdateProfileView, DeleteUserView,
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

    path('user_update/',
         UpdateProfileView.as_view(),
         name='user_update'),

    path('delete_user/',
         DeleteUserView.as_view(),
         name='delete_user')
]
