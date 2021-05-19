from django.shortcuts import render, redirect, get_object_or_404
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.views.generic import ListView
from users.models import MyUser
from evento.forms import InserirInscricao, AlterarInscricao
from evento.models import (Evento, Inscricao)
from django.contrib.auth import *
from evento.tables import InscricaoTable, InscricaoTableProponente
from evento.filters import InscricaoFilter
from django.template.defaultfilters import register
from django.contrib.sessions.backends.base import SessionBase

import datetime




def homepage(request):
    return render(request, 'evento/inicio.html')


def vieweventos(request):
    context = {
        'eventos' : Evento.objects.all()
    }
    return render(request, 'evento/vieweventos.html', context)    

def criarinscricao(request, pk_test):
    if not Evento.objects.filter(pk=pk_test).exists():
        return render(request, 'evento/mensagem.html', {'tipo':'error', 'm':'Evento não existe', 'link':'homepage'})
    if request.user.is_authenticated:

    # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = InserirInscricao(request.POST)
            # check whether it's valid:
            if form.is_valid():
                evento_id_r = Evento.objects.get(pk=pk_test)
                participanteutilizadorid_r = request.user
                datainscricao_r = datetime.date.today()
                requer_certificado_r = 0
                if request.POST.get('requer_certificado') == 'on':
                    requer_certificado_r = 1
                # Inscricao_r = Inscricao(eventoid=evento_id_r, requer_certificado=requer_certificado_r,
                #                         participanteutilizadorid=participanteutilizadorid_r, datainscricao=datainscricao_r)
                # Inscricao_r.save()
                # return render(request, 'evento/mensagem.html', {'tipo':'success', 'm':'Inscrição feita com sucesso', 'link':'homepage'})
            else:
                return redirect(criarinscricao)

        # if a GET (or any other method) we'll create a blank form
        else:
            form = InserirInscricao()
            return render(request, 'evento/inscricao.html', {'form': form, 'pk_test':pk_test, 'participante':request.user.username, 'evento':Evento.objects.get(pk=pk_test)})
    else:
        return render(request, 'evento/mensagem.html', {'tipo':'error', 'm':'Realizar o login primeiro', 'link':'homepage'})

class viewinscricao(SingleTableMixin, FilterView):
    ''' Consultar as inscricoes do participante que se encontra no sistema '''
    table_class = InscricaoTable
    template_name = 'evento/viewinscricao.html'
    filterset_class = InscricaoFilter
    table_pagination = {
        'per_page': 10
    }

    def get_queryset(self):
        if self.request.user.is_authenticated:
            print(self.request.user.id)
            return Inscricao.objects.filter(participanteutilizadorid=self.request.user.id)


class viewinscricaoProponente(SingleTableMixin, FilterView):
    ''' Consultar as inscricoes por parte do Proponente apenas para o seus eventos '''
    table_class = InscricaoTableProponente
    template_name = 'evento/viewinscricao2.html'
    filterset_class = InscricaoFilter
    table_pagination = {
        'per_page': 10
    }

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role.role == 'Proponente':
            return Inscricao.objects.filter(eventoid__in=Evento.objects.filter(proponenteutilizadorid=self.request.user.id))


def apagarinscricao(request, id):
    if request.user.is_authenticated:
        Inscricao.objects.filter(id=id).delete()
        return render(request, 'evento/mensagem.html', {'tipo':'success', 'm':'Inscrição Cancelada com Sucesso', 'link':'viewinscricao'})
    else:
        return render(request, 'evento/mensagem.html', {'tipo':'error', 'm':'Realizar o login primeiro'})

def alterarinscricao(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            forms = AlterarInscricao(request.POST)
            if forms.is_valid():
                presenca_r = 0
                if request.POST.get('presenca') == 'on':
                    presenca_r = 1
                Inscricao.objects.filter(id=id).update(presenca=presenca_r)
                return render(request, 'evento/mensagem.html', {'tipo':'success', 'm':'Inscrição alterada com sucesso', 'link':'viewinscricao'})
            else:
                return redirect(alterarinscricao)
        else:
            forms = AlterarInscricao()
            return render(request, 'evento/alterarinscricao.html', {'forms': forms, 'id':id})
# Create your views here.