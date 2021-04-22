from django.shortcuts import render
from .forms import InserirSalaForm, InscricaoForm
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.http import HttpResponseRedirect
from django.views.generic import(
    ListView,
    CreateView,
)
from .models import Sala, Edificio
from utilizadores.models import Administrador
from utilizadores.views import user_check
from evento.tables import SalaTable
from evento.filters import SalasFilter
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
            print(request.POST.get('mobilidade_reduzida'))
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
            print(request.POST.get('mobilidade_reduzida'))
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
