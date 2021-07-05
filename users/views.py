import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import login as l, authenticate, logout
from django_filters.views import FilterView
from .filters import usersfilter
from django_tables2 import SingleTableMixin
from .tables import Myuserstable, pedidos

from .models import MyUser, pedidomudar
from evento.views import homepage
from .forms import registerForm, loginForm, alterarperfil
from .models import Role


def register(request):
    context = {}
    if request.method == 'POST':
        form = registerForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            var.role = Role.objects.get(pk=1)
            var.save()
            user = authenticate(email=email, password=password)
            return redirect(concluir_registo)
        else:
            context['form'] = form
    else:
        form = registerForm()
        context['form'] = form
    return render(request, 'users/criar_utilizador.html', context)


def concluir_registo(request):
    return render(request, 'users/concluir_registo.html')


def login(request):
    context = {}
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            if user:
                l(request, user)
                request.session['role'] = user.role.role
                request.session['nome_completo'] = user.NomeProprio + " " + user.SecondName
                request.session['n_telefone'] = user.n_telefone
                request.session['id'] = user.id
                return redirect(homepage)
    else:
        form = loginForm()
        context['form'] = form
    return render(request, 'users/login.html', {'form': form})


def logout1(request):
    request.session.clear()
    logout(request)
    return redirect(homepage)


class consultar_utilizadors(SingleTableMixin, FilterView):
    model = MyUser
    table_class = Myuserstable
    template_name = 'users/consultar_utilizadores_tabela.html'
    filterset_class = usersfilter
    table_pagination = {'per_page': 10}


def pedidodeperfil(request):
    if request.method == 'POST':
        user = MyUser.objects.get(id=request.user.id)
        user.email = request.POST.get('Email:')
        user.NomeProprio = request.POST.get('Nome Próprio:')
        user.SecondName = request.POST.get('Apelido:')
        user.date_of_birth = datetime.datetime.strptime(request.POST.get('Data de Nascimento:'), "%Y-%m-%d")
        user.n_telefone = request.POST.get('Numero de telefone:')
        user.username = request.POST.get('Nome do Usuário:')
        if user.role.role != request.POST.get('role'):
            pd = pedidomudar(asked_role=request.POST.get('role'), usuario=user)
            pd.save()
            user.save()
            return render(request, 'evento/mensagem.html',
                          {'tipo': 'success',
                           'm': 'Alteração de Dados feito com sucesso. O seu pedido de perfil será revisto pelo administrador.',
                           'link': 'evento-home'})
        else:
            user.save()
            return render(request, 'evento/mensagem.html',
                          {'tipo': 'success',
                           'm': 'Alteração de Dados feito com sucesso.',
                           'link': 'evento-home'})
    else:
        dict = {}
        dict.update({'Email:': request.user.email})
        dict.update({'Nome Próprio:': request.user.NomeProprio})
        dict.update({'Apelido:': request.user.SecondName})
        dict.update({'Data de Nascimento:': request.user.date_of_birth.strftime("%Y-%m-%d")})
        dict.update({'Numero de telefone:': request.user.n_telefone})
        dict.update({'Nome do Usuário:': request.user.username})
        dict.update({'Atual Perfil de Utilizador': 0})
        forms = alterarperfil(initial={'role': request.user.role.role})
        return render(request, 'users/mudar_perfil.html', {'dados': dict, 'form': forms})


class consultarpedidos(SingleTableMixin, FilterView):
    model = pedidomudar
    table_class = pedidos
    template_name = 'users/consultarpedidos.html'
    filterset_class = usersfilter
    table_pagination = {'per_page': 10}


def aceitarpedido(request, id):
    p1 = pedidomudar.objects.get(id=id)
    user = MyUser.objects.get(id=p1.usuario.id)
    role = Role.objects.get(role=p1.asked_role)
    user.role = role
    user.save()
    p1.delete()
    return redirect('consultarutilizadores')


def recusarpedido(request, id):
    p1 = pedidomudar.objects.get(id=id)
    p1.delete()
    return redirect('consultarutilizadores')
