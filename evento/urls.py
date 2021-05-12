from django.urls import path
from .views import (
    SalaCreateView,
    home,
    consultar_salas,
    apagar_sala,
    alterar_sala,
    load_edificios,
    consultar_formularios,
    show_perguntas,
    apagar_form
)
from evento import views

urlpatterns = [
    path('',home,name ='home'),
    path('sala/new/',SalaCreateView , name='criar_sala'),
    path('consultarsalas', consultar_salas.as_view(), name='consultar-salas'),
    path('apagarsala/<int:id>', apagar_sala, name = 'apagar-sala'),
    path('alterar/<int:id>', alterar_sala, name = 'alterar-sala'),
    path('consultarformularios/', consultar_formularios.as_view(), name='consultar-formularios'),
    path('consultarperguntasformulario/<int:id>', show_perguntas, name='consultar-perguntas-formulario'), 
    path('apagarformulario/<int:id>', apagar_form, name='apagar-form'),

    path('ajax/load-edificios/', views.load_edificios, name='ajax_load_edificios'),
]