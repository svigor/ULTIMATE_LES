from django.urls import path
from .views import (
    SalaCreateView,
    apagar_pergunta,
    home,
    consultar_salas,
    apagar_sala,
    alterar_sala,
    load_edificios,
    consultar_formularios,
    show_perguntas,
    apagar_form,
    consultar_perguntas,
    show_opcoes,
)
from evento import views

urlpatterns = [
    path('',home,name ='home'),
    path('sala/new/',SalaCreateView , name='criar_sala'),
    path('consultarsalas', consultar_salas.as_view(), name='consultar-salas'),
    path('apagarsala/<int:id>', apagar_sala, name = 'apagar-sala'),
    path('alterar/<int:id>', alterar_sala, name = 'alterar-sala'),
    path('formularios/', consultar_formularios.as_view(), name='consultar-formularios'),
    path('formularios/<int:id>', show_perguntas, name='consultar-perguntas-formulario'), 
    path('apagarformulario/<int:id>', apagar_form, name='apagar-form'),
    path('perguntas/', consultar_perguntas.as_view(), name='consultar-perguntas'),
    path('apagarpergunta/<int:id>', apagar_pergunta, name='apagar-pergunta'),
    path('perguntas/<int:id>', show_opcoes, name='consultar-opcoes'),

    path('ajax/load-edificios/', views.load_edificios, name='ajax_load_edificios'),
]