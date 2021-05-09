from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='evento-home'),
    path('criarevento/', views.criarevento, name='evento-criar'),
    path('atr_opcao/', views.atr_opcao, name='atr_opcao'),
    path('concluir/', views.concluir_pre_evento, name='concluir'),
    path('consultar/', views.consultar_evento.as_view(), name='consultar'),

    path('criarsala/',views.SalaCreateView , name='criar_sala'),
    path('consultarsalas/', views.consultar_salas.as_view(), name='consultar-salas'),
    path('apagarsala/<int:id>', views.apagar_sala, name = 'apagar-sala'),
    path('alterarsala/<int:id>', views.alterar_sala, name = 'alterar-sala'),
    path('ajax/load-edificios/', views.load_edificios, name='ajax_load_edificios'),
    
    path('criarservico/', views.criar_servico, name='criar-servico'),
    path('consultarservicos/', views.consultar_servicos.as_view(), name='consultar-servicos'),
    path('apagarservico/<int:id>', views.apagar_sevico, name='apagar-servico'),
    path('alterarservico/<int:id>', views.alterar_servico, name='alterar-servico'),

    path('criarequipamento/', views.criar_equipamento, name='criar-equipamento'),
]
