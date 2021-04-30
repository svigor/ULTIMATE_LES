from django.shortcuts import render, redirect
from .forms import InserirSalaForm, InscricaoForm, AlterarSalaForm
    
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.http import HttpResponseRedirect
from django.views.generic import(
    ListView,
    CreateView,
)
from .models import Sala, Edificio
from utilizadores.models import Administrador
from utilizadores.views import user_check, mensagem
from evento.tables import SalaTable
from evento.filters import SalasFilter
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
    
        form = AlterarSalaForm(request.POST, request.FILES, instance=sala_object)
        

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
                Sala.objects.filter(id=id).delete()
            
            Sala1 = sala_object
            Sala1.capacidade = request.POST.get('capacidade')
            if not request.FILES.get('fotos') is not False:
                Sala1.fotos = request.FILES.get('fotos')
            if request.FILES.get('fotos') is None:
                Sala.objects.get(id=id).fotos.delete(save=True)
                Sala.objects.filter(id=id).delete()
           
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
        form = AlterarSalaForm(instance=sala_object)
        #form = AlterarSalaForm(initial={'capacidade':sala_object.capacidade,'nome':sala_object.nome})
        return render(
                request,
                'evento/alterarsala.html',
                {'form': form, 'id':id}
                
            )

        

