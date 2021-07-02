from django.shortcuts import render, redirect
from django.urls import reverse
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from evento import views as ev
from inscricao.forms import InserirInscricao
from evento.models import (Evento, Inscricao as inscricao, Opcoes, Pergunta, TipoDePergunta, Respostas)
from inscricao.tables import InscricaoTable, InscricaoTableProponente, InscricaoTableProponenteValidados
from inscricao.filters import InscricaoFilter
from django.utils.html import format_html
import datetime


def criarinscricao(request, pk_test):
    if not Evento.objects.filter(pk=pk_test).exists():
        return render(request, 'inscricao/mensagem.html',
                      {'tipo': 'error', 'm': 'Evento não existe', 'link': 'recursos-home'})
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
                                    participanteutilizadorid=participanteutilizadorid_r, datainscricao=datainscricao_r,
                                    estado=1, presenca=0)
            Inscricao_r.save()

            for key in fields_final:
                if key == 'requer_certificado':
                    continue
                if key == 'inscricao':
                    continue

                pergunta = Pergunta.objects.get(titulo=key)
                resposta = Respostas(texto=fields_final.get(key), perguntaid=pergunta, opcoesid=None,
                                     inscricaoid=Inscricao_r,
                                     eventoid=evento_id_r)
                resposta.save()
            return render(request, 'inscricao/mensagem.html',
                          {'tipo': 'success', 'm': 'Inscrição feita com sucesso', 'link': 'recursos-home'})
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

            return render(request, 'inscricao/inscricao.html',
                          {'form': form, 'forms': forms, 'pk_test': pk_test, 'participante': request.user.username,
                           'recursos': Evento.objects.get(pk=pk_test)})
    else:
        return render(request, 'inscricao/mensagem.html',
                      {'tipo': 'error', 'm': 'Realizar o login primeiro', 'link': 'recursos-home'})


class viewinscricao(SingleTableMixin, FilterView):
    ''' Consultar as inscricoes do participante que se encontra no sistema '''
    table_class = InscricaoTable
    template_name = 'inscricao/viewinscricao.html'
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

        return render(request, 'inscricao/alterarinscricao.html',
                      {'aproved': aproved, 'respostas': dict, 'button': button, 'id': id})
    else:
        return render(request, 'inscricao/mensagem.html',
                      {'tipo': 'error', 'm': 'Esta inscrição não foi feita por si', 'link': 'recursos-home'})


def viewInscricaoporValidar(request, id):
    if request.user.is_authenticated:
        if Evento.objects.get(id=id).proponenteutilizadorid.id == request.user.id:
            table = InscricaoTableProponente(inscricao.objects.filter(eventoid=id))
            table.request = request
            table.paginate(page=request.GET.get("page", 1), per_page=10)
            return render(request, 'inscricao/viewinscricao2.html', {'table': table})
        else:
            return render(request, 'inscricao/mensagem.html',
                          {'tipo': 'error', 'm': 'Este recursos não foi proposto por si', 'link': 'recursos-home'})
    else:
        return render(request, 'inscricao/mensagem.html',
                      {'tipo': 'error', 'm': 'Realizar Login primeiro', 'link': 'login'})


def validarInscricao(request, id):
    if inscricao.objects.get(id=id).eventoid.proponenteutilizadorid.id != request.user.id:
        redirect(ev.homepage)
    if id == None:
        redirect(ev.homepage)
    inscricao2 = inscricao.objects.get(id=id)
    dict = {}
    for resposta in Respostas.objects.all().filter(inscricaoid=inscricao2):
        dict.update({resposta.perguntaid.titulo: resposta})

    return render(request, 'inscricao/validarInscricao.html', {'inscricao': inscricao2, 'respostas': dict})


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
        return redirect(reverse('viewinscricaomeuevento', kwargs={'id': id}))
    else:
        return redirect(ev.homepage)


def viewinscricaoValidadas(request, id):
    if request.user.is_authenticated:
        if Evento.objects.get(id=id).proponenteutilizadorid.id == request.user.id:
            table = InscricaoTableProponenteValidados(inscricao.objects.filter(estado=2, eventoid=id))
            table.request = request
            table.paginate(page=request.GET.get("page", 1), per_page=10)
            return render(request, 'inscricao/inscricoesvalidadas.html', {'table': table})
        else:
            return render(request, 'inscricao/mensagem.html',
                          {'tipo': 'error', 'm': 'Este recursos não foi proposto por si', 'link': 'recursos-home'})
    else:
        return render(request, 'inscricao/mensagem.html',
                      {'tipo': 'error', 'm': 'Realizar Login primeiro', 'link': 'login'})


def apagarinscricao(request, id):
    if request.user.is_authenticated:
        for resposta in Respostas.objects.all().filter(inscricaoid=id):
            resposta.delete()
        inscricao.objects.filter(id=id).delete()
        return render(request, 'inscricao/mensagem.html',
                      {'tipo': 'success', 'm': 'Inscrição Cancelada com Sucesso', 'link': 'viewinscricao'})
    else:
        return render(request, 'inscricao/mensagem.html', {'tipo': 'error', 'm': 'Realizar o login primeiro'})


def checkin(request, id):
    if (request.user.is_authenticated):
        inscricao1 = inscricao.objects.get(id=id)
        inscricao1.presenca = 1
        inscricao1.save()
    id = inscricao.objects.get(id=id).eventoid.id
    return redirect(reverse('inscricaovalidadas', kwargs={'id': id}))


def checkout(request, id):
    if (request.user.is_authenticated):
        inscricao.objects.filter(id=id).update(presenca=0)
        id = inscricao.objects.get(id=id).eventoid.id
        return redirect(reverse('inscricaovalidadas', kwargs={'id': id}))
