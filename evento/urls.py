from django.urls import path
from evento.views import (homepage, vieweventos, criarinscricao, viewinscricao, apagarinscricao, alterarinscricao, viewinscricaoProponente)
from evento import views

urlpatterns = [
	path('', homepage, name='homepage'),
	path('eventos/', vieweventos, name='vieweventos'),
	path('eventos/inscricao/<int:pk_test>', criarinscricao, name='criarinscricao'),
	path('inscricao/', viewinscricao.as_view(), name='viewinscricao'),
	path('eventos/inscricao-no-meu-evento', viewinscricaoProponente.as_view(), name='viewinscricaomeuevento'),
	path('inscricao/<int:id>', apagarinscricao, name='apagarinscricao'),
	path('inscricao2/<int:id>', alterarinscricao, name='alterarinscricao'),
]