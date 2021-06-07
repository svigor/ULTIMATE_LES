from django.shortcuts import render, redirect, get_object_or_404
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.views.generic import ListView
from users.models import MyUser
from evento.forms import InserirInscricao
from evento.models import (Evento, Inscricao as inscricao)
from django.contrib.auth import *
from evento.tables import EventoTable, InscricaoTable, InscricaoTableProponente, InscricaoTableProponenteValidados
from evento.filters import InscricaoFilter
from django.db.models import Q
from django.template.defaultfilters import register
from django.contrib.sessions.backends.base import SessionBase

import datetime




def homepage(request):
    return render(request, 'evento/inicio.html')


# def vieweventos(request):
#     context = {
#         'eventos' : Evento.objects.all()
#     }
#     return render(request, 'evento/vieweventos.html', context)    

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
                estado_r = 1
                requer_certificado_r = 0
                if request.POST.get('requer_certificado') == 'on':
                    requer_certificado_r = 1
                Inscricao_r = inscricao(eventoid=evento_id_r, requer_certificado=requer_certificado_r,
                                        participanteutilizadorid=participanteutilizadorid_r, datainscricao=datainscricao_r, estado=1)
                Inscricao_r.save()
                return render(request, 'evento/mensagem.html', {'tipo':'success', 'm':'Inscrição feita com sucesso', 'link':'homepage'})
            else:
                return redirect(criarinscricao)

        # if a GET (or any other method) we'll create a blank form
        else:
            form = InserirInscricao()
            return render(request, 'evento/inscricao.html', {'form': form, 'pk_test':pk_test, 'participante':request.user.username, 'evento':Evento.objects.get(pk=pk_test)})
    else:
        return render(request, 'evento/mensagem.html', {'tipo':'error', 'm':'Realizar o login primeiro', 'link':'homepage'})

class vieweventos(SingleTableMixin, ListView):
    table_class = EventoTable
    template_name = 'evento/vieweventos.html'
    table_pagination = {
        'per_page': 10
    }

    def get_queryset(self):
        return Evento.objects.all()

class viewinscricao(SingleTableMixin, FilterView):
    ''' Consultar as inscricoes do participante que se encontra no sistema '''
    table_class = InscricaoTable
    template_name = 'evento/viewinscricao.html'
    filterset_class = InscricaoFilter
    table_pagination = {
        'per_page': 10
    }

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request,'evento/mensagem.html', {'tipo':'error', 'm':'Realizar o login primeiro', 'link':'login'})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return inscricao.objects.filter(participanteutilizadorid=self.request.user.id)


def viewInscricaoporValidar(request, id):
    if request.user.is_authenticated:
        table = InscricaoTableProponente(inscricao.objects.filter(eventoid=id))
        table.request = request
        table.paginate(page=request.GET.get("page", 1), per_page=10)
        return render(request, 'evento/viewinscricao2.html', {'table' : table}) 
    else:
        return render(request, 'evento/mensagem.html', {'tipo':'error', 'm':'Realizar Login primeiro', 'link':'login'})


def viewinscricaoValidadas(request, id):
    if request.user.is_authenticated:
        table = InscricaoTableProponenteValidados(inscricao.objects.filter(estado=2, eventoid=id))
        table.request = request
        table.paginate(page=request.GET.get("page", 1), per_page=10)
        return render(request, 'evento/inscricoesvalidadas.html', {'table' : table})
    else:
        return render(request, 'evento/mensagem.html', {'tipo':'error', 'm':'Realizar Login primeiro', 'link':'login'})








def apagarinscricao(request, id):
    if request.user.is_authenticated:
        inscricao.objects.filter(id=id).delete()
        return render(request, 'evento/mensagem.html', {'tipo':'success', 'm':'Inscrição Cancelada com Sucesso', 'link':'viewinscricao'})
    else:
        return render(request, 'evento/mensagem.html', {'tipo':'error', 'm':'Realizar o login primeiro'})

def checkin(request, id):
    if(request.user.is_authenticated):
        inscricao.objects.filter(id=id).update(presenca=1)
        return redirect('inscricaovalidadas')

def checkout(request, id):
    if(request.user.is_authenticated):
        inscricao.objects.filter(id=id).update(presenca=0)
        return redirect('inscricaovalidadas')
# Create your views here.