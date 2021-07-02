from django.shortcuts import render, redirect
from formularios.forms import CriarFormularioForm, AlterarFormularioForm, CriarPerguntaForm, AlterarPerguntaForm

from django_tables2 import SingleTableMixin
from django.views.generic import (
    ListView,
)
from evento.models import Evento, Opcoes, Formulario, Pergunta, TipoDeEvento, TipoDeFormulario, TipoDePergunta
from formularios.tables import PerguntaTable, FormularioTable


# Create your views here.


class consultar_formularios(SingleTableMixin, ListView):
    model = Formulario
    table_class = FormularioTable
    template_name = 'formularios/consultar_formularios.html'
    table_pagination = {'per_page': 10}


def show_perguntas(request, id):
    if not Formulario.objects.filter(id=id):
        redirect('consultar-formularios')
    perguntas = {}
    for pergunta in Pergunta.objects.all().filter(formularioid=id):
        perguntas.update({pergunta.titulo: pergunta.tipo_de_perguntaid.nome})
    tipo = Formulario.objects.get(pk=id)
    return render(request, 'formularios/visualizar_formulario.html', {'perguntas': perguntas, 'tipo': tipo})


def apagar_form(request, id):
    if not Evento.objects.filter(formularioinscricaoid=Formulario.objects.get(id=id)) and not Evento.objects.filter(
            formulariofeedbackid=Formulario.objects.get(id=id)):
        Pergunta.objects.filter(formularioid=id).update(formularioid=None)
        Formulario.objects.filter(id=id).delete()
        return render(request, 'formularios/mensagem.html',
                      {'tipo': 'success', 'm': 'O formulário foi apagado com sucesso', 'link': 'consultar-formularios'})
    else:
        return render(request, 'formularios/mensagem.html',
                      {'tipo': 'error', 'm': 'O formulário não pôde ser apagado', 'link': 'consultar-formularios'})


class consultar_perguntas(SingleTableMixin, ListView):
    model = Pergunta
    table_class = PerguntaTable
    template_name = 'formularios/consultar_perguntas.html'
    table_pagination = {'per_page': 10}


def show_opcoes(request, id):
    if not Pergunta.objects.filter(id=id):
        return redirect('consultar-perguntas')
    tipo_pergunta = Pergunta.objects.get(id=id).tipo_de_perguntaid.nome
    # print(tipo_pergunta)
    if tipo_pergunta != "Caixa de seleção" and tipo_pergunta != "Escolha múltipla":
        return redirect('consultar-perguntas')
    opcoes = {}
    i = 0
    for opcao in Opcoes.objects.all().filter(perguntaid=id):
        opcoes.update({i: opcao.texto})
        i += 1
    tipo = Pergunta.objects.get(pk=id)
    return render(request, 'formularios/visualizar_pergunta.html', {'opcoes': opcoes, 'tipo': tipo})


def apagar_pergunta(request, id):
    if not Pergunta.objects.filter(id=id):
        return redirect('consultar-perguntas')

    p = Pergunta.objects.get(id=id)
    if not p.formularioid == None:
        formulario = p.formularioid
        if not Evento.objects.filter(formularioinscricaoid=formulario) and not Evento.objects.filter(
                formulariofeedbackid=formulario):
            Opcoes.objects.filter(perguntaid=id).delete()
            Pergunta.objects.filter(id=id).delete()
            # Pergunta.objects.filter(formularioid=id).update(formularioid=None)
            # Formulario.objects.filter(id=id).delete()
            return render(request, 'formularios/mensagem.html',
                          {'tipo': 'success', 'm': 'A pergunta foi apagada com sucesso', 'link': 'consultar-perguntas'})
        else:
            return render(request, 'formularios/mensagem.html',
                          {'tipo': 'error', 'm': 'A pergunta não pôde ser apagada', 'link': 'consultar-perguntas'})
    else:
        Opcoes.objects.filter(perguntaid=id).delete()
        Pergunta.objects.filter(id=id).delete()
        return render(request, 'formularios/mensagem.html',
                      {'tipo': 'success', 'm': 'A pergunta foi apagada com sucesso', 'link': 'consultar-perguntas'})


def criar_formulario(request):
    if request.method == 'POST':
        form = CriarFormularioForm(request.POST)

        if form.is_valid:
            tipo_form_r = request.POST.get('tipo_form')
            Tipo_Form_r = TipoDeFormulario.objects.get(pk=tipo_form_r)
            pergunta_r = request.POST.get('pergunta')
            Pergunta_r = Pergunta.objects.get(pk=pergunta_r)
            if Pergunta_r.formularioid != None:
                return render(
                    request,
                    'formularios/mensagem.html',
                    {
                        'tipo': 'error',
                        'm': 'A pergunta já está associada a um formulário!',
                        'link': 'consultar-formularios'
                    })

            if Tipo_Form_r.nome == 'Evento':
                tipo_evento_r = request.POST.get('tipo_evento')
                Tipo_Evento_r = TipoDeEvento.objects.get(pk=tipo_evento_r)
                if Formulario.objects.filter(tipo_de_formularioid=Tipo_Form_r).filter(tipo_de_eventoid=Tipo_Evento_r):
                    return render(
                        request,
                        'formularios/mensagem.html',
                        {
                            'tipo': 'error',
                            'm': 'O formulário não pôde ser criado',
                            'link': 'consultar-formularios'
                        })
                else:
                    Form_r = Formulario(tipo_de_formularioid=Tipo_Form_r, tipo_de_eventoid=Tipo_Evento_r,
                                        disponibilidade=0)
            else:
                Form_r = Formulario(tipo_de_formularioid=Tipo_Form_r, tipo_de_eventoid=None, disponibilidade=0)

            Form_r.save()
            Pergunta_r.formularioid = Form_r
            Pergunta_r.save()

            return render(
                request,
                'formularios/mensagem.html',
                {
                    'tipo': 'success',
                    'm': 'O formulário foi criado com o sucesso',
                    'link': 'consultar-formularios'
                }
            )

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CriarFormularioForm()

    return render(request, 'formularios/criar_formulario.html', {'form': form})


def alterar_formulario(request, id):
    try:
        form_object = Formulario.objects.get(id=id)
    except:
        return redirect('consultar-formulario')
    if Evento.objects.filter(formulariofeedbackid=form_object) or Evento.objects.filter(
            formularioinscricaoid=form_object):
        return render(request, 'formularios/mensagem.html',
                      {'tipo': 'error', 'm': 'O formulario já está associado a um recursos e não pode ser alterado.',
                       'link': 'consultar-formularios'})

    if request.method == 'POST':
        form_object = Formulario.objects.get(id=id)
        # submited_data = request.POST.copy()
        # form = AlterarSalaForm(submited_data, request.FILES.copy(), instance=sala_object)
        if form_object.tipo_de_eventoid != None:
            form = AlterarFormularioForm(initial={'tipo_form': form_object.tipo_de_formularioid.pk,
                                                  'tipo_evento': form_object.tipo_de_eventoid.pk})
        else:
            form = AlterarFormularioForm(initial={'tipo_form': form_object.tipo_de_formularioid.pk})

        erros = []

        if form.is_valid:

            tipo_form_r = request.POST.get('tipo_form')
            Tipo_Form_r = TipoDeFormulario.objects.get(pk=tipo_form_r)
            pergunta_r = request.POST.get('pergunta')

            if Tipo_Form_r.nome == 'Evento':
                tipo_evento_r = request.POST.get('tipo_evento')
                Tipo_Evento_r = TipoDeEvento.objects.get(pk=tipo_evento_r)
                form_object.tipo_de_eventoid = Tipo_Evento_r
                if Formulario.objects.filter(tipo_de_formularioid=Tipo_Form_r).filter(
                        tipo_de_eventoid=Tipo_Evento_r).exclude(id=id):
                    msg = "Já existe um formulário de eventos para esse tipo de recursos."
                    return render(request, 'formularios/alterar_formulario.html', {'msg': msg, 'id': id, 'form': form})
            else:
                form_object.tipo_de_eventoid = None

            if pergunta_r != '':
                Pergunta_r = Pergunta.objects.get(pk=pergunta_r)
                if Pergunta_r.formularioid == None:
                    Pergunta_r.formularioid = form_object
                    Pergunta_r.save()
                else:
                    msg = "A pergunta já está associada a um formulário!"
                    return render(request, 'formularios/alterar_formulario.html', {'msg': msg, 'id': id, 'form': form})

            form_object.tipo_de_formularioid = Tipo_Form_r
            form_object.save()
            return render(request, 'formularios/mensagem.html',
                          {'tipo': 'success', 'm': 'O formulário foi alterado com sucesso',
                           'link': 'consultar-formularios'})


        else:

            return render(
                request=request,
                template_name='formularios/alterar_formulario.html',
                context={
                    'form': form, 'msg': msg, 'erros': erros, 'id': id
                }
            )
    else:
        form_object = Formulario.objects.get(id=id)
        if form_object.tipo_de_eventoid != None:
            form = AlterarFormularioForm(initial={'tipo_form': form_object.tipo_de_formularioid.pk,
                                                  'tipo_evento': form_object.tipo_de_eventoid.pk})
        else:
            form = AlterarFormularioForm(initial={'tipo_form': form_object.tipo_de_formularioid.pk})
        # form = AlterarSalaForm(initial={'capacidade':sala_object.capacidade,'nome':sala_object.nome})
        # perguntas = {}
        perguntas = []
        for pergunta in Pergunta.objects.filter(formularioid=id):
            # perguntas.update({pergunta.titulo : pergunta.tipo_de_perguntaid.nome})
            perguntas.append(pergunta)
        return render(
            request,
            'formularios/alterar_formulario.html',
            {'form': form, 'id': id, 'perguntas': perguntas}

        )


def remover_pergunta(request, id):
    perg = Pergunta.objects.get(pk=id)
    form = perg.formularioid
    perg.formularioid = None
    perg.save()
    return render(request, 'formularios/mensagem.html',
                  {'tipo': 'success', 'm': 'A pergunta foi removida do formulário', 'form': form,
                   'link': 'consultar-formularios'})


def disponibilizar_formulario(request, id):
    form = Formulario.objects.get(pk=id)
    form.disponibilidade = 1
    form.save()
    return render(request, 'formularios/mensagem.html',
                  {'tipo': 'success', 'm': 'O formulário foi disponibilizado com sucesso', 'form': form,
                   'link': 'consultar-formularios'})


def criar_pergunta(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # if Sala.objects.filter(nome = request.POST.get('nome')).exists():
        #     return render(request,'formularios/mensagem.html',{'tipo':'error','m':'A sala com esse nome já existe','link':'consultar-salas'})
        # create a form instance and populate it with data from the request:
        form = CriarPerguntaForm(request.POST)
        # check whether it's valid:

        if form.is_valid:
            titulo_r = request.POST.get('titulo')
            tipo_pergunta_r = request.POST.get('tipo_pergunta')
            Tipo_Pergunta_r = TipoDePergunta.objects.get(pk=tipo_pergunta_r)
            pergunta = Pergunta(titulo=titulo_r, tipo_de_perguntaid=Tipo_Pergunta_r)
            pergunta.save()
            if Tipo_Pergunta_r.nome == 'Escolha múltipla' or Tipo_Pergunta_r.nome == 'Caixa de seleção':
                opcao1_r = request.POST.get('opcao1')
                Opcao1_r = Opcoes(texto=opcao1_r, perguntaid=pergunta)
                Opcao1_r.save()
                opcao2_r = request.POST.get('opcao2')
                Opcao2_r = Opcoes(texto=opcao2_r, perguntaid=pergunta)
                Opcao2_r.save()

            return render(
                request,
                'formularios/mensagem.html',
                {
                    'tipo': 'success',
                    'm': 'A pergunta foi criada com o sucesso',
                    'link': 'consultar-perguntas'
                }
            )



    # if a GET (or any other method) we'll create a blank form
    else:
        form = CriarPerguntaForm()

    return render(request, 'formularios/criar_pergunta.html', {'form': form})


def alterar_pergunta(request, id):
    try:
        pergunta_object = Pergunta.objects.get(id=id)
    except:
        return redirect('consultar-perguntas')
    pergunta_form = pergunta_object.formularioid
    if (Evento.objects.filter(formulariofeedbackid=pergunta_form) or Evento.objects.filter(
            formularioinscricaoid=pergunta_form)) and pergunta_form != None:
        return render(request, 'formularios/mensagem.html',
                      {'tipo': 'error', 'm': 'A pergunta já está associada a um recursos e não pode ser alterada.',
                       'link': 'consultar-perguntas'})

    if request.method == 'POST':
        # submited_data = request.POST.copy()
        # form = AlterarSalaForm(submited_data, request.FILES.copy(), instance=sala_object)

        pergunta = AlterarPerguntaForm(
            initial={'titulo': pergunta_object.titulo, 'tipo_evento': pergunta_object.tipo_de_perguntaid.pk})

        erros = []

        if pergunta.is_valid:

            titulo_r = request.POST.get('titulo')
            tipo_pergunta_r = request.POST.get('tipo_pergunta')
            Tipo_Pergunta_r = TipoDePergunta.objects.get(pk=tipo_pergunta_r)

            if Tipo_Pergunta_r.nome != 'Escolha múltipla' and Tipo_Pergunta_r.nome != 'Caixa de seleção':
                opcoes = Opcoes.objects.filter(perguntaid=id)
                for opcao in opcoes:
                    opcao.delete()

                pergunta_object.titulo = titulo_r
                pergunta_object.tipo_de_perguntaid = Tipo_Pergunta_r
                pergunta_object.save()

                return render(request, 'formularios/mensagem.html',
                              {'tipo': 'success', 'm': 'A pergunta foi alterada com sucesso.',
                               'link': 'consultar-perguntas'})
            else:
                opcao_r = request.POST.get('opcao')
                if opcao_r != '':
                    Opcao_r = Opcoes(texto=opcao_r, perguntaid=pergunta_object)
                    Opcao_r.save()

                pergunta_object.titulo = titulo_r
                pergunta_object.tipo_de_perguntaid = Tipo_Pergunta_r
                pergunta_object.save()

                return render(request, 'formularios/mensagem.html',
                              {'tipo': 'success', 'm': 'A pergunta foi alterada com sucesso.',
                               'link': 'consultar-perguntas'})

        else:
            msg = ""
            return render(
                request=request,
                template_name='formularios/alterar_pergunta.html',
                context={
                    'form': pergunta, 'msg': msg, 'erros': erros, 'id': id
                }
            )

    else:
        form = AlterarPerguntaForm(
            initial={'titulo': pergunta_object.titulo, 'tipo_pergunta': pergunta_object.tipo_de_perguntaid.pk})
        # form = AlterarSalaForm(initial={'capacidade':sala_object.capacidade,'nome':sala_object.nome})
        # perguntas = {}
        opcoes = []
        for opcao in Opcoes.objects.filter(perguntaid=id):
            # perguntas.update({pergunta.titulo : pergunta.tipo_de_perguntaid.nome})
            opcoes.append(opcao)
        return render(
            request,
            'formularios/alterar_pergunta.html',
            {'form': form, 'id': id, 'opcoes': opcoes}

        )


def remover_opcao(request, id):
    opcao = Opcoes.objects.get(pk=id)
    form = opcao.perguntaid
    opcao.delete()
    return render(request, 'formularios/mensagem.html',
                  {'tipo': 'success', 'm': 'A opcao foi removida da pergunta', 'form': form,
                   'link': 'consultar-perguntas'})
