from django.forms.forms import Form
from django.shortcuts import render, redirect
from django.urls.base import reverse
from .forms import InserirSalaForm, InscricaoForm, AlterarSalaForm, CriarFormularioForm, AlterarFormularioForm, CriarPerguntaForm, AlterarPerguntaForm
    
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.http import HttpResponseRedirect
from django.views.generic import(
    ListView,
    CreateView,
)
from .models import Evento, Opcoes, Sala, Edificio, Formulario, Pergunta, TipoDeEvento, TipoDeFormulario, TipoDePergunta
from utilizadores.models import Administrador
from utilizadores.views import user_check, mensagem
from evento.tables import PerguntaTable, SalaTable, FormularioTable
from evento.filters import SalasFilter, FormulariosFilter
from django.contrib.auth import *
from django.contrib import messages
# Create your views here.


def home(request):
    return render(request, 'evento/inicio.html')

class consultar_salas(SingleTableMixin, FilterView):
    ''' Consultar todos os utilizadores com as funcionalidades dos filtros '''
    table_class = SalaTable
    template_name = 'evento/consultar_salas.html'
    filterset_class = SalasFilter
    table_pagination = {
        'per_page': 10
    }

    def dispatch(self, request, *args, **kwargs):
        user_check_var = user_check(
            request=request, user_profile=[Administrador])
        if not user_check_var.get('exists'):
            return user_check_var.get('render')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SingleTableMixin, self).get_context_data(**kwargs)
        table = self.get_table(**self.get_table_kwargs())
        table.request = self.request
        table.fixed = True
        context[self.get_context_table_name(table)] = table
        return context


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

def InscricaoView(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InscricaoForm(request.POST, request.FILES)
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
            return HttpResponseRedirect('http://127.0.0.1:8000/sala/new/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = InserirSalaForm()

    return render(request, 'evento/criar_sala.html', {'form': form})

def apagar_sala(request, id):
    if request.user.is_authenticated:
        user = get_user(request)
        if user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        else:
            return render(request,'evento/mensagem.html',{'tipo':'error','m':'Não é permetido','link':'home'})
    Sala.objects.get(id=id).fotos.delete(save=True)
    Sala.objects.filter(id=id).delete()

    return render(request,'evento/mensagem.html',{'tipo':'success','m':'A sala foi apagada com o sucesso','link':'consultar-salas'})

def alterar_sala(request,id):
    if request.user.is_authenticated:
        user = get_user(request)
        if user.groups.filter(name="Administrador").exists():
            u = "Administrador"
        else:
            return render(request,'evento/mensagem.html',{'tipo':'error','m':'Não é permetido','link':'home'})

    
    if request.method == 'POST':
        sala_object = Sala.objects.get(id=id)
        # submited_data = request.POST.copy()
        # form = AlterarSalaForm(submited_data, request.FILES.copy(), instance=sala_object)
        form = AlterarSalaForm(request.POST, request.FILES, instance=sala_object,initial={'campus':sala_object.edificioid.campusid.pk})
        

        nome = request.POST.get('nome')
        erros = []

        
        if Sala.objects.exclude(nome = sala_object.nome).filter(nome = request.POST.get('nome')).exists():
            msg = "A sala com esse nome já existe"
            return render(request,'evento/alterarsala.html',{'msg':msg,'id':id,'form':form})

    
        if form.is_valid() and len(erros)==0:
            mobilidade_reduzida_r = 0
            if request.POST.get('mobilidade_reduzida') == 'on':
                mobilidade_reduzida_r = 1
            
            
            if(sala_object.fotos):
                Sala.objects.get(id=id).fotos.delete(save=True)
            
            Sala1 = sala_object
            Sala1.capacidade = request.POST.get('capacidade')
            if not request.FILES.get('fotos') is not False:
                Sala1.fotos = request.FILES.get('fotos')
            if request.FILES.get('fotos') is None:
                Sala.objects.get(id=id).fotos.delete(save=True)
           
            Sala1.nome = request.POST.get('nome')
            Sala1.mobilidade_reduzida = mobilidade_reduzida_r
            Edificio1 = Edificio.objects.get(pk=request.POST.get('edificioid'))
            Sala1.edificioid = Edificio1
            Sala1.save()
            return render(request,'evento/mensagem.html',{'tipo':'success','m':'A sala foi alterada com o sucesso','link':'consultar-salas'})


        else:
            
            return render(
                request= request,
                template_name='evento/alterarsala.html',
                context={
                    'form':form, 'msg':msg, 'erros':erros, 'id':id
                }
            )
    else:
        sala_object = Sala.objects.get(id=id)
        form = AlterarSalaForm(instance=sala_object,initial={'campus':sala_object.edificioid.campusid.pk})
        #form = AlterarSalaForm(initial={'capacidade':sala_object.capacidade,'nome':sala_object.nome})
        return render(
                request,
                'evento/alterarsala.html',
                {'form': form, 'id':id}
                
            )

        
class consultar_formularios(SingleTableMixin, ListView):
    model = Formulario
    table_class = FormularioTable
    template_name = 'evento/consultar_formularios.html'
    filterset_class = FormulariosFilter
    table_pagination = {'per_page':10}
    

def show_perguntas(request, id):
    print(id)
    if not Formulario.objects.filter(id=id):
        redirect('consultar-formularios')
    perguntas = {}
    for pergunta in Pergunta.objects.all().filter(formularioid=id) :
        perguntas.update({pergunta.tipo_de_perguntaid.nome : pergunta.titulo})
    tipo = Formulario.objects.get(pk=id)
    return render(request, 'evento/visualizar_formulario.html', {'perguntas':perguntas, 'tipo' : tipo})

def apagar_form(request, id):
    
    if not Evento.objects.filter(formularioinscricaoid=Formulario.objects.get(id=id)) and not Evento.objects.filter(formulariofeedbackid=Formulario.objects.get(id=id)) :
        Pergunta.objects.filter(formularioid=id).update(formularioid=None)
        Formulario.objects.filter(id=id).delete()
        return render(request,'evento/mensagem.html',{'tipo':'success','m':'O formulário foi apagado com sucesso','link':'consultar-formularios'})
    else :
        return render(request,'evento/mensagem.html',{'tipo':'error','m':'O formulário não pôde ser apagado','link':'consultar-formularios'})

class consultar_perguntas(SingleTableMixin, ListView):
    model = Pergunta
    table_class = PerguntaTable
    template_name = 'evento/consultar_perguntas.html'
    table_pagination = {'per_page':10}

def show_opcoes(request, id):
    if not Pergunta.objects.filter(id=id):
        return redirect('consultar-perguntas')
    tipo_pergunta = Pergunta.objects.get(id=id).tipo_de_perguntaid.nome
    # print(tipo_pergunta)
    if tipo_pergunta != "Caixa de seleção" and tipo_pergunta != "Escolha múltipla" :
        return redirect('consultar-perguntas')
    opcoes = {}
    i = 0
    for opcao in Opcoes.objects.all().filter(perguntaid=id) :
        opcoes.update({ i : opcao.texto })
        i += 1
    tipo = Pergunta.objects.get(pk=id)
    return render(request, 'evento/visualizar_pergunta.html', {'opcoes':opcoes, 'tipo' : tipo})

def apagar_pergunta(request, id):
    if not Pergunta.objects.filter(id=id) :
        return redirect('consultar-perguntas')
    
    p = Pergunta.objects.get(id=id)
    if not p.formularioid == None:
        formulario = p.formularioid
        if not Evento.objects.filter(formularioinscricaoid=formulario) and not Evento.objects.filter(formulariofeedbackid=formulario) :
            Opcoes.objects.filter(perguntaid=id).delete()
            Pergunta.objects.filter(id=id).delete()
            # Pergunta.objects.filter(formularioid=id).update(formularioid=None)
            # Formulario.objects.filter(id=id).delete()
            return render(request,'evento/mensagem.html',{'tipo':'success','m':'A pergunta foi apagada com sucesso','link':'consultar-perguntas'})
        else :
            return render(request,'evento/mensagem.html',{'tipo':'error','m':'A pergunta não pôde ser apagada','link':'consultar-perguntas'})
    else :
        Opcoes.objects.filter(perguntaid=id).delete()
        Pergunta.objects.filter(id=id).delete()
        return render(request,'evento/mensagem.html',{'tipo':'success','m':'A pergunta foi apagada com sucesso','link':'consultar-perguntas'})

def criar_formulario(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # if Sala.objects.filter(nome = request.POST.get('nome')).exists():
        #     return render(request,'evento/mensagem.html',{'tipo':'error','m':'A sala com esse nome já existe','link':'consultar-salas'})
        # create a form instance and populate it with data from the request:
        form = CriarFormularioForm(request.POST)
        # check whether it's valid:
      
       
        if form.is_valid:
            tipo_form_r = request.POST.get('tipo_form')
            Tipo_Form_r = TipoDeFormulario.objects.get(pk=tipo_form_r)
            pergunta_r = request.POST.get('pergunta')
            Pergunta_r = Pergunta.objects.get(pk=pergunta_r)
            if Pergunta_r.formularioid != None :
                return render(
                        request,
                        'evento/mensagem.html',
                        {
                            'tipo':'error',
                            'm':'A pergunta já está associada a um formulário!',
                            'link':'consultar-formularios'
                        })

            if Tipo_Form_r.nome == 'Evento' :
                tipo_evento_r = request.POST.get('tipo_evento')
                Tipo_Evento_r = TipoDeEvento.objects.get(pk=tipo_evento_r)
                if Formulario.objects.filter(tipo_de_formularioid=Tipo_Form_r).filter(tipo_de_eventoid=Tipo_Evento_r) :
                    return render(
                        request,
                        'evento/mensagem.html',
                        {
                            'tipo':'error',
                            'm':'O formulário não pôde ser criado',
                            'link':'consultar-formularios'
                        })
                else :
                    Form_r = Formulario(tipo_de_formularioid=Tipo_Form_r, tipo_de_eventoid=Tipo_Evento_r, disponibilidade=0)
            else :
                Form_r = Formulario(tipo_de_formularioid=Tipo_Form_r, tipo_de_eventoid=None, disponibilidade=0)
            
            Form_r.save()
            Pergunta_r.formularioid = Form_r
            Pergunta_r.save()

            return render(
                request,
                'evento/mensagem.html',
                {
                    'tipo':'success',
                    'm':'O formulário foi criado com o sucesso',
                    'link':'consultar-formularios'
                }
            )

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CriarFormularioForm()

    return render(request, 'evento/criar_formulario.html', {'form': form})

def alterar_formulario(request, id):
    try : 
        form_object = Formulario.objects.get(id=id)
    except :
        return redirect('consultar-formulario')
    if Evento.objects.filter(formulariofeedbackid=form_object) or Evento.objects.filter(formularioinscricaoid=form_object) :
        return render(request,'evento/mensagem.html',{'tipo':'error','m':'O formulario já está associado a um evento e não pode ser alterado.','link':'consultar-formularios'})

    if request.method == 'POST':
        form_object = Formulario.objects.get(id=id)
        # submited_data = request.POST.copy()
        # form = AlterarSalaForm(submited_data, request.FILES.copy(), instance=sala_object)
        if form_object.tipo_de_eventoid != None :
            form = AlterarFormularioForm(initial={'tipo_form':form_object.tipo_de_formularioid.pk, 'tipo_evento':form_object.tipo_de_eventoid.pk})
        else :
            form = AlterarFormularioForm(initial={'tipo_form':form_object.tipo_de_formularioid.pk})
        
        
        erros = []
    
        if form.is_valid:
            
            tipo_form_r = request.POST.get('tipo_form')
            Tipo_Form_r = TipoDeFormulario.objects.get(pk=tipo_form_r)
            pergunta_r = request.POST.get('pergunta')
            
            if Tipo_Form_r.nome == 'Evento' :
                tipo_evento_r = request.POST.get('tipo_evento')
                Tipo_Evento_r = TipoDeEvento.objects.get(pk=tipo_evento_r)
                form_object.tipo_de_eventoid = Tipo_Evento_r
                if Formulario.objects.filter(tipo_de_formularioid=Tipo_Form_r).filter(tipo_de_eventoid=Tipo_Evento_r).exclude(id=id):
                    msg = "Já existe um formulário de eventos para esse tipo de evento."
                    return render(request,'evento/alterar_formulario.html',{'msg':msg,'id':id,'form':form})
            else :
                form_object.tipo_de_eventoid = None

            if pergunta_r != '' :
                Pergunta_r = Pergunta.objects.get(pk=pergunta_r)
                if Pergunta_r.formularioid == None :
                    Pergunta_r.formularioid = form_object
                    Pergunta_r.save()
                else :
                    msg = "A pergunta já está associada a um formulário!"
                    return render(request,'evento/alterar_formulario.html',{'msg':msg,'id':id,'form':form})
           
            form_object.tipo_de_formularioid = Tipo_Form_r
            form_object.save()
            return render(request,'evento/mensagem.html',{'tipo':'success','m':'O formulário foi alterado com sucesso','link':'consultar-formularios'})


        else:
            
            return render(
                request= request,
                template_name='evento/alterar_formulario.html',
                context={
                    'form':form, 'msg':msg, 'erros':erros, 'id':id
                }
            )
    else:
        form_object = Formulario.objects.get(id=id)
        if form_object.tipo_de_eventoid != None :
            form = AlterarFormularioForm(initial={'tipo_form':form_object.tipo_de_formularioid.pk, 'tipo_evento':form_object.tipo_de_eventoid.pk})
        else :
            form = AlterarFormularioForm(initial={'tipo_form':form_object.tipo_de_formularioid.pk})
        #form = AlterarSalaForm(initial={'capacidade':sala_object.capacidade,'nome':sala_object.nome})
        # perguntas = {}
        perguntas = []
        for pergunta in Pergunta.objects.filter(formularioid=id) :
            # perguntas.update({pergunta.titulo : pergunta.tipo_de_perguntaid.nome})
            perguntas.append(pergunta)
        return render(
                request,
                'evento/alterar_formulario.html',
                {'form': form, 'id':id, 'perguntas':perguntas}
                
            )

def remover_pergunta(request, id):
    perg = Pergunta.objects.get(pk=id)
    form = perg.formularioid
    perg.formularioid = None
    perg.save()
    return render(request,'evento/mensagem.html',{'tipo':'success','m':'A pergunta foi removida do formulário', 'form':form, 'link':'consultar-formularios'})

def disponibilizar_formulario(request, id):
    form = Formulario.objects.get(pk=id)
    form.disponibilidade = 1
    form.save()
    return render(request,'evento/mensagem.html',{'tipo':'success','m':'O formulário foi disponibilizado com sucesso', 'form':form, 'link':'consultar-formularios'})

def criar_pergunta(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # if Sala.objects.filter(nome = request.POST.get('nome')).exists():
        #     return render(request,'evento/mensagem.html',{'tipo':'error','m':'A sala com esse nome já existe','link':'consultar-salas'})
        # create a form instance and populate it with data from the request:
        form = CriarPerguntaForm(request.POST)
        # check whether it's valid:
      
       
        if form.is_valid:
            titulo_r = request.POST.get('titulo')
            tipo_pergunta_r = request.POST.get('tipo_pergunta')
            Tipo_Pergunta_r = TipoDePergunta.objects.get(pk=tipo_pergunta_r)
            pergunta = Pergunta(titulo=titulo_r, tipo_de_perguntaid=Tipo_Pergunta_r)
            pergunta.save()
            if Tipo_Pergunta_r.nome == 'Escolha múltipla' or Tipo_Pergunta_r.nome == 'Caixa de seleção' :
                opcao1_r = request.POST.get('opcao1')
                Opcao1_r = Opcoes(texto=opcao1_r, perguntaid=pergunta)
                Opcao1_r.save()
                opcao2_r = request.POST.get('opcao2')
                Opcao2_r = Opcoes(texto=opcao2_r, perguntaid=pergunta)
                Opcao2_r.save()

            return render(
                request,
                'evento/mensagem.html',
                {
                    'tipo':'success',
                    'm':'A pergunta foi criada com o sucesso',
                    'link':'consultar-perguntas'
                }
            )

        

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CriarPerguntaForm()

    return render(request, 'evento/criar_pergunta.html', {'form': form})

def alterar_pergunta(request, id):
    try : 
        pergunta_object = Pergunta.objects.get(id=id)
    except :
        return redirect('consultar-perguntas')
    pergunta_form = pergunta_object.formularioid
    if (Evento.objects.filter(formulariofeedbackid=pergunta_form) or Evento.objects.filter(formularioinscricaoid=pergunta_form)) and pergunta_form != None :
        return render(request,'evento/mensagem.html',{'tipo':'error','m':'A pergunta já está associada a um evento e não pode ser alterada.','link':'consultar-perguntas'})


    if request.method == 'POST':
        # submited_data = request.POST.copy()
        # form = AlterarSalaForm(submited_data, request.FILES.copy(), instance=sala_object)
        
        pergunta = AlterarPerguntaForm(initial={'titulo':pergunta_object.titulo, 'tipo_evento':pergunta_object.tipo_de_perguntaid.pk})
        
        erros = []
    
        if pergunta.is_valid:
            
            titulo_r = request.POST.get('titulo')
            tipo_pergunta_r = request.POST.get('tipo_pergunta')
            Tipo_Pergunta_r = TipoDePergunta.objects.get(pk=tipo_pergunta_r)
            
            if Tipo_Pergunta_r.nome != 'Escolha múltipla' and Tipo_Pergunta_r.nome != 'Caixa de seleção' :
                opcoes = Opcoes.objects.filter(perguntaid=id)
                for opcao in opcoes :
                    opcao.delete()
                
                pergunta_object.titulo = titulo_r
                pergunta_object.tipo_de_perguntaid = Tipo_Pergunta_r
                pergunta_object.save()

                return render(request,'evento/mensagem.html',{'tipo':'success','m':'A pergunta foi alterada com sucesso.','link':'consultar-perguntas'})
            else :
                opcao_r = request.POST.get('opcao')
                if opcao_r != '' :
                    Opcao_r = Opcoes(texto=opcao_r, perguntaid=pergunta_object)
                    Opcao_r.save()
                
                pergunta_object.titulo = titulo_r
                pergunta_object.tipo_de_perguntaid = Tipo_Pergunta_r
                pergunta_object.save()

                return render(request,'evento/mensagem.html',{'tipo':'success','m':'A pergunta foi alterada com sucesso.','link':'consultar-perguntas'})
        
        else:
            
            return render(
                request= request,
                template_name='evento/alterar_pergunta.html',
                context={
                    'form':pergunta, 'msg':msg, 'erros':erros, 'id':id
                }
            )

    else:
        form = AlterarPerguntaForm(initial={'titulo':pergunta_object.titulo, 'tipo_pergunta':pergunta_object.tipo_de_perguntaid.pk})
        #form = AlterarSalaForm(initial={'capacidade':sala_object.capacidade,'nome':sala_object.nome})
        # perguntas = {}
        opcoes = []
        for opcao in Opcoes.objects.filter(perguntaid=id) :
            # perguntas.update({pergunta.titulo : pergunta.tipo_de_perguntaid.nome})
            opcoes.append(opcao)
        return render(
                request,
                'evento/alterar_pergunta.html',
                {'form': form, 'id':id, 'opcoes':opcoes}
                
            )

def remover_opcao(request, id):
    opcao = Opcoes.objects.get(pk=id)
    form = opcao.perguntaid
    opcao.delete()
    return render(request,'evento/mensagem.html',{'tipo':'success','m':'A opcao foi removida da pergunta', 'form':form, 'link':'consultar-perguntas'})