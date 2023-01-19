from django.urls import path
from .views import CheckUserStatusAPIView

urlpatterns = [
    path('CheckUserStatus', CheckUserStatusAPIView.as_view(), name='check_user_status'),
]
