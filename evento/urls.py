from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homepage, name='evento-home'),
    path('criarevento/', views.criarevento, name='evento-criar'),
    path('atr_opcao/', views.atr_opcao, name='atr_opcao'),
    path('concluir/', views.concluir_pre_evento, name='concluir'),
    path('consultar/', views.consultar_evento.as_view(), name='consultar'),
    path('mudarevento/<int:id>/', views.mudar_evento, name='mudarevento'),
    path('mudar_evento_concluir/', views.mudar_evento_concluir, name="mudar_evento2"),
    path('meus_eventos/', views.meus_eventos.as_view(), name='meus_eventos'),
    path('apagar_evento/<int:id>', views.apagar_evento, name='apagar_evento'),
    path('editar_evento/<int:id>', views.editar_evento, name='editar_evento'),
    path('editar_final/', views.editar_final, name='editar_final'),
    path('criarlogistica1/<int:id>', views.criar_logistica1, name='criar-logistica1'),
    path('criarlogistica2/', views.criar_logistica2, name='criar-logistica2'),
    path('criarlogistica3/', views.criar_logistica3, name='criar-logistica3'),
    path('visualizarlogistica2/<int:id>', views.visualizar_logistica2, name='visualizar-logistica2'),
    path('adicionar_recurso_logistica/<int:id>/<int:tipo>', views.adicionar_recurso_logistica,
         name='adicionar_recurso_logistica'),
    path('apagar_recurso_logistica/<int:id>', views.apagar_recurso_logistica, name='apagar_recurso_logistica'),
    path('alterar_recurso_logistica/<int:id>', views.alterar_recurso_logistica, name='alterar_recurso_logistica'),
    path('validar_logistica/<int:id>', views.validar_logistica, name='validar_logistica'),
    path('consultarlogisticas/', views.consultar_logisticas.as_view(), name='consultar_logisticas'),
    path('apagarlogisticas/<int:id>', views.apagar_logistica, name='apagar-logistica'),
    path('eventosaprovados/', views.consultareventosaprovado.as_view(), name='eventos-aprovados'),
    path('getnot/', views.getnotif, name='getnotifications'),
    path('seenotify/<int:id>', views.seemessage, name='seenotify'),
    path('responder/<int:id>', views.responde, name='responde')
]
