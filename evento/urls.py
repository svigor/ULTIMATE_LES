from django.urls import path
from .views import (
    SalaCreateView,
    home,
)
from . import views

urlpatterns = [
    path('',home,name ='home'),
    path('sala/new/',SalaCreateView , name='criar_sala'),
]