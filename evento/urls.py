from django.urls import path
from .views import (
    SalaCreateView,
    alterar_pergunta,
    apagar_pergunta,
    criar_formulario,
    disponibilizar_formulario,
    home,
    consultar_salas,
    apagar_sala,
    alterar_sala,
    load_edificios,
    consultar_formularios,
    remover_pergunta,
    show_perguntas,
    apagar_form,
    consultar_perguntas,
    show_opcoes,
    alterar_formulario,
    criar_pergunta,
    remover_opcao
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
    path('formularios/new', criar_formulario, name='criar-formulario'),
    path('formularios/alterar/<int:id>', alterar_formulario, name='alterar-formulario'),
    path('removerpergunta/<int:id>', remover_pergunta, name='remover-pergunta'),
    path('perguntas/new', criar_pergunta, name='criar-pergunta'),
    path('perguntas/alterar/<int:id>', alterar_pergunta, name='alterar-pergunta'),
    path('removeropcao/<int:id>', remover_opcao, name='remover-opcao'),
    path('disponibilizarformulario/<int:id>', disponibilizar_formulario, name='disponibilizar-formulario'),

    path('ajax/load-edificios/', views.load_edificios, name='ajax_load_edificios'),
]