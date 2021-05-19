import django_tables2 as django_tables
from utilizadores.models import Administrador, Utilizador
from evento.models import Evento, Pergunta, Sala, Formulario
from django.utils.html import format_html
from django.urls import reverse

class SalaTable(django_tables.Table):
    #Os nomes que aparecem na tabela
    capacidade = django_tables.Column(empty_values=(), order_by='capacidade')
    nome = django_tables.Column('Sala')
    mobilidade_reduzida = django_tables.Column('Apropriado para as pessoas com a mobilidade reduzida?')
    edificioid = django_tables.Column('Edifício')
    acoes = django_tables.Column('Ações', empty_values=(), orderable=False, attrs={"th": {"width": "150"}})
    campus = django_tables.Column('Campus', accessor='edificioid.campusid.nome')

    class Meta:
        model = Sala
        sequence = ('campus','mobilidade_reduzida','edificioid', 'nome','capacidade',  'acoes')

    def before_render(self,request):
        self.columns.hide('fotos')
        self.columns.hide('id')
        self.columns.hide('mobilidade_reduzida')
    

    def render_mobilidade_reduzida(self,value):
        if value == True:
            return "Sim"
        else:
            return "Não"

    def render_acoes(self, record):
        primeiro_botao = """<span class="icon"></span>"""
       
        primeiro_botao = ""
        if self.request.user.groups.filter(name='Administrador').exists():
            primeiro_botao = f"""
            <a href='{reverse('alterar-sala', args=[record.id])}'
                data-tooltip="Editar">
                <span class="icon">
                    <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                </span>
            </a>
            """
        
        segundo_botao = ""
        alerta = "Tem certeza que quer apagar a sala?"
        if self.request.user != record.id and segundo_botao == "":
            segundo_botao = f"""
                <a onclick="alert.render('{alerta}','{reverse('apagar-sala', args=[record.id])}')"
                    data-tooltip="Apagar">
                    <span class="icon has-text-danger">
                        <i class="mdi mdi-trash-can mdi-24px"></i>
                    </span>
                </a>
            """
        return format_html(f"""
        <div>
            {primeiro_botao}
            {segundo_botao}
        </div>
        """)

class FormularioTable(django_tables.Table):
    tipo_de_formularioid = django_tables.Column('Tipo de Formulário')
    tipo_de_eventoid = django_tables.Column('Tipo de Evento')
    acoes = django_tables.Column('Ações', empty_values=(), orderable=False, attrs={"th": {"width": "150"}})
    
    def render_tipo_de_formularioid(self, value):
        return value.nome
    
    def render_tipo_de_eventoid(self, value):
        return value.nome

    def before_render(self,request):
        self.columns.hide('id')

    def render_acoes(self, record):
        primeiro_botao = f"""
            <a href='{reverse('consultar-perguntas-formulario', args={record.id})}'
                data-tooltip="Visualizar">
                <span class="icon">
                    <i class="mdi mdi-magnify mdi-24px"></i>
                </span>
            </a>
            """
        
        if not Evento.objects.filter(formularioinscricaoid=Formulario.objects.get(id=record.id)) and not Evento.objects.filter(formulariofeedbackid=Formulario.objects.get(id=record.id)) :
            alerta = "Tem certeza que quer apagar a sala?"
            segundo_botao = f"""
                <a onclick="alert.render('{alerta}','{reverse('apagar-form', args=[record.id])}')"
                    data-tooltip="Apagar">
                    <span class="icon has-text-danger">
                        <i class="mdi mdi-trash-can mdi-24px"></i>
                    </span>
                </a>
            """
        else :
            segundo_botao = f"""
                    <span class="icon">
                        <i class="mdi mdi-trash-can mdi-24px" style="color: gray"></i>
                    </span>
            """
        return format_html(f"""
        <div>
            {primeiro_botao}
            {segundo_botao}
        </div>
        """)
    
    

    class Meta:
        model = Formulario
        template_name = 'evento/bulma_table.html'
        fields = ('id', 'tipo_de_formularioid', 'tipo_de_eventoid')
    

class PerguntaTable(django_tables.Table):
    titulo = django_tables.Column('Título')
    tipo_de_perguntaid = django_tables.Column('Tipo de Pergunta')
    formularioid = django_tables.Column('Formulário')
    acoes = django_tables.Column('Ações', empty_values=(), orderable=False, attrs={"th": {"width": "150"}})
    
    # def render_titulo(self, value):
    #     return value.titulo
    
    def render_tipo_de_perguntaid(self, value):
        return value.nome

    def render_formularioid(self, value):
        if not value.tipo_de_formularioid.nome == "Evento" :
            return "(%d) " % value.id + "%s" % value.tipo_de_formularioid.nome
        else :
            return "(%d) " % value.id + "%s " % value.tipo_de_formularioid.nome + "%s " % value.tipo_de_eventoid.nome

    def before_render(self,request):
        self.columns.hide('id')

    def render_acoes(self, record):
        primeiro_botao = f"""
            <a href='#'
                data-tooltip="Editar">
                <span class="icon">
                    <i class="mdi mdi-pencil mdi-24px"></i>
                </span>
            </a>
            """
        
        # if not Evento.objects.filter(formularioinscricaoid=Formulario.objects.get(id=record.id)) and not Evento.objects.filter(formulariofeedbackid=Formulario.objects.get(id=record.id)) :
        #     alerta = "Tem certeza que quer apagar a sala?"
        #     segundo_botao = f"""
        #         <a onclick="alert.render('{alerta}','{reverse('apagar-form', args=[record.id])}')"
        #             data-tooltip="Apagar">
        #             <span class="icon has-text-danger">
        #                 <i class="mdi mdi-trash-can mdi-24px"></i>
        #             </span>
        #         </a>
        #     """
        # else :
        #     segundo_botao = f"""
        #             <span class="icon">
        #                 <i class="mdi mdi-trash-can mdi-24px" style="color: gray"></i>
        #             </span>
        #     """
        return format_html(f"""
        <div>
            {primeiro_botao}
            
        </div>
        """)
    

    class Meta:
        model = Pergunta
        template_name = 'evento/bulma_table.html'
        fields = ('id', 'titulo', 'tipo_de_perguntaid', 'formularioid')
    

