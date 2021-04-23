from django.urls import path
from .views import (
    SalaCreateView,
    home,
    consultar_salas,
    apagar_sala,
)
from . import views

urlpatterns = [
    path('',home,name ='home'),
    path('sala/new/',SalaCreateView , name='criar_sala'),
    path('consultarsalas', consultar_salas.as_view(), name='consultar-salas'),
    path('apagarsala/<int:id>', apagar_sala, name = 'apagar-sala'),
]