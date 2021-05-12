from django.shortcuts import render, redirect
from django.urls import reverse
from django_filters.views import FilterView
from .filters import eventofilter
from django_tables2 import SingleTableMixin
from django.utils.html import format_html
from .tables import consultarEvento, meuseventos as me
from .forms import opcaoevento, r_a_form, r_c_form, n_tel, c_s_form, r_c_form_dis
from .models import TipoDeEvento, Formulario, Pergunta, TipoDePergunta, Campus, Evento, TipoDeFormulario, Respostas


def homepage(request):
    return render(request, 'evento/homepage.html')


def criarevento(request):
    print(request.user.role.role)
    if request.user.is_authenticated and (
            request.user.role.role == 'Proponente' or request.user.role.role == 'Administrador'):
        title = 'Criar Evento'
        opcoes = 'Escolha o Tipo de Evento'
        form_opcao = opcaoevento()
        return render(request, 'evento/criarevento.html', {'title': title, 'opcoes': opcoes, 'form': form_opcao})
    else:
        return redirect(homepage)


def atr_opcao(request):
    if not request.POST.get('nome'):
        return redirect(criarevento)
    elif request.method == 'POST':
        form = opcaoevento(request.POST)
        if form.is_valid():
            tipodeevento = request.POST.get('nome')
            opcao = TipoDeEvento.objects.get(pk=tipodeevento)
            tipo_formulario = TipoDeFormulario.objects.get(nome='pré-evento')
            formulario = Formulario.objects.get(tipo_de_eventoid=opcao, tipo_de_formularioid=tipo_formulario)
            perguntas = Pergunta.objects.all().filter(formularioid=formulario)
            pergunta_relat = {}
            for pergunta in perguntas:
                pergunta_relat.update({pergunta.titulo: TipoDePergunta.objects.get(pk=pergunta.tipo_de_perguntaid_id)})

            forms = {}
            for elem in pergunta_relat:
                if pergunta_relat[elem].nome == "Resposta Curta" or pergunta_relat[elem].nome == 'Resposta Aberta':
                    forms.update({elem.title(): pergunta_relat[elem].nome})
                elif pergunta_relat[elem].nome == 'Caixa de Seleção':
                    forms.update({elem.title(): c_s_form})

            opcoes = 'Preencha o Formulário'
            title = 'Criar Eventos'

            return render(request, 'evento/criarevento2.html',
                          {'title': title, 'opcoes': opcoes, 'forms': forms, 'tipo': tipodeevento})


def concluir_pre_evento(request):
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
        campus = Campus.objects.get(nome=fields_final.get('Campus'))
        nome_do_evento = fields_final.get('Nome Do Evento')
        evnt = TipoDeEvento.objects.get(pk=fields_final.get('tipodeevento'))
        tipo_form = TipoDeFormulario.objects.get(nome='Inscrição')
        inscricao_form = Formulario.objects.get(tipo_de_eventoid=evnt, tipo_de_formularioid=tipo_form)
        evento1 = Evento(capacidade=fields_final.get('Lotação'), nome=nome_do_evento, aprovado='0',
                         dia=fields_final.get('Dia'),
                         hora_de_inicio=fields_final.get('Hora De Inicio'),
                         duracao=fields_final.get('Duração Do Evento'),
                         campusid=campus, formularioinscricaoid=inscricao_form, formulariofeedbackid=None,
                         proponenteutilizadorid=request.user, tipo_de_eventoid=evnt)
        evento1.save()

        for key in fields_final:
            if key == 'tipodeevento':
                continue
            pergunta = Pergunta.objects.get(titulo=key)
            resposta = Respostas(texto=fields_final.get(key), perguntaid=pergunta, opcoesid=None, inscricaoid=None,
                                 eventoid=evento1)
            resposta.save()

        return render(request, 'evento/concluir_pre-evento.html')


class consultar_evento(SingleTableMixin, FilterView):
    model = Evento
    table_class = consultarEvento
    template_name = 'evento/consultar_eventos.html'
    filterset_class = eventofilter
    table_pagination = {'per_page': 10}
    valuer = chr(40) + chr(39) + chr(39) + chr(44) + chr(39) + chr(45) + chr(45) + chr(45) + chr(45) + chr(45) + chr(
        45) + chr(45) + chr(45) + chr(45) + chr(39) + chr(41)
    extra_context = {'valuer': valuer}


def mudar_evento(request, id):
    if request.user.role.role != 'Administrador':
        return redirect(homepage)
    if id == None:
        return redirect(homepage)
    evento = Evento.objects.get(id=id)
    dict = {}
    for resposta in Respostas.objects.all().filter(eventoid=evento):
        dict.update({resposta.perguntaid.titulo: resposta})

    return render(request, 'evento/mudar_evento.html', {'evento': evento, 'respostas': dict})


def mudar_evento_concluir(request):
    if request.method == 'POST':
        decision = request.POST.get('decision')
        decision_bool = 0
        eventoid = request.POST.get('idevento')
        evento = Evento.objects.get(id=eventoid)
        if decision == 'Aprovado':
            decision_bool = 1
        elif decision == 'Não aprovado':
            decision_bool = 0
        evento.aprovado = decision_bool
        evento.save()
        return redirect('/consultar/')
    else:
        return redirect(homepage)


def apagar_evento(request, id):
    if request.user.is_authenticated and (request.user.id != request.session['id']):
        return redirect(homepage)
    for resposta in Respostas.objects.all().filter(eventoid=id):
        resposta.delete()
    evento = Evento.objects.get(id=id)
    evento.delete()
    return redirect('meus_eventos')


def editar_evento(request, id):
    if request.user.is_authenticated and (request.user.id != request.session['id']):
        return redirect(homepage)
    dict = {}
    aproved = Evento.objects.get(id=id).aprovado
    conf = 'Deseja mesmo Editar o evento'
    button = format_html(f"""
                <a onclick="clicked()"
                    data-tooltip="Apagar">
                    <button type=button class= "button is-success">Editar</button>
                </a>""")
    for resposta in Respostas.objects.all().filter(eventoid=id):
        dict.update({resposta.perguntaid.titulo: resposta})
    return render(request, 'evento/mudar_meu_evento.html', {'aproved': aproved, 'respostas': dict, 'button': button})

def editar_final(request):
    if request.method == 'POST':
        print(request.POST)
    else:
        print('falhou')




class meus_eventos(SingleTableMixin, FilterView):
    model = Evento

    def get(self, request, *args, **kwargs):
        if not bool(request.GET.dict()):
            filter = eventofilter(request.GET,
                                  queryset=Evento.objects.all().filter(proponenteutilizadorid=request.user.pk))
            table = me(Evento.objects.all().filter(proponenteutilizadorid=request.user.pk))
            table.filterset_class = filter
            table.paginate(page=request.GET.get("page", 1), per_page=10)
            return render(request, 'evento/consultar_meus_eventos.html', {'table': table, 'filter': filter})
        else:
            filter = eventofilter(request.GET,
                                  queryset=Evento.objects.all().filter(proponenteutilizadorid=request.user.pk))
            tipo_de_eventoid = request.GET.get('tipo_de_eventoid')
            aprovado = request.GET.get('aprovado')
            campusid = request.GET.get('campusid')
            table = me(
                Evento.objects.all().filter(proponenteutilizadorid=request.user.pk, tipo_de_eventoid=tipo_de_eventoid,
                                            aprovado=aprovado, campusid=campusid))
            table.filterset_class = filter
            table.paginate(page=request.GET.get("page", 1), per_page=10)
            return render(request, 'evento/consultar_meus_eventos.html', {'table': table, 'filter': filter})
