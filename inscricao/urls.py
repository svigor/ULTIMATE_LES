from django.urls import path
from . import views

urlpatterns = [
    path('inscrever/<int:pk_test>', views.criarinscricao, name='criarinscricao'),
    path('', views.viewinscricao.as_view(), name='viewinscricao'),
    path('inscricao/alterarinscricao/<int:id>', views.alterarinscricao, name='alterarinscricao'),
    path('inscricao-no-meu-evento/<int:id>', views.viewInscricaoporValidar, name='viewinscricaomeuevento'),
    path('validarinscricao/<int:id>', views.validarInscricao, name='validarInscricao'),
    path('finalizarvalidacaoinscricao', views.finalizarvalidacao, name='finalizarvalidacao'),
    path('inscricao-no-meu-evento-validada/<int:id>/', views.viewinscricaoValidadas, name='inscricaovalidadas'),

    path('inscricao/<int:id>', views.apagarinscricao, name='apagarinscricao'),
    path('checkout/<int:id>', views.checkout, name='checkout'),
    path('checkin/<int:id>', views.checkin, name='checkin'),
]
