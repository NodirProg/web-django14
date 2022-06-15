from django.urls import path

from .views import register 

app_name="userprofile"
urlpatterns = [
    path('register/', register, name='register'),
]