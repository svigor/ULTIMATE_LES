from django.shortcuts import render, redirect
from .forms import opcaoevento, r_a_form, r_c_form, n_tel
from .models import TipoDeEvento, Formulario, Pergunta, TipoDePergunta, Campus


def homepage(request):
    return render(request, 'evento/homepage.html')


def criarevento(request):
    title = 'Criar Evento'
    opcoes = 'Escolha o Tipo de Evento'
    form_opcao = opcaoevento()
    return render(request, 'evento/criarevento.html', {'title': title, 'opcoes': opcoes, 'form': form_opcao})


def atr_opcao(request):
    if not request.POST.get('nome'):
        return redirect(criarevento)
    elif request.method == 'POST':
        form = opcaoevento(request.POST)
        if form.is_valid():
            tipodeevento = request.POST.get('nome')
            opcao = TipoDeEvento.objects.get(pk=tipodeevento)
            formulario = Formulario.objects.get(tipo_de_eventoid=opcao)
            perguntas = Pergunta.objects.all().filter(formularioid=formulario)
            pergunta_relat = {}
            for pergunta in perguntas:
                pergunta_relat.update({pergunta.titulo: TipoDePergunta.objects.get(pk=pergunta.tipo_de_perguntaid_id)})

            forms = {}
            for elem in pergunta_relat:
                if pergunta_relat[elem].nome == "Resposta Curta":
                    if elem.title() == 'Nº De Telefone':
                        print('cona')
                        r_c = n_tel()
                    else:
                        r_c = r_c_form()
                    forms.update({elem.title() + ":": r_c})
                elif pergunta_relat[elem].nome == "Resposta Aberta":
                    r_a = r_a_form()
                    forms.update({elem.title() + ":": r_a})
                elif pergunta_relat[elem].nome == "Caixa de Seleção":
                    c_s = 'ola'
                    forms.update({elem.title() + ":" + '_1': c_s})

            opcoes = 'Preencha o Formulário'
            title = 'Criar Eventos'
            return render(request, 'evento/criarevento2.html', {'title': title, 'opcoes': opcoes, 'forms': forms})
