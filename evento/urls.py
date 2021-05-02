from django.urls import path
from .views import (
    SalaCreateView,
    home,
    consultar_salas,
    apagar_sala,
    alterar_sala,
    load_edificios,
    criar_servico
)
from evento import views

urlpatterns = [
    path('',home,name ='home'),
    path('sala/new/',SalaCreateView , name='criar_sala'),
    path('consultarsalas', consultar_salas.as_view(), name='consultar-salas'),
    path('apagarsala/<int:id>', apagar_sala, name = 'apagar-sala'),
    path('alterar/<int:id>', alterar_sala, name = 'alterar-sala'),

    path('ajax/load-edificios/', views.load_edificios, name='ajax_load_edificios'),

    path('servico/new/',criar_servico, name='criar_servico')
]