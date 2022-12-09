from authentication.views import RegisterView, LoginAPIView
from django.urls import path

urlpatterns = [
    path('register/',
         RegisterView.as_view(),
         name='user_registration'),

    path('login/',
         LoginAPIView.as_view(),
         name='user_login'),

]
