from datetime import date

import django_tables2 as django_tables
from .models import Equipamento, Evento, Sala, Campus, Edificio, Servicos, Logistica
from django.utils.html import format_html
from django.urls import reverse


class consultarEvento(django_tables.Table):
    aprovado = django_tables.Column('Aprovado')
    proponenteutilizadorid = django_tables.Column('Nome do Proponente')
    tipo_de_eventoid = django_tables.Column('Tipo de Evento')
    campusid = django_tables.Column('Campus')
    duracao = django_tables.Column('Duração')
    hora_de_inicio = django_tables.Column('Hora de Inicio')

    def render_hora_de_inicio(self, value):
        return str(value)

    def render_aprovado(self, value):
        if value == '0':
            return 'Não Aprovado'
        elif value == '1':
            return 'Aprovado'

    class Meta:
        model = Evento
        template_name = 'evento/bulma_table_details.html'
        fields = (
            "id", "capacidade", "aprovado", "dia", "hora_de_inicio", "duracao", "campusid", "proponenteutilizadorid",
            "tipo_de_eventoid")


class SalaTable(django_tables.Table):
    # Os nomes que aparecem na tabela
    capacidade = django_tables.Column(empty_values=(), order_by='capacidade')
    nome = django_tables.Column('Sala')
    mobilidade_reduzida = django_tables.Column(
        'Apropriado para as pessoas com a mobilidade reduzida?')
    edificioid = django_tables.Column('Edifício')
    acoes = django_tables.Column('Ações', empty_values=(
    ), orderable=False, attrs={"th": {"width": "150"}})
    campus = django_tables.Column(
        'Campus', accessor='edificioid.campusid.nome')
    tipo_sala = django_tables.Column(
        'Tipo', accessor='tipo_salaid.nome'
    )

    class Meta:
        #template_name = 'evento/bulma_table_details'
        model = Sala
        sequence = ('campus', 'mobilidade_reduzida',
                    'edificioid', 'nome', 'tipo_sala','capacidade',  'acoes')

    def before_render(self, request):
        self.columns.hide('fotos')
        self.columns.hide('id')
        self.columns.hide('mobilidade_reduzida')
        self.columns.hide('tipo_salaid')

    def render_mobilidade_reduzida(self, value):
        if value == True:
            return "Sim"
        else:
            return "Não"

    

    def render_acoes(self, record):
        primeiro_botao = """<span class="icon"></span>"""
       
        primeiro_botao = ""
        if self.request.user.role.role == 'Administrador':
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
        if segundo_botao == "":
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




class ServicoTable(django_tables.Table):
    nome = django_tables.Column('Nome')
    preco_base = django_tables.Column('Preço em €')
    tipo_servicoid = django_tables.Column('Tipo', accessor='tipo_servicoid.nome')
    acoes = django_tables.Column('Ações', empty_values=(
    ), orderable=False, attrs={"th": {"width": "150"}})
    

    class Meta:
        model = Servicos
        sequence = ('tipo_servicoid', 'nome', 'preco_base', 'acoes','descricao')

    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('descricao')

    def render_acoes(self, record):
        primeiro_botao = """<span class="icon"></span>"""
        primeiro_botao = ""
        if self.request.user.role.role == 'Administrador':
            primeiro_botao = f"""
            <a href='{reverse('alterar-servico', args=[record.id])}'
                data-tooltip="Editar">
                <span class="icon">
                    <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                </span>
            </a>
            """
        
        segundo_botao = ""
        alerta = "Tem certeza que quer apagar a sala?"
        if segundo_botao == "":
            segundo_botao = f"""
                <a onclick="alert.render('{alerta}','{reverse('apagar-servico', args=[record.id])}')"
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



class EquipamentoTable(django_tables.Table):
    tipo_equipmaentoid = django_tables.Column('Tipo', accessor='tipo_equipamentoid.nome')
    nome = django_tables.Column('Nome')
    descricao = django_tables.Column('Descricao')
    acoes = django_tables.Column('Ações', empty_values=(
    ), orderable=False, attrs={"th": {"width": "150"}})
    

    class Meta:
        model = Equipamento
        sequence = ('nome', 'tipo_equipmaentoid', 'acoes')

    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('descricao')
        self.columns.hide('tipo_equipamentoid')
        

    def render_acoes(self, record):
        primeiro_botao = """<span class="icon"></span>"""
        primeiro_botao = ""
        if self.request.user.role.role == 'Administrador':
            primeiro_botao = f"""
            <a href='{reverse('alterar-equipamento', args=[record.id])}'
                data-tooltip="Editar">
                <span class="icon">
                    <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                </span>
            </a>
            """
        
        segundo_botao = ""
        alerta = "Tem certeza que quer apagar a sala?"
        if segundo_botao == "":
            segundo_botao = f"""
              <a onclick="alert.render('{alerta}','{reverse('apagar-equipamento', args=[record.id])}')"
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







class LogisticaTable(django_tables.Table):
    # Os nomes que aparecem na tabela
    eventoid = django_tables.Column(empty_values=(), order_by='eventoid', accessor='eventoid.id')
    valido = django_tables.Column('Estado')
    acoes = django_tables.Column('Ações', empty_values=(
    ), orderable=False, attrs={"th": {"width": "150"}})
   

    class Meta:
        #template_name = 'evento/bulma_table_details'
        model = Logistica
        sequence = ('eventoid','valido','acoes')

    def before_render(self, request):
        self.columns.hide('id')

    def render_valido(self, value):
        if value == 0:
            return format_html(
                '<div><button class="button is-danger small"style="pointer-events:none;">Não Aprovado</button></div>')
        elif value == 1:
            return format_html(
                '<div><button class="button is-success small" style="pointer-events:none;">Aprovado</button></div>')
    

    def render_acoes(self, record):
        primeiro_botao = """<span class="icon"></span>"""
       
        primeiro_botao = ""
        if self.request.user.role.role == 'Administrador':
            primeiro_botao = f"""
            <a href='{reverse('visualizar-logistica2', args=[record.eventoid.id])}'
                data-tooltip="Editar">
                <span class="icon">
                    <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                </span>
            </a>
            """
        
        segundo_botao = ""
        alerta = "Tem certeza que quer apagar a sala?"
        if segundo_botao == "":
            segundo_botao = f"""
                <a onclick="alert.render('{alerta}','{reverse('visualizar-logistica2', args=[record.id])}')"
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