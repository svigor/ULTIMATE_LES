import django_tables2 as django_tables
from users.models import MyUser
from evento.models import Inscricao
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth import *

class InscricaoTable(django_tables.Table):
    #Os nomes que aparecem na tabela
    eventoid = django_tables.Column('Evento')
    requer_certificado = django_tables.Column('Pretende Receber um Certificado?')
    presenca = django_tables.Column('Esteve Presente no Evento?')
    datainscricao = django_tables.Column('Realizou a inscrição no dia:')
    acoes = django_tables.Column('Ações', empty_values=(),
                                orderable=False, attrs={"th": {"width": "150"}})

    class Meta:
        model = Inscricao
        template_name = 'evento/bulma_table.html'
        sequence = ('eventoid', 'requer_certificado', 'presenca', 'datainscricao')

    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('participanteutilizadorid')
       
    def render_requer_certificado(self,value):
        if value == True:
            return "Sim"
        else:
            return "Não"

    def render_presenca(self,value):
        if value == True:
            return "Sim"
        else:
            return "Não"
    

    def render_acoes(self, record):
        segundo_botao = ""
        alerta = "Tem certeza que quer apagar a sala?"
        if self.request.user != record.id and segundo_botao == "":
            segundo_botao = f"""
                <a onclick="alert.render('{alerta}','{reverse('apagarinscricao', args=[record.id])}')"
                    data-tooltip="Apagar">
                    <span class="icon has-text-danger">
                        <i class="mdi mdi-trash-can mdi-24px"></i>
                    </span>
                </a>
            """
        return format_html(f"""
        <div>
            {segundo_botao}
        </div>
        """)

class InscricaoTableProponente(django_tables.Table):
    #Os nomes que aparecem na tabela
    eventoid = django_tables.Column('Evento')
    requer_certificado = django_tables.Column('Pretende Receber um Certificado?')
    presenca = django_tables.Column('Esteve Presente no Evento?')
    datainscricao = django_tables.Column('Realizou a inscrição no dia')
    participanteutilizadorid = django_tables.Column('Participante')
    acoes = django_tables.Column('Ações', empty_values=(),
                                orderable=False, attrs={"th": {"width": "150"}})

    class Meta:
        model = Inscricao
        sequence = ('eventoid', 'requer_certificado', 'presenca', 'datainscricao')

    def before_render(self, request):
        self.columns.hide('id')
       
    def render_requer_certificado(self,value):
        if value == True:
            return "Sim"
        else:
            return "Não"

    def render_presenca(self,value):
        if value == True:
            return "Sim"
        else:
            return "Não"
    

    def render_acoes(self, record):
        primeiro_botao = """<span class="icon"></span>"""
       
        primeiro_botao = ""
        if self.request.user.role.role == 'Proponente':
            primeiro_botao = f"""
            <a href='{reverse('alterarinscricao', args=[record.id])}'
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
                <a onclick="alert.render('{alerta}','{reverse('apagarinscricao', args=[record.id])}')"
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