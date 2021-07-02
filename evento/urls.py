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
]
