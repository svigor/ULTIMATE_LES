from datetime import date

import django_tables2 as tables
from .models import Evento


class consultarEvento(tables.Table):
    aprovado = tables.Column('Aprovado')
    proponenteutilizadorid = tables.Column('Nome do Proponente')
    tipo_de_eventoid = tables.Column('Tipo de Evento')
    campusid = tables.Column('Campus')
    duracao = tables.Column('Duração')
    hora_de_inicio = tables.Column('Hora de Inicio')

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
