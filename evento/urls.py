from django.urls import path
from evento.views import (checkin, homepage, vieweventos, criarinscricao, viewinscricao, apagarinscricao, 
							viewInscricaoporValidar, viewinscricaoValidadas, checkout, validarInscricao, finalizarvalidacao, alterarinscricao)
from evento import views

urlpatterns = [
	path('', homepage, name='homepage'),
	path('eventos/', vieweventos.as_view(), name='vieweventos'),
	path('eventos/inscricao/<int:pk_test>', criarinscricao, name='criarinscricao'),
	path('inscricao/', viewinscricao.as_view(), name='viewinscricao'),
	path('inscricao/alterarinscricao/<int:id>', alterarinscricao, name='alterarinscricao'),
	path('eventos/inscricao-no-meu-evento/<int:id>', viewInscricaoporValidar, name='viewinscricaomeuevento'),
	path('eventos/validarinscricao/<int:id>', validarInscricao, name='validarInscricao'),
	path('eventos/finalizarvalidacaoinscricao', finalizarvalidacao, name='finalizarvalidacao'),
	path('eventos/inscricao-no-meu-evento-validada/<int:id>/', viewinscricaoValidadas, name='inscricaovalidadas'),
	
	path('inscricao/<int:id>', apagarinscricao, name='apagarinscricao'),
	path('checkout/<int:id>', checkout, name='checkout'),
	path('checkin/<int:id>', checkin, name='checkin'),
]