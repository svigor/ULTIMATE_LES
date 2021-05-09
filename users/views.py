from django.shortcuts import render, redirect
from django.contrib.auth import login as l, authenticate, logout
from .models import MyUser
from evento.views import homepage
from .forms import registerForm, loginForm
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
                request.session['nome_completo'] = user.NomeProprio
                request.session['n_telefone'] = user.n_telefone
                return redirect(homepage)
    else:
        form = loginForm()
        context['form'] = form
    return render(request, 'users/login.html', {'form': form})

def logout1(request):
    logout(request)
    return redirect(homepage)

def consultar_utilizadors(request):
    return render(request, 'users/consultar_utilizadores_tabela.html')
