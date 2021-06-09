from django.shortcuts import render, redirect
from urllib.parse import urlencode
from django.urls import reverse
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.views.generic import ListView
from users.models import MyUser
from evento.forms import InserirInscricao, c_s_form
from evento.models import (Evento, Formulario, Inscricao as inscricao, Opcoes, Pergunta, TipoDePergunta, Respostas)
from django.contrib.auth import *
from evento.tables import EventoTable, InscricaoTable, InscricaoTableProponente, InscricaoTableProponenteValidados
from evento.filters import InscricaoFilter
from django.db.models import Q
from django.template.defaultfilters import register
from django.contrib.sessions.backends.base import SessionBase
from django.utils.html import format_html

import datetime




def homepage(request):
    return render(request, 'evento/inicio.html')   

def criarinscricao(request, pk_test):
    if not Evento.objects.filter(pk=pk_test).exists():
        return render(request, 'evento/mensagem.html', {'tipo':'error', 'm':'Evento não existe', 'link':'homepage'})
    if request.user.is_authenticated:

    # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            dict = []
            fields_final = {}
            for field in request.POST:
                dict.append(field)
            for values in dict:
                if values == 'csrfmiddlewaretoken':
                    continue
                value = request.POST.get(values)
                fields_final.update({values: value})


            evento_id_r = Evento.objects.get(pk=pk_test)
            participanteutilizadorid_r = request.user
            datainscricao_r = datetime.date.today()
            requer_certificado_r = 0
            if request.POST.get('requer_certificado') == 'on':
                requer_certificado_r = 1
            Inscricao_r = inscricao(eventoid=evento_id_r, requer_certificado=requer_certificado_r,
                                    participanteutilizadorid=participanteutilizadorid_r, datainscricao=datainscricao_r, estado=1, presenca=0)         
            Inscricao_r.save()
            

            for key in fields_final:
                print(key)
                if key == 'requer_certificado':
                    continue
                if key == 'inscricao':
                    continue
                
                pergunta = Pergunta.objects.get(titulo=key)
                resposta = Respostas(texto=fields_final.get(key), perguntaid=pergunta, opcoesid=None, inscricaoid=Inscricao_r,
                                    eventoid=evento_id_r)
                resposta.save()
            return render(request, 'evento/mensagem.html', {'tipo':'success', 'm':'Inscrição feita com sucesso', 'link':'homepage'})
        # if a GET (or any other method) we'll create a blank form
        else:
            form = InserirInscricao()
            formulario = Evento.objects.get(id=pk_test).formularioinscricaoid.id
            perguntas = Pergunta.objects.all().filter(formularioid=formulario)

            pergunta_relat = {}
            for pergunta in perguntas:
                pergunta_relat.update({pergunta.titulo: TipoDePergunta.objects.get(pk=pergunta.tipo_de_perguntaid_id)})
            forms = {}
            for elem in pergunta_relat:
                if pergunta_relat[elem].nome == "Resposta Curta" or pergunta_relat[elem].nome == 'Resposta Aberta':
                    forms.update({elem.title(): pergunta_relat[elem].nome})
                elif pergunta_relat[elem].nome == 'Caixa de selecao':
                    forms.update({elem.title(): Opcoes.objects.filter(perguntaid=pergunta.id)})
                    
            return render(request, 'evento/inscricao.html', {'form': form, 'forms' : forms ,'pk_test':pk_test, 'participante':request.user.username, 'evento':Evento.objects.get(pk=pk_test)})
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

    def get_queryset(self):
        return inscricao.objects.filter(participanteutilizadorid=self.request.user.id)

def alterarinscricao(request, id):
    if request.user.is_authenticated and inscricao.objects.get(id=id).participanteutilizadorid.id == request.user.id:
        dict = {}
        aproved = inscricao.objects.get(id=id).estado
        button = format_html(f"""
                    <a onclick="clicked()"
                        data-tooltip="Editar">
                        <button type="submit" class="button is-info is-outlined">
                                <span>Editar</span>
                            </button>
                    </a>""")
        for resposta in Respostas.objects.all().filter(inscricaoid=id):
            dict.update({resposta.perguntaid.titulo: resposta})
        if request.method == 'POST':
            dict = []
            fields_final = {}
            for field in request.POST:
                dict.append(field)
            for values in dict:
                if values == 'csrfmiddlewaretoken':
                    continue
                value = request.POST.get(values)
                fields_final.update({values: value})

            for key in fields_final:
                print(key)
                if key == 'requer_certificado':
                    continue
                if key == 'inscricao':
                    continue
                
                Respostas.objects.all().filter(inscricaoid=id).update(texto=fields_final.get(key))
            return redirect('viewinscricao')
        
        return render(request, 'evento/alterarinscricao.html', {'aproved': aproved, 'respostas': dict, 'button': button, 'id' : id})
    else:
        return render(request, 'evento/mensagem.html', {'tipo':'error', 'm':'Esta inscrição não foi feita por si', 'link':'homepage'})
    


def viewInscricaoporValidar(request, id):
    if request.user.is_authenticated:
        if Evento.objects.get(id=id).proponenteutilizadorid.id == request.user.id:
            table = InscricaoTableProponente(inscricao.objects.filter(eventoid=id))
            table.request = request
            table.paginate(page=request.GET.get("page", 1), per_page=10)
            return render(request, 'evento/viewinscricao2.html', {'table' : table}) 
        else:
            return render(request, 'evento/mensagem.html', {'tipo':'error', 'm':'Este evento não foi proposto por si', 'link':'homepage'})
    else:
        return render(request, 'evento/mensagem.html', {'tipo':'error', 'm':'Realizar Login primeiro', 'link':'login'})

def validarInscricao(request, id):
    if inscricao.objects.get(id=id).eventoid.proponenteutilizadorid.id != request.user.id:
        redirect(homepage)
    if id == None:
        redirect(homepage)
    inscricao2 = inscricao.objects.get(id=id)
    dict = {}
    for resposta in Respostas.objects.all().filter(inscricaoid=inscricao2):
        dict.update({resposta.perguntaid.titulo: resposta})

    return render(request, 'evento/validarInscricao.html', {'inscricao': inscricao2, 'respostas': dict})

def finalizarvalidacao(request):
    if request.method == 'POST':
        decision = request.POST.get('decision')
        decision_bool = 0
        inscricaoid = request.POST.get('idinscricao')
        inscricao_r = inscricao.objects.get(id=inscricaoid)
        if decision == 'Aprovado':
            decision_bool = 2
        elif decision == 'Não aprovado':
            decision_bool = 3
        inscricao_r.estado = decision_bool
        inscricao_r.save()
        id = inscricao_r.eventoid.id
        return redirect(reverse('viewinscricaomeuevento', kwargs={'id':id}))
    else:
        return redirect(homepage)

def viewinscricaoValidadas(request, id):
    if request.user.is_authenticated:
        if Evento.objects.get(id=id).proponenteutilizadorid.id == request.user.id:
            table = InscricaoTableProponenteValidados(inscricao.objects.filter(estado=2, eventoid=id))
            table.request = request
            table.paginate(page=request.GET.get("page", 1), per_page=10)
            return render(request, 'evento/inscricoesvalidadas.html', {'table' : table})
        else:
            return render(request, 'evento/mensagem.html', {'tipo':'error', 'm':'Este evento não foi proposto por si', 'link':'homepage'})
    else:
        return render(request, 'evento/mensagem.html', {'tipo':'error', 'm':'Realizar Login primeiro', 'link':'login'})



def apagarinscricao(request, id):
    if request.user.is_authenticated:
        for resposta in Respostas.objects.all().filter(inscricaoid=id):
            resposta.delete()
        inscricao.objects.filter(id=id).delete()
        return render(request, 'evento/mensagem.html', {'tipo':'success', 'm':'Inscrição Cancelada com Sucesso', 'link':'viewinscricao'})
    else:
        return render(request, 'evento/mensagem.html', {'tipo':'error', 'm':'Realizar o login primeiro'})

def checkin(request, id):
    if(request.user.is_authenticated):
        inscricao.objects.filter(id=id).update(presenca=1)
        id = inscricao.objects.get(id=id).eventoid.id
        return redirect(reverse('inscricaovalidadas', kwargs={'id':id}))

def checkout(request, id):
    if(request.user.is_authenticated):
        inscricao.objects.filter(id=id).update(presenca=0)
        id = inscricao.objects.get(id=id).eventoid.id
        return redirect(reverse('inscricaovalidadas', kwargs={'id':id}))
# Create your views here.