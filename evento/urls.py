from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='evento-home'),
    path('criarevento/', views.criarevento, name='evento-criar'),
    path('atr_opcao/', views.atr_opcao, name='atr_opcao'),
    path('concluir/', views.concluir_pre_evento, name='concluir'),
    path('consultar/', views.consultar_evento.as_view(), name='consultar'),
]
