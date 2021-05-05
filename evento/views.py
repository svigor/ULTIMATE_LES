from django.shortcuts import render, redirect
from django.views.generic import ListView
from django_tables2 import SingleTableView
from .tables import consultarEvento
from django.template.defaultfilters import register
from django.contrib.sessions.backends.base import SessionBase

from .forms import opcaoevento, r_a_form, r_c_form, n_tel, c_s_form, r_c_form_dis, InserirSalaForm
from .models import TipoDeEvento, Formulario, Pergunta, TipoDePergunta, Campus, Evento, TipoDeFormulario, Edificio, Sala


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
            value = request.POST.get(values)
            fields_final.update({values: value})
        print(fields_final)
        campus = Campus.objects.get(nome=fields_final.get('Campus'))
        print(campus)
        evnt = TipoDeEvento.objects.get(pk=fields_final.get('tipodeevento'))
        tipo_form = TipoDeFormulario.objects.get(nome='Inscrição')
        inscricao_form = Formulario.objects.get(tipo_de_eventoid=evnt, tipo_de_formularioid=tipo_form)
        evento1 = Evento(capacidade=fields_final.get('Lotação'), aprovado='0', dia=fields_final.get('Dia'),
                         hora_de_inicio=fields_final.get('Hora De Inicio'), duracao=fields_final.get('Duração'),
                         campusid=campus, formularioinscricaoid=inscricao_form, formulariofeedbackid=None,
                         proponenteutilizadorid=request.user, tipo_de_eventoid=evnt)
        evento1.save()
        return render(request, 'evento/concluir_pre-evento.html')


class consultar_evento(SingleTableView):
    model = Evento
    table_class = consultarEvento
    template_name = 'evento/consultar_eventos.html'
    extra_context = {'Campus': Campus.objects.all(), 'Tipo': TipoDeEvento.objects.all()}



def SalaCreateView(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        if Sala.objects.filter(nome = request.POST.get('nome')).exists():
            return render(request,'evento/mensagem.html',{'tipo':'error','m':'A sala com esse nome já existe','link':'consultar-salas'})
        # create a form instance and populate it with data from the request:
        form = InserirSalaForm(request.POST, request.FILES)
        # check whether it's valid:
      
       
        if form.is_valid():
            edificio_id_r = request.POST.get('edificioid')
            Edificio_r = Edificio.objects.get(pk=edificio_id_r)
            ##Edificio_r = Edificio.objects.filter(pk=edificio_id_r)

            capacidade_r = request.POST.get('capacidade')
            #fotos_r = request.POST.get('fotos')
            fotosw = request.FILES.get('fotos')
            nome_r = request.POST.get('nome')
            mobilidade_reduzida_r = request.POST.get('mobilidade_reduzida')
            mobilidade_reduzida_r = 0
            
            if request.POST.get('mobilidade_reduzida') == 'on':
                mobilidade_reduzida_r = 1

            Sala_r = Sala(capacidade=capacidade_r, fotos=fotosw, nome=nome_r,
                          mobilidade_reduzida=mobilidade_reduzida_r,edificioid=Edificio_r)
            Sala_r.save()
            return render(
                request,
                'evento/mensagem.html',
                {
                    'tipo':'success',
                    'm':'A sala foi criada com o sucesso',
                    'link':'consultar-salas'
                }
            )

    # if a GET (or any other method) we'll create a blank form
    else:
        form = InserirSalaForm()

    return render(request, 'evento/criar_sala.html', {'form': form})

def load_edificios(request):
    campus_id = request.GET.get('campus')
    edificios = Edificio.objects.filter(campusid=campus_id).order_by('nome')
    print("CAMPUSID", campus_id)
    print("EDIFICIOS ",edificios)
    return render(request, 'evento/edificios_dropdown_list.html', {'edificios': edificios})
