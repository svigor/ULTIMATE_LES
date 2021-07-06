import datetime
import json
from json import JSONEncoder

from django.forms import formset_factory, model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.html import format_html

from .forms import opcaoevento, c_s_form, ValidarLogistica, LogisticaOpcoesForm_3, LogisticaOpcoesForm_2, \
    LogisticaOpcoesForm_1, i_s_form
from .models import TipoDeEvento, Formulario, Pergunta, TipoDePergunta, Campus, Evento, TipoDeFormulario, Respostas, \
    Sala, PeriodoSala, Servicos, PeriodoServico, Equipamento, Periodo_logistica, Logistica, TipoServico, \
    TipoEquipamento, TiposDeRecursos, Notificacoes
from .tables import consultarEvento, meuseventos as me, LogisticaTable, consultarEventosaprovados
from users.models import MyUser
from .filters import eventofilter, LogisticasFilter
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin


def homepage(request):
    return render(request, 'evento/homepage.html')


def criarevento(request):
    if request.user.is_authenticated and (
            request.user.role.role == 'Proponente' or request.user.role.role == 'Administrador'):
        title = 'Criar Evento'
        opcoes = 'Escolha o Tipo de Evento'
        form_opcao = opcaoevento()
        return render(request, 'evento/criarevento.html', {'title': title, 'opcoes': opcoes, 'form': form_opcao})
    else:
        return redirect(homepage)


def atr_opcao(request):
    global formulario
    if not request.POST.get('nome'):
        return redirect(criarevento)
    elif request.method == 'POST':
        form = opcaoevento(request.POST)
        if form.is_valid():
            tipodeevento = request.POST.get('nome')
            opcao = TipoDeEvento.objects.get(pk=tipodeevento)
            tipo_formulario = TipoDeFormulario.objects.get(nome='Evento')

            try:
                formulario = Formulario.objects.get(tipo_de_eventoid=opcao, tipo_de_formularioid=tipo_formulario)
            except Formulario.DoesNotExist:
                return render(request, 'evento/mensagem.html',
                              {'tipo': 'error', 'm': 'Não existe Formulário para este tipo de Evento',
                               'link': 'evento-home'})
            if formulario.disponibilidade == 0:
                return render(request, 'evento/mensagem.html',
                              {'tipo': 'error', 'm': 'Não existe Formulário para este tipo de Evento',
                               'link': 'evento-home'})
            else:
                perguntas = Pergunta.objects.all().filter(formularioid=formulario)
                pergunta_relat = {}
                for pergunta in perguntas:
                    pergunta_relat.update(
                        {pergunta.titulo: TipoDePergunta.objects.get(pk=pergunta.tipo_de_perguntaid_id)})

                forms = {}
                for elem in pergunta_relat:
                    if pergunta_relat[elem].nome == "Resposta Curta" or pergunta_relat[elem].nome == 'Resposta Aberta':
                        forms.update({elem.title(): pergunta_relat[elem].nome})
                    elif pergunta_relat[elem].nome == 'Caixa de Seleção':
                        forms.update({elem.title(): c_s_form})

                opcoes = 'Preencha o Formulário'
                title = 'Criar Eventos'
                inscriform = i_s_form()

                return render(request, 'evento/criarevento2.html',
                              {'title': title, 'opcoes': opcoes, 'forms': forms, 'tipo': tipodeevento,
                               'inscform': inscriform})


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
        divide = fields_final.get('inscricaoform')
        divided = divide.split()
        fo = Formulario.objects.get(id=divided[1])
        nome_do_evento = fields_final.get('Nome Do Evento')
        diafinal = fields_final.get('Dia Final')
        evnt = TipoDeEvento.objects.get(pk=fields_final.get('tipodeevento'))
        evento1 = Evento(capacidade=fields_final.get('Lotação'), nome=nome_do_evento, aprovado=0,
                         dia=fields_final.get('Dia'), diaFinal=diafinal,
                         hora_de_inicio=fields_final.get('Hora De Início'),
                         duracao=fields_final.get('Duração Do Evento'),
                         campusid=campus, formularioinscricaoid=fo, formulariofeedbackid=None,
                         proponenteutilizadorid=request.user, tipo_de_eventoid=evnt)
        evento1.save()
        tipo_form = TipoDeFormulario.objects.get(nome='Evento')
        for key in fields_final:
            if key == 'tipodeevento' or key == 'inscricaoform':
                continue
            formu = Formulario.objects.get(tipo_de_eventoid=evnt, tipo_de_formularioid=tipo_form)
            pergunta = Pergunta.objects.get(titulo=key, formularioid=formu)
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
                Evento.objects.all().filter(proponenteutilizadorid=request.user.pk,
                                            tipo_de_eventoid=tipo_de_eventoid,
                                            aprovado=aprovado, campusid=campusid))
            table.filterset_class = filter
            table.paginate(page=request.GET.get("page", 1), per_page=10)
            return render(request, 'evento/consultar_meus_eventos.html', {'table': table, 'filter': filter})


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
    evento = Evento.objects.get(id=id)
    aproved = evento.aprovado
    conf = 'Deseja mesmo Editar o evento'
    button = format_html(f"""
                <a onclick="mostrar()">
                    <button type=button class= "button is-success">Editar</button>
                </a>""")
    for resposta in Respostas.objects.all().filter(eventoid=id):
        dict.update({resposta.perguntaid.titulo: resposta})
    return render(request, 'evento/mudar_meu_evento.html',
                  {'aproved': aproved, 'respostas': dict, 'button': button, 'evento': evento.id})


def editar_final(request):
    if request.method == 'POST' and request.user.is_authenticated and request.user.id == request.session['id']:
        dic = request.POST.dict()
        even = Evento.objects.get(id=request.POST.get('evento'))
        for key, value in dic.items():
            if key == 'csrfmiddlewaretoken' or key == 'estado' or key == 'evento':
                continue
            else:
                ti = TipoDeFormulario.objects.get(nome='Evento')
                formu = Formulario.objects.get(tipo_de_eventoid=even.tipo_de_eventoid, tipo_de_formularioid=ti)
                respo = Respostas.objects.get(perguntaid=Pergunta.objects.get(titulo=key, formularioid=formu).id, eventoid=even.pk)
                respo.texto = value
                respo.save()
        even.duracao = request.POST.get('Duração Do Evento')
        even.campusid = Campus.objects.get(nome=request.POST.get('Campus'))
        even.capacidade = request.POST.get('Capacidade')
        even.dia = request.POST.get('Dia')
        even.capacidade = request.POST.get('Lotação')
        even.diaFinal = request.POST.get('Dia Final')
        even.nome = request.POST.get('Nome Do Evento')
        if request.POST.get('estado') == '1':
            even.aprovado = 0
        even.save()
        return redirect('meus_eventos')
    else:
        return redirect(homepage)


def criar_logistica1(request, id):
    ev1 = Evento.objects.get(id=id)
    if not request.user.is_authenticated or ev1.proponenteutilizadorid.id != request.user.id:
        return render(request, 'evento/mensagem.html', {'tipo': 'error', 'm': 'Não é permetido', 'link': 'evento-home'})

    if request.method == 'POST':
        form = LogisticaOpcoesForm_1(request.POST)

        if form.is_valid():
            yesnoSala = request.POST.get('yesnoSala')
            yesnoEquipamento = request.POST.get('yesnoEquipamento')
            yesnoServico = request.POST.get('yesnoServico')
            form2 = LogisticaOpcoesForm_2()

            ## é o id do evento
            ## Apaga se no futuro fica como argumento na função

            # id = 3

            return render(request,
                          'evento/criar_logistica2.html',
                          {'form2': form2,
                           'yesnoSala': yesnoSala,
                           'yesnoEquipamento': yesnoEquipamento,
                           'yesnoServico': yesnoServico,
                           'id': id
                           })
    else:
        form = LogisticaOpcoesForm_1()
    return render(request, 'evento/criar_logistica1.html', {'form': form, 'id': id})


def criar_logistica2(request):
    if not request.user.is_authenticated:
        return render(request, 'evento/mensagem.html', {'tipo': 'error', 'm': 'Não é permetido', 'link': 'evento-home'})

    if request.method == 'POST':
        form = LogisticaOpcoesForm_2(request.POST)

        if form.is_valid():
            id = request.POST.get('id')
            ev1 = Evento.objects.get(id=id)
            if ev1.proponenteutilizadorid.id != request.user.id:
                return render(request, 'evento/mensagem.html',
                              {'tipo': 'error', 'm': 'Não é permetido', 'link': 'evento-home'})
            numeroSalas = request.POST.get('numeroSalas')
            numeroEquipamentos = request.POST.get('numeroEquipamentos')
            numeroServicos = request.POST.get('numeroServicos')

            if (numeroSalas is None):
                numeroSalas = 0

            if (numeroEquipamentos is None):
                numeroEquipamentos = 0

            if (numeroServicos is None):
                numeroServicos = 0

            SalaFormSet = formset_factory(LogisticaOpcoesForm_3, extra=int(numeroSalas))
            EquipamentoFormSet = formset_factory(LogisticaOpcoesForm_3, extra=int(numeroEquipamentos))
            ServicoFormSet = formset_factory(LogisticaOpcoesForm_3, extra=int(numeroServicos))
            return render(request,
                          'evento/criar_logistica3.html',
                          {'id': request.POST.get('id'),
                           'form': SalaFormSet,
                           'form2': EquipamentoFormSet,
                           'form3': ServicoFormSet,
                           'numeroSalas': int(numeroSalas),
                           'numeroEquipamentos': int(numeroEquipamentos),
                           'numeroServicos': int(numeroServicos)
                           })
    else:
        form = LogisticaOpcoesForm_2()
    return render(request, 'evento/criar_logistica2.html', {'form': form})


def criar_logistica3(request):
    if not request.user.is_authenticated:
        return render(request, 'evento/mensagem.html', {'tipo': 'error', 'm': 'Não é permetido', 'link': 'evento-home'})

    SalaFormSet = formset_factory(LogisticaOpcoesForm_3)
    EquipamentoFormSet = formset_factory(LogisticaOpcoesForm_3)
    ServicoFormSet = formset_factory(LogisticaOpcoesForm_3)
    if request.method == 'POST':
        numeroSalas = request.POST.get('numeroSalas')
        numeroEquipamentos = request.POST.get('numeroEquipamentos')
        numeroServicos = request.POST.get('numeroServicos')
        form = SalaFormSet(request.POST, request.FILES)
        form2 = EquipamentoFormSet(request.POST, request.FILES)
        form3 = ServicoFormSet(request.POST, request.FILES)
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            id = request.POST.get('id')
            evento_object = Evento.objects.get(id=id)
            if evento_object.proponenteutilizadorid.id != request.user.id:
                return render(request, 'evento/mensagem.html',
                              {'tipo': 'error', 'm': 'Não é permetido', 'link': 'evento-home'})
            # logistica_object= Logistica.objects.get(eventoid=evento_object.id)
            # logistica_object.valido = 1
            logistica_object = Logistica(valido=0, eventoid=evento_object)
            logistica_object.save()
            if int(numeroSalas) > 0:
                for f in form:
                    cd = f.cleaned_data
                    dia_inicial = cd.get('dia_inicial')
                    dia_final = cd.get('dia_final')
                    hora_de_inicio = cd.get('hora_de_inicio')
                    hora_de_fim = cd.get('hora_de_fim')
                    capacidade = cd.get('capacidade')
                    recurso = TiposDeRecursos.objects.get(id=1)

                    newPeriodo = Periodo_logistica(logistica_id=logistica_object, tipos_de_recursosid=recurso,
                                                   dia_inicial=dia_inicial, dia_final=dia_final,
                                                   hora_de_inicio=hora_de_inicio, hora_de_fim=hora_de_fim,
                                                   capacidade=capacidade)
                    newPeriodo.save()
            if int(numeroEquipamentos) > 0:
                for f in form2:
                    cd = f.cleaned_data
                    dia_inicial = cd.get('dia_inicial')
                    dia_final = cd.get('dia_final')
                    hora_de_inicio = cd.get('hora_de_inicio')
                    hora_de_fim = cd.get('hora_de_fim')
                    tipo_equipamentoid = cd.get('tipo_equipamentoid')
                    recurso = TiposDeRecursos.objects.get(id=2)

                    newPeriodo = Periodo_logistica(logistica_id=logistica_object, tipos_de_recursosid=recurso,
                                                   dia_inicial=dia_inicial, dia_final=dia_final,
                                                   hora_de_inicio=hora_de_inicio, hora_de_fim=hora_de_fim, capacidade=0,
                                                   tipo_equipamentoid=tipo_equipamentoid)
                    newPeriodo.save()
            if int(numeroServicos) > 0:
                for f in form3:
                    print(form3)
                    cd = f.cleaned_data
                    dia_inicial = cd.get('dia_inicial')
                    dia_final = cd.get('dia_final')
                    hora_de_inicio = cd.get('hora_de_inicio')
                    hora_de_fim = cd.get('hora_de_fim')
                    capacidade = cd.get('capacidade')
                    tipo_de_servico = cd.get('tipo_de_servico')
                    recurso = TiposDeRecursos.objects.get(id=3)

                    newPeriodo = Periodo_logistica(logistica_id=logistica_object, tipos_de_recursosid=recurso,
                                                   dia_inicial=dia_inicial, dia_final=dia_final,
                                                   hora_de_inicio=hora_de_inicio, hora_de_fim=hora_de_fim,
                                                   capacidade=capacidade, tipo_servicoid=tipo_de_servico)
                    newPeriodo.save()
            return redirect(homepage)

    else:
        numeroSalas = request.POST.get('numeroSalas')
        numeroEquipamentos = request.POST.get('numeroEquipamentos')
        numeroServicos = request.POST.get('numeroServicos')
        EquipamentoFormSet = formset_factory(LogisticaOpcoesForm_3, extra=int(numeroEquipamentos))
        ServicoFormSet = formset_factory(LogisticaOpcoesForm_3, extra=int(numeroServicos))
        SalaFormSet = formset_factory(LogisticaOpcoesForm_3, extra=numeroSalas)

    return render(request, 'evento/criar_logistica3.html', {'form': SalaFormSet})


def visualizar_logistica2(request, id):
    if not request.user.is_authenticated or not request.user.role.role == 'Administrador':
        return render(request, 'evento/mensagem.html', {'tipo': 'error', 'm': 'Não é permetido', 'link': 'evento-home'})

    logistica_object = Logistica.objects.get(eventoid=id)
    recursos = Periodo_logistica.objects.filter(logistica_id=logistica_object)
    d = ValidarLogistica(initial={'decision': logistica_object.valido})

    if request.user.role.role == 'Administrador':
        role = 3
    else:
        role = 0
    return render(request, 'evento/visualizar_logistica.html', {'recursos': recursos, 'id': id, 'd': d, 'role': role})


def adicionar_recurso_logistica(request, id, tipo):
    if not request.user.is_authenticated or not request.user.role.role == 'Administrador':
        return render(request, 'evento/mensagem.html', {'tipo': 'error', 'm': 'Não é permetido', 'link': 'evento-home'})

    if request.method == 'POST':
        form = LogisticaOpcoesForm_3(request.POST)
        evento_object = Evento.objects.get(id=id)
        logistica_object = Logistica.objects.get(eventoid=evento_object)
        print(form.is_valid())

        if form.is_valid():

            if tipo == 1:
                dia_inicial = request.POST.get('dia_inicial')
                dia_final = request.POST.get('dia_final')
                hora_de_inicio = request.POST.get('hora_de_inicio')
                hora_de_fim = request.POST.get('hora_de_fim')
                capacidade = request.POST.get('capacidade')
                recurso = TiposDeRecursos.objects.get(id=1)
                newPeriodo = Periodo_logistica(logistica_id=logistica_object, dia_inicial=dia_inicial,
                                               dia_final=dia_final, hora_de_inicio=hora_de_inicio,
                                               hora_de_fim=hora_de_fim, capacidade=capacidade,
                                               tipos_de_recursosid=recurso)
                newPeriodo.save()
            if tipo == 2:
                dia_inicial = request.POST.get('dia_inicial')
                dia_final = request.POST.get('dia_final')
                hora_de_inicio = request.POST.get('hora_de_inicio')
                hora_de_fim = request.POST.get('hora_de_fim')
                tipo_equipamentoid = request.POST.get('tipo_equipamentoid')
                equipamento = TipoEquipamento.objects.get(id=tipo_equipamentoid)
                recurso = TiposDeRecursos.objects.get(id=2)

                newPeriodo = Periodo_logistica(logistica_id=logistica_object, tipos_de_recursosid=recurso,
                                               dia_inicial=dia_inicial, dia_final=dia_final,
                                               hora_de_inicio=hora_de_inicio, hora_de_fim=hora_de_fim, capacidade=0,
                                               tipo_equipamentoid=equipamento)
                newPeriodo.save()
            if tipo == 3:
                dia_inicial = request.POST.get('dia_inicial')
                dia_final = request.POST.get('dia_final')
                hora_de_inicio = request.POST.get('hora_de_inicio')
                hora_de_fim = request.POST.get('hora_de_fim')
                capacidade = request.POST.get('capacidade')
                tipo_de_servico = request.POST.get('tipo_de_servico')
                servico = TipoServico.objects.get(id=tipo_de_servico)
                recurso = TiposDeRecursos.objects.get(id=3)

                newPeriodo = Periodo_logistica(logistica_id=logistica_object, tipos_de_recursosid=recurso,
                                               dia_inicial=dia_inicial, dia_final=dia_final,
                                               hora_de_inicio=hora_de_inicio, hora_de_fim=hora_de_fim,
                                               capacidade=capacidade, tipo_servicoid=servico)
                newPeriodo.save()

            return redirect('/visualizarlogistica2/' + str(evento_object.id))

    else:
        form = LogisticaOpcoesForm_3()
    return render(request, 'evento/adicionar_logistica_recurso.html', {'f': form, 'tipo': tipo, 'id': id})


def apagar_recurso_logistica(request, id):
    if not request.user.is_authenticated or not request.user.role.role == 'Administrador':
        return render(request, 'evento/mensagem.html', {'tipo': 'error', 'm': 'Não é permetido', 'link': 'evento-home'})
    recurso_object = Periodo_logistica.objects.get(id=id)
    evento_id = recurso_object.logistica_id.eventoid.id
    Periodo_logistica.objects.filter(id=id).delete()
    # return render(request,'evento/mensagem.html',{'tipo':'success','m':'A equipamento foi apagado com o sucesso','link':'evento-home'})
    return redirect('/visualizarlogistica2/' + str(evento_id))


def alterar_recurso_logistica(request, id):
    if not request.user.is_authenticated or not request.user.role.role == 'Administrador':
        return render(request, 'evento/mensagem.html', {'tipo': 'error', 'm': 'Não é permetido', 'link': 'evento-home'})

    if request.method == 'POST':
        recurso_object = Periodo_logistica.objects.get(id=id)
        form = LogisticaOpcoesForm_3(request.POST, initial=
        {'capacidade': recurso_object.capacidade,
         'dia_inicial': recurso_object.dia_inicial,
         'dia_final': recurso_object.dia_final,
         'hora_de_inicio': recurso_object.hora_de_inicio,
         'hora_de_fim': recurso_object.hora_de_fim,
         'tipos_de_recursosid': recurso_object.tipos_de_recursosid,
         'tipo_equipamentoid': recurso_object.tipo_equipamentoid,
         'tipo_servicoid': recurso_object.tipo_servicoid
         })
        tipo = recurso_object.tipos_de_recursosid.id

        print("WALID: ", form.is_valid())
        if form.is_valid():
            print("TIPO: ", tipo)
            if tipo == 1:
                recurso_object.dia_inicial = request.POST.get('dia_inicial')
                recurso_object.dia_final = request.POST.get('dia_final')
                recurso_object.hora_de_inicio = request.POST.get('hora_de_inicio')
                recurso_object.hora_de_fim = request.POST.get('hora_de_fim')
                recurso_object.capacidade = request.POST.get('capacidade')
                recurso_object.save()
            if tipo == 2:
                recurso_object.dia_inicial = request.POST.get('dia_inicial')
                recurso_object.dia_final = request.POST.get('dia_final')
                recurso_object.hora_de_inicio = request.POST.get('hora_de_inicio')
                recurso_object.hora_de_fim = request.POST.get('hora_de_fim')
                tipo_equipamento = TipoEquipamento.objects.get(id=request.POST.get('tipo_equipamentoid'))
                recurso_object.tipo_equipamentoid = tipo_equipamento
                recurso_object.save()
            if tipo == 3:
                print("SERVICO: ", request.POST.get('tipo_de_servico'))
                recurso_object.dia_inicial = request.POST.get('dia_inicial')
                recurso_object.dia_final = request.POST.get('dia_final')
                recurso_object.hora_de_inicio = request.POST.get('hora_de_inicio')
                recurso_object.hora_de_fim = request.POST.get('hora_de_fim')
                recurso_object.capacidade = request.POST.get('capacidade')
                tipo_de_servico = TipoServico.objects.get(id=request.POST.get('tipo_de_servico'))
                recurso_object.tipo_servicoid = tipo_de_servico
                recurso_object.save()

            # return render(request,'evento/mensagem.html',{'tipo':'success','m':'O recurso foi alterado com o sucesso','link':'evento-home'})

            return redirect('/visualizarlogistica2/' + str(recurso_object.logistica_id.eventoid.id))

        else:
            msg = 'Preenche todos os campos corretamente'
            return render(
                request=request,
                template_name='evento/alterar_equipamento.html',
                context={
                    'f': form, 'm': msg, 'id': id, 'tipo': recurso_object.tipos_de_recursosid
                }
            )
    else:
        recurso_object = Periodo_logistica.objects.get(id=id)
        form = LogisticaOpcoesForm_3(initial=
                                     {'capacidade': recurso_object.capacidade,
                                      'dia_inicial': recurso_object.dia_inicial,
                                      'dia_final': recurso_object.dia_final,
                                      'hora_de_inicio': recurso_object.hora_de_inicio,
                                      'hora_de_fim': recurso_object.hora_de_fim,
                                      'tipos_de_recursosid': recurso_object.tipos_de_recursosid,
                                      'tipo_equipamentoid': recurso_object.tipo_equipamentoid,
                                      'tipo_servicoid': recurso_object.tipo_servicoid
                                      })
        return render(
            request,
            'evento/alterar_recurso_logistica.html',
            {'f': form, 'id': id, 'tipo': recurso_object.tipos_de_recursosid.id}
        )


def validar_logistica(request, id):
    if not request.user.is_authenticated or not request.user.role.role == 'Administrador':
        return render(request, 'evento/mensagem.html', {'tipo': 'error', 'm': 'Não é permetido', 'link': 'evento-home'})

    if request.method == 'POST':
        evento_object = Evento.objects.get(id=id)
        logistica_object = Logistica.objects.get(eventoid=evento_object)
        decision = request.POST.get('decision')
        form = ValidarLogistica(request.POST)
        print("DECISIO: ", request.POST.get('decision'))
        if form.is_valid():
            if decision == '1':
                logistica_object.valido = 1
                evento_object.aprovado = 2
            if decision == '0':
                logistica_object.valido = 0
            logistica_object.save()
            evento_object.save()
    else:
        evento_object = Evento.objects.get(id=id)
        logistica_object = Logistica.objects.get(eventoid=evento_object)
        logistica_object.valido = 1
        logistica_object.save()
        evento_object.aprovado = 2
        evento_object.save()
        return redirect('/consultar/')

    return redirect('/consultarlogisticas/')


class consultar_logisticas(SingleTableMixin, FilterView):
    table_class = LogisticaTable
    template_name = 'evento/consultar_logisticas.html'
    filterset_class = LogisticasFilter
    table_pagination = {
        'per_page': 10
    }

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.role.role == 'Administrador':
            return render(request, 'evento/mensagem.html',
                          {'tipo': 'error', 'm': 'Não é permetido', 'link': 'evento-home'})
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SingleTableMixin, self).get_context_data(**kwargs)
        table = self.get_table(**self.get_table_kwargs())
        table.request = self.request
        table.fixed = True
        context[self.get_context_table_name(table)] = table
        return context


def apagar_logistica(request, id):
    if not request.user.is_authenticated or not request.user.role.role == 'Administrador':
        return render(request, 'evento/mensagem.html', {'tipo': 'error', 'm': 'Não é permetido', 'link': 'evento-home'})

    logistica_object = Logistica.objects.get(id=id)
    evento1 = Evento.objects.get(id=logistica_object.eventoid.id)
    recursos = Periodo_logistica.objects.filter(logistica_id=logistica_object)
    recursos.delete()
    evento1.aprovado = 1
    evento1.save()
    logistica_object.delete()
    return render(request, 'evento/mensagem.html',
                  {'tipo': 'success', 'm': 'A logistica foi apagada com o sucesso', 'link': 'consultar_logisticas'})


class consultareventosaprovado(SingleTableMixin, FilterView):
    table_class = consultarEventosaprovados
    table_data = Evento.objects.all().filter(aprovado=2)
    template_name = 'evento/consultareventosaprovados.html'
    filterset_class = eventofilter
    table_pagination = {
        'per_page': 100
    }


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def getnotif(request):
    queryset = Notificacoes.objects.filter(recetor=request.user)
    lista = queryset.values_list()
    listainside = list(lista.values())
    for mensagens in range(0, len(listainside)):
        for items in listainside[mensagens]:
            if items == 'emissor_id':
                id = listainside[mensagens][items]
                user = MyUser.objects.get(id=id)
                value = str(id) + " " + str(user.email)
                listainside[mensagens][items] = value
            if items == 'recetor_id':
                id = listainside[mensagens][items]
                user = MyUser.objects.get(id=id)
                value = str(id) + " " + user.email
                listainside[mensagens][items] = value
    return JsonResponse({'notifications': listainside})


def seemessage(request, id):
    notification = Notificacoes.objects.get(id=id)
    if notification.recetor.id != request.user.id or not request.user.is_authenticated:
        return redirect(homepage)
    else:
        notification.viewed = 1
        notification.save()
        return render(request, 'evento/seenotify.html', {'mensagem': notification})


def responde(request, id):
    if not request.user.is_authenticated:
        return redirect(homepage)
    if request.method == 'POST':
        notification = Notificacoes.objects.get(id=id)
        recetor = notification.emissor
        emissor = request.user
        mensagem = Notificacoes(recetor=recetor, emissor=emissor, descricao=request.POST.get('mensagem futura'),
                                criadoem=datetime.datetime.now(), viewed=0)
        mensagem.save()
        return render(request, 'evento/mensagem.html',
                      {'tipo': 'success', 'm': 'Mensagem enviado com sucesso', 'link': 'evento-home'})
    else:
        notifcation = Notificacoes.objects.get(id=id)
        return render(request, 'evento/respond_notify.html', {'recetor': notifcation})
