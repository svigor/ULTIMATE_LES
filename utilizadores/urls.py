from django.urls import path, include
from .views import consultar_utilizadores
from .views import escolher_perfil
from .views import criar_utilizador
from .views import concluir_registo
from .views import home
from .views import login_action
from .views import logout_action
from .views import alterar_password

from . import views

app_name = 'utilizadores'


urlpatterns = [
    path('consultarutilizadores', consultar_utilizadores.as_view(),name='consultar-utilizadores'), #
    path('escolherperfil', escolher_perfil,name='escolher-perfil'),    
    path('criarutilizadores/<int:id>', criar_utilizador, name='criar-utilizador'), #
    path('alterarpassword',alterar_password,name='alterar-password'), #

    path('validarutilizador/<int:id>', views.validar_utilizador,name='validar-utilizador'),
    path('rejeitarutilizador/<int:id>', views.rejeitar_utilizador,name='rejeitar-utilizador'),
    path('alteraridioma', views.alterar_idioma,name='alterar-idioma'),


    path('concluirregisto/<int:id>', concluir_registo,name='concluir-registo'), #
    path("logout", logout_action, name="logout"), # 
    path("login", login_action, name="login"),   #





]       
