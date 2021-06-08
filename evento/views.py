from django.shortcuts import render, redirect
from django.views.generic import ListView
from django_tables2 import SingleTableView
from .tables import consultarEvento
from django.template.defaultfilters import register
from django.contrib.sessions.backends.base import SessionBase
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from .tables import SalaTable, ServicoTable, EquipamentoTable

from .forms import opcaoevento, r_a_form, r_c_form, n_tel, c_s_form, r_c_form_dis, InserirSalaForm, AlterarSalaForm, CriarServicoForm, AlterarServicoForm, CriarEquipamentoForm, AlterarEquipamentoForm
from .models import TipoDeEvento, Formulario, Pergunta, TipoDePergunta, Campus, Evento, TipoDeFormulario, Edificio, Sala, TipoServico, Servicos, Equipamento, TipoEquipamento, TipoSala
from .filters import SalasFilter, ServicosFilter, EquipamentosFilter


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
    if not request.user.is_authenticated or not request.user.role.role == 'Administrador':
        return render(request,'evento/mensagem.html',{'tipo':'error','m':'Não é permetido','link':'evento-home'})
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
            capacidade_r = request.POST.get('capacidade')
            fotosw = request.FILES.get('fotos')
            nome_r = request.POST.get('nome')
            mobilidade_reduzida_r = request.POST.get('mobilidade_reduzida')
            mobilidade_reduzida_r = 0
            
            if request.POST.get('mobilidade_reduzida') == 'on':
                mobilidade_reduzida_r = 1

            tipo_salaid = request.POST.get('tipo_salaid')
            TipoSala1 = TipoSala.objects.get(pk = tipo_salaid)
            Sala_r = Sala(capacidade=capacidade_r, fotos=fotosw, nome=nome_r,
                          mobilidade_reduzida=mobilidade_reduzida_r,tipo_salaid=TipoSala1,edificioid=Edificio_r)
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
    return render(request, 'evento/edificios_dropdown_list.html', {'edificios': edificios})



class consultar_salas(SingleTableMixin, FilterView):
    
    table_class = SalaTable
    template_name = 'evento/consultar_salas.html'
    filterset_class = SalasFilter
    table_pagination = {
        'per_page': 10
    }

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.role.role == 'Administrador':
            return render(request,'evento/mensagem.html',{'tipo':'error','m':'Não é permetido','link':'evento-home'})
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SingleTableMixin, self).get_context_data(**kwargs)
        table = self.get_table(**self.get_table_kwargs())
        table.request = self.request
        table.fixed = True
        context[self.get_context_table_name(table)] = table
        return context


def alterar_sala(request,id):
    if not request.user.is_authenticated or not request.user.role.role == 'Administrador':
        return render(request,'evento/mensagem.html',{'tipo':'error','m':'Não é permetido','link':'evento-home'})
    
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
            
            
    
            
            Sala1 = sala_object
            Sala1.capacidade = request.POST.get('capacidade')
            
            
            if request.FILES.get('fotos'):
                Sala1.fotos = request.FILES.get('fotos')

            tipo_salaid = request.POST.get('tipo_salaid')
            TipoSala1 = TipoSala.objects.get(pk = tipo_salaid)
            Sala1.tipo_salaid = TipoSala1
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


def apagar_sala(request, id):
    if not request.user.is_authenticated or not request.user.role.role == 'Administrador':
        return render(request,'evento/mensagem.html',{'tipo':'error','m':'Não é permetido','link':'evento-home'})
    Sala.objects.get(id=id).fotos.delete(save=True)
    Sala.objects.filter(id=id).delete()

    return render(request,'evento/mensagem.html',{'tipo':'success','m':'A sala foi apagada com o sucesso','link':'consultar-salas'})



def criar_servico(request):
    if not request.user.is_authenticated or not request.user.role.role == 'Administrador':
        return render(request,'evento/mensagem.html',{'tipo':'error','m':'Não é permetido','link':'evento-home'})

    if request.method == 'POST':
        form = CriarServicoForm(request.POST)

        if Servicos.objects.filter(nome = request.POST.get('nome')).exists():
            return render(request,'evento/mensagem.html',{'tipo':'error','m':'A serviço com esse nome já existe','link':'consultar-servicos'})

        if form.is_valid():
            nome = request.POST.get('nome')
            preco_base = request.POST.get('preco_base')
            tipo_de_servico = request.POST.get('tipo_de_servico')
            descricao = request.POST.get('descricao')

            servico = TipoServico.objects.get(pk=tipo_de_servico)
            new_Servico = Servicos(nome=nome,descricao=descricao, preco_base=preco_base, tipo_servicoid=servico)
            new_Servico.save()

            return render(
                request,
                'evento/mensagem.html',
                {
                    'tipo':'success',
                    'm':'O servico foi criado com o sucesso',
                    'link':'consultar-servicos'
                }
            )
    else:
        form = CriarServicoForm()
    return render(request, 'evento/criar_servico.html', {'form':form})



class consultar_servicos(SingleTableMixin, FilterView):
    table_class = ServicoTable
    template_name = 'evento/consultar_servicos.html'
    filterset_class = ServicosFilter
    table_pagination = {
        'per_page': 10
    }

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.role.role == 'Administrador':
            return render(request,'evento/mensagem.html',{'tipo':'error','m':'Não é permetido','link':'evento-home'})
        return super().dispatch(request, *args, **kwargs)

    
    def get_context_data(self, **kwargs):
        context = super(SingleTableMixin, self).get_context_data(**kwargs)
        table = self.get_table(**self.get_table_kwargs())
        table.request = self.request
        table.fixed = True
        context[self.get_context_table_name(table)] = table
        return context


def apagar_sevico(request, id):
    if not request.user.is_authenticated or not request.user.role.role == 'Administrador':
        return render(request,'evento/mensagem.html',{'tipo':'error','m':'Não é permetido','link':'evento-home'})
    Servicos.objects.get(id=id).delete()
    return render(request, 'evento/mensagem.html', {'tipo':'success', 'm':'O serviço foi apagado com o sucesso','link':'consultar-servicos'})




def alterar_servico(request,id):
    if not request.user.is_authenticated or not request.user.role.role == 'Administrador':
        return render(request,'evento/mensagem.html',{'tipo':'error','m':'Não é permetido','link':'evento-home'})
    
    if request.method == 'POST':
        servico_object = Servicos.objects.get(id=id)
        form = AlterarServicoForm(request.POST, instance=servico_object, initial={'tipo_se_Servico':servico_object.tipo_servicoid.pk})
        nome = request.POST.get('nome')
        if Servicos.objects.exclude(nome = servico_object.nome).filter(nome = request.POST.get('nome')).exists():
            msg = "A serviço com esse nome já existe"
            return render(request,'evento/alteraservico.html',{'msg':msg,'id':id,'form':form})

        

       

    
        if form.is_valid():
            Servico1 = servico_object
            
            Servico1.nome = request.POST.get('nome')
            Servico1.preco_base = request.POST.get('preco_base')
            TipoServico1 = TipoServico.objects.get(pk=request.POST.get('tipo_de_servico'))

            Servico1.tipo_servicoid = TipoServico1
            Servico1.save()

            return render(request,'evento/mensagem.html',{'tipo':'success','m':'O servico foi alterado com o sucesso','link':'consultar-servicos'})

        else:
            
            return render(
                request= request,
                template_name='evento/alterarservico.html',
                context={
                    'form':form, 'm':msg, 'id':id
                }
            )
    else:
        servico_object = Servicos.objects.get(id=id)
        form = AlterarServicoForm(instance=servico_object,initial={'tipo_de_servico':servico_object.tipo_servicoid.pk})
        return render(
                request,
                'evento/alterarservico.html',
                {'form': form, 'id':id}            
            )

def criar_equipamento(request):
    if not request.user.is_authenticated or not request.user.role.role == 'Administrador':
        return render(request,'evento/mensagem.html',{'tipo':'error','m':'Não é permetido','link':'evento-home'})
    
    if request.method == 'POST':
        form = CriarEquipamentoForm(request.POST)

        if Equipamento.objects.filter(nome = request.POST.get('nome')).exists():
            return render(request,'evento/mensagem.html',{'tipo':'error','m':'O equipamento com esse nome já existe','link':'consultar-equipamentos'})

        if form.is_valid():
            tipo_equipamentoid = request.POST.get('tipo_equipamentoid')
            nome = request.POST.get('nome')
            descricao = request.POST.get('descricao')

            equipamento = TipoEquipamento.objects.get(pk=tipo_equipamentoid)
            new_equpamento = Equipamento(nome=nome, descricao=descricao,tipo_equipamentoid=equipamento)

            new_equpamento.save()

            return render(
                request,
                'evento/mensagem.html',
                {
                    'tipo':'success',
                    'm':'O equipamento foi criado com o sucesso',
                    'link':'consultar-equipamentos'
                }
            )
    else:
        form = CriarEquipamentoForm()
    return render(request, 'evento/criar_equipamento.html',{'form':form})




def alterar_equipamento(request,id):
    if not request.user.is_authenticated or not request.user.role.role == 'Administrador':
        return render(request,'evento/mensagem.html',{'tipo':'error','m':'Não é permetido','link':'evento-home'})
    
    if request.method == 'POST':
        equipamento_object = Equipamento.objects.get(id=id)
        form = AlterarEquipamentoForm(request.POST, instance=equipamento_object, initial={'tipo_equipamentoid':equipamento_object.tipo_equipamentoid.pk})
                        
        nome = request.POST.get('nome')

        if Equipamento.objects.exclude(nome = equipamento_object.nome).filter(nome = request.POST.get('nome')).exists():
            msg = "O equipamento com esse nome já existe"
            return render(request,'evento/alterasequipamento.html',{'msg':msg,'id':id,'form':form})
    
        if form.is_valid():
            Equipamento1 = equipamento_object
            
            Equipamento1.nome = request.POST.get('nome')
            Equipamento1.preco_base = request.POST.get('descricao')
            TipoEquipamento1 = TipoEquipamento.objects.get(pk=request.POST.get('tipo_equipamentoid'))

            Equipamento1.tipo_equipamentoid = TipoEquipamento1
            Equipamento1.save()

            return render(request,'evento/mensagem.html',{'tipo':'success','m':'O equipamento foi alterado com o sucesso','link':'consultar-equipamentos'})

        else:
            
            return render(
                request= request,
                template_name='evento/alterarequipamento.html',
                context={
                    'form':form, 'm':msg, 'id':id
                }
            )
    else:
        equipamento_object = Equipamento.objects.get(id=id)
        form = AlterarEquipamentoForm(instance=equipamento_object,initial={'tipo_equipamentoid':equipamento_object.tipo_equipamentoid.pk})
        return render(
                request,
                'evento/alterar_equipamento.html',
                {'form': form, 'id':id}            
            )



class consultar_equipamentos(SingleTableMixin, FilterView):
    table_class = EquipamentoTable
    template_name = 'evento/consultar_equipamentos.html'
    filterset_class = EquipamentosFilter
    table_pagination = {
        'per_page': 10
    }

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.role.role == 'Administrador':
            return render(request,'evento/mensagem.html',{'tipo':'error','m':'Não é permetido','link':'evento-home'})
        return super().dispatch(request, *args, **kwargs)

    
    def get_context_data(self, **kwargs):
        context = super(SingleTableMixin, self).get_context_data(**kwargs)
        table = self.get_table(**self.get_table_kwargs())
        table.request = self.request
        table.fixed = True
        context[self.get_context_table_name(table)] = table
        return context



def apagar_equipamento(request, id):
    if not request.user.is_authenticated or not request.user.role.role == 'Administrador':
        return render(request,'evento/mensagem.html',{'tipo':'error','m':'Não é permetido','link':'evento-home'})
    Equipamento.objects.filter(id=id).delete()
    return render(request,'evento/mensagem.html',{'tipo':'success','m':'A equipamento foi apagado com o sucesso','link':'consultar-equipamentos'})


        


