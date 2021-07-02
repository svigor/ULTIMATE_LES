from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.consultar_formularios.as_view(), name='consultar-formularios'),
    path('consultarperguntas/<int:id>', views.show_perguntas, name='consultar-perguntas-formulario'),
    path('apagarformulario/<int:id>', views.apagar_form, name='apagar-form'),
    path('perguntas/', views.consultar_perguntas.as_view(), name='consultar-perguntas'),
    path('apagarpergunta/<int:id>', views.apagar_pergunta, name='apagar-pergunta'),
    path('perguntas/<int:id>', views.show_opcoes, name='consultar-opcoes'),
    path('new/', views.criar_formulario, name='criar-formulario'),
    path('alterar/<int:id>', views.alterar_formulario, name='alterar-formulario'),
    path('removerpergunta/<int:id>', views.remover_pergunta, name='remover-pergunta'),
    path('perguntas/new', views.criar_pergunta, name='criar-pergunta'),
    path('perguntas/alterar/<int:id>', views.alterar_pergunta, name='alterar-pergunta'),
    path('removeropcao/<int:id>', views.remover_opcao, name='remover-opcao'),
    path('disponibilizarformulario/<int:id>', views.disponibilizar_formulario, name='disponibilizar-formulario'),
]
