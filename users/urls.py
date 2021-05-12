from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('concluir/', views.concluir_registo, name='cl'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout1, name='logout'),
    path('consultar/', views.consultar_utilizadors.as_view(), name='consultarutilizadores')
]
