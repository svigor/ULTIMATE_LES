from django.urls import path
from .views import (
    SalaCreateView,
    home,
    CriarFormularioView,
)
from . import views

urlpatterns = [
    path('',home,name ='home'),
    path('sala/new/',SalaCreateView , name='criar_sala'),
    path('formulario/new/', CriarFormularioView, name='criar_formulario')
]