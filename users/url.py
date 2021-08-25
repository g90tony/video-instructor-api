from .views import RegisterAPI
from .views import LoginAPI
from django.urls import path
from django.urls import path


urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
]
