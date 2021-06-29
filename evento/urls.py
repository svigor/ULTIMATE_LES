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
    path('alterarequipamento/<int:id>', views.alterar_equipamento, name='alterar-equipamento'),
    path('consultarequipamentos/', views.consultar_equipamentos.as_view(), name='consultar-equipamentos'),
    path('apagarequipamento/<int:id>', views.apagar_equipamento, name='apagar-equipamento'),

    
    path('criarlogistica1/',views.criar_logistica1, name='criar-logistica1'),
    path('criarlogistica2/',views.criar_logistica2, name='criar-logistica2'),
    path('criarlogistica3/',views.criar_logistica3, name='criar-logistica3'),
    path('visualizarlogistica2/<int:id>',views.visualizar_logistica2,name='visualizar-logistica2'),
    path('adicionar_recurso_logistica/<int:id>/<int:tipo>', views.adicionar_recurso_logistica, name='adicionar_recurso_logistica'),
    path('apagar_recurso_logistica/<int:id>', views.apagar_recurso_logistica,name='apagar_recurso_logistica'), 
    path('alterar_recurso_logistica/<int:id>', views.alterar_recurso_logistica,name='alterar_recurso_logistica')
]
