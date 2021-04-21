from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Utilizador, Participante, Proponente
from django.shortcuts import redirect
from .forms import *
from .tables import UtilizadoresTable
from .filters import UtilizadoresFilter
from django.contrib import messages
from django.contrib.auth import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group

from django.core.paginator import Paginator
#from notificacoes import views
#from inscricoes.models import Inscricao
from django.db import transaction
#from atividades.models import Sessao
#from notificacoes.models import *
#from coordenadores.models import Tarefa
from django.db.models import F
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView



def user_check(request, user_profile = None):
    ''' 
    Verifica se o utilizador que esta logado pertence a pelo menos um dos perfis mencionados 
    e.g. user_profile = {Administrador,Coordenador,ProfessorUniversitario}
    Isto faz com que o user que esta logado possa ser qualquer um dos 3 perfis. 
    '''
    if not request.user.is_authenticated:
        return {'exists': False, 'render': redirect('utilizadores:login')}
    elif user_profile is not None:
        matches_profile = False
        for profile in user_profile:
            if profile.objects.filter(utilizador_ptr_id = request.user.id).exists():
                return {'exists': True, 'firstProfile': profile.objects.filter(utilizador_ptr_id = request.user.id).first()}
        return {'exists': False, 
                'render': render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'error',
                                'm':'Não tem permissões para aceder a esta página!'
                            })
                }
    raise Exception('Unknown Error!')







class consultar_utilizadores(SingleTableMixin, FilterView):
    ''' Consultar todos os utilizadores com as funcionalidades dos filtros '''
    table_class = UtilizadoresTable
    template_name = 'utilizadores/consultar_utilizadores.html'
    filterset_class = UtilizadoresFilter
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




def escolher_perfil(request):
    ''' Escolher tipo de perfil para criar um utilizador '''
    if request.user.is_authenticated:    
        user = get_user(request)
    
        if user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "Proponente").exists():
            u = "Proponente"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""     
    else:
        u=""
    utilizadores = ["Participante",
                    "Proponente","Administrador"]
    return render(request=request, template_name='utilizadores/escolher_perfil.html', context={"utilizadores": utilizadores,'u': u})






def criar_utilizador(request, id):
    ''' Criar um novo utilizador que poderá ter de ser validado dependendo do seu tipo '''
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "Proponente").exists():
            u = "Proponente"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""     
    else:
        u=""
    msg=False
    if request.method == "POST":
        tipo = id
        if tipo == 1:
            form = ParticipanteRegisterForm(request.POST)
            perfil = "Participante"
            my_group = Group.objects.get(name='Participante') 
        elif tipo == 2:
            form = ProponenteRegisterForm(request.POST)
            perfil = "Proponente"
            my_group = Group.objects.get(name='Proponente')
        elif tipo == 3:
            form = AdministradorRegisterForm(request.POST)
            perfil = "Administrador"
            my_group = Group.objects.get(name='Administrador')    
        else:
            return redirect("utilizadores:escolher-perfil")

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            my_group.user_set.add(user)

            if tipo == 1:
                user.valido = 'True'
                user.save()
                p=1
            else:
                user.valido = 'False'
                user.save()
                p=1
                #user.valido = 'False'
                #recipient_id = user.id #Enviar Notificacao Automatica !!!!!!!!!
                #user.save()
                #p=0
                #views.enviar_notificacao_automatica(request,"validarRegistosPendentes",recipient_id) #Enviar Notificacao Automatica !!!!!!!!!
            
            if request.user.is_authenticated:    
                user = get_user(request)
                if user.groups.filter(name = "Proponente").exists():
                    return redirect("utilizadores:concluir-registo",2)
                elif user.groups.filter(name = "Administrador").exists():
                    return redirect("utilizadores:concluir-registo",2)  
            else:   
                return redirect("utilizadores:concluir-registo",p)

        else:
            msg=True
            tipo = id
            return render(request=request,
                          template_name="utilizadores/criar_utilizador.html",
                          context={"form": form, 'perfil': perfil, 'u': u,'registo' : tipo,'msg': msg})
    else:
        tipo = id
        if tipo == 1:
            form = ParticipanteRegisterForm()
            perfil = "Participante"
        elif tipo == 2:
            form = ProponenteRegisterForm()
            perfil = "Proponente"
        elif tipo == 3:
            form = AdministradorRegisterForm()
            perfil = "Administrador" 
        else:
            return redirect("utilizadores:escolher-perfil")
    return render(request=request,
                  template_name="utilizadores/criar_utilizador.html",
                  context={"form": form, 'perfil': perfil,'u': u,'registo' : tipo,'msg': msg})




def login_action(request):
    ''' Fazer login na plataforma do dia aberto e gestão de acessos à plataforma '''
    if request.user.is_authenticated: 
        return redirect("utilizadores:logout")   
    else:
        u=""
    msg=False
    error=""
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username=="" or password=="":
                msg=True
                error="Todos os campos são obrigatórios!"
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                utilizador = Utilizador.objects.get(id=user.id)
                if utilizador.valido=="False": 
                    msg=True
                    error="O seu registo ainda não foi validado"
                elif utilizador.valido=="Rejeitado":
                    msg=True
                    error="O seu registo não é válido"
                else:
                    login(request, user)
                    return redirect('utilizadores:mensagem',1)
            else:
                msg=True
                error="O nome de utilizador ou a palavra-passe inválidos!"
    form = LoginForm()
    return render(request=request,
                  template_name="utilizadores/login.html",
                  context={"form": form,"msg": msg, "error": error, 'u': u})






def logout_action(request):
    ''' Fazer logout na plataforma '''
    logout(request)
    return redirect('utilizadores:mensagem',2)





def alterar_password(request):
    ''' Alterar a password do utilizador '''
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""     
    else:
        return redirect('utilizadores:mensagem',5)
    msg=False
    error="" 
    if request.method == 'POST':
        form = AlterarPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('utilizadores:mensagem',6)
        else:
            msg=True
            error="Passwords Incorretas!"
    form = AlterarPasswordForm(user=request.user)
    return render(request=request,
                  template_name="utilizadores/alterar_password.html",
                  context={"form": form,"msg": msg, "error": error, 'u': u})    






def rejeitar_utilizador(request, id): 
    ''' Funcionalidade de rejeitar um utilizador na pagina de consultar utilizadores '''
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Administrador").exists():
            u = "Administrador"   
        elif user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"       
        else:
            return redirect('utilizadores:mensagem',5) 
    else:
        return redirect('utilizadores:mensagem',5) 
        
    try:
        u = Utilizador.objects.get(id = id)
        u.valido = 'Rejeitado'           
        u.save()   
        subject = 'Validação do registo do na plataforma do dia aberto'
        message = 'Caro(a) '+u.first_name+",\n\n"
        message+='O seu registo na plataforma do dia aberto foi rejeitado!'+"\n\n"
        message+='Equipa do dia aberto da Ualg'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [u.email,]
        send_mail( subject, message, email_from, recipient_list )
    except:
        pass
    if 'consultar_utilizadores' not in request.session:
        return redirect('utilizadores:consultar-utilizadores')
    else:    
        return HttpResponseRedirect(request.session['consultar_utilizadores'])





def alterar_idioma(request):  
    ''' Alterar o idioma da plataforma ''' 
    return redirect('utilizadores:mensagem',5)  




def validar_utilizador(request, id): 
    ''' Validar um utilizador na pagina consultar utilizadores '''
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Administrador").exists():
            u = "Administrador"   
        elif user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"       
        else:
            return redirect('utilizadores:mensagem',5) 
    else:
        return redirect('utilizadores:mensagem',5) 
        
    try:
        u = Utilizador.objects.get(id = id)
        u.valido = 'True'           
        u.save()   
        subject = 'Validação do registo do na plataforma do dia aberto'
        message = 'Caro(a) '+u.first_name+"\n\n"
        message+='O seu registo na plataforma do dia aberto foi bem sucedido!'+",\n\n"
        message+='Equipa do dia aberto da Ualg'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [u.email,]
        send_mail( subject, message, email_from, recipient_list )
    except:
        pass

    if 'consultar_utilizadores' not in request.session:
        return redirect('utilizadores:consultar-utilizadores')
    else:    
        return HttpResponseRedirect(request.session['consultar_utilizadores'])



def home(request):
    ''' Pagina principal da plataforma '''
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""     
    else:
        u=""
    
    return render(request, "inicio.html",context={ 'u': u})



def concluir_registo(request,id):
    ''' Página que é mostrada ao utilizador quando faz um registo na plataforma '''
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""   
    else:
        u=""
    if id == 1:
        participante="True"
    elif id == 0:
        participante="False"
    elif id == 2:
        participante="Admin"   
    return render(request=request,
                  template_name="utilizadores/concluir_registo.html",
                  context={'participante': participante, 'u': u})

