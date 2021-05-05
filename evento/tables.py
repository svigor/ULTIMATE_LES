from datetime import date

import django_tables2 as django_tables
from .models import Evento, Sala, Campus, Edificio


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
    #Os nomes que aparecem na tabela
    capacidade = django_tables.Column(empty_values=(), order_by='capacidade')
    nome = django_tables.Column('Sala')
    mobilidade_reduzida = django_tables.Column('Apropriado para as pessoas com a mobilidade reduzida?')
    edificioid = django_tables.Column('Edifício')
    acoes = django_tables.Column('Ações', empty_values=(), orderable=False, attrs={"th": {"width": "150"}})
    campus = django_tables.Column('Campus', accessor='edificioid.campusid.nome')

    class Meta:
        #template_name = 'evento/bulma_table_details'
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
        if self.request.user.role.role == 'Administrador':
            primeiro_botao = f"""
           
            """
        
        segundo_botao = ""
        alerta = "Tem certeza que quer apagar a sala?"
        if self.request.user != record.id and segundo_botao == "":
            segundo_botao = f"""
               
            """
  