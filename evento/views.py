from django.shortcuts import render
from .forms import InserirSalaForm
from django.http import HttpResponseRedirect
from django.views.generic import(
    ListView,
    CreateView,
)
from .models import Sala, Edificio
# Create your views here.


def home(request):
    return render(request, 'evento/inicio.html')


def SalaCreateView(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InserirSalaForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            edificio_id_r = request.POST.get('edificioid')
            Edificio_r = Edificio.objects.get(pk=edificio_id_r)
            capacidade_r = request.POST.get('capacidade')
            fotos_r = request.POST.get('fotos')
            nome_r = request.POST.get('nome')
            mobilidade_reduzida_r = ('mobilidade_reduzida')
            if mobilidade_reduzida_r == 'mobilidade_reduzida':
                mobilidade_reduzida_r = 1
            Sala_r = Sala(capacidade=capacidade_r, fotos=fotos_r, nome=nome_r,
                          mobilidade_reduzida=mobilidade_reduzida_r, edificioid=Edificio_r)
            Sala_r.save()
            # return HttpResponseRedirect('')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = InserirSalaForm()

    return render(request, 'evento/criar_sala.html', {'form': form})
