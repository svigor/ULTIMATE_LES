from datetime import date

import django_tables2 as tables
import django_filters.views
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from .models import Evento, Respostas
from .filters import eventofilter
from users.models import MyUser
from django.urls import reverse


class consultarEvento(tables.Table):
    aprovado = tables.Column('Estado')
    nome = tables.Column('Nome')
    proponenteutilizadorid = tables.Column('Nome do Proponente')
    tipo_de_eventoid = tables.Column('Tipo de Evento')
    campusid = tables.Column('Campus')
    dia = tables.Column('dia')
    capacidade = tables.Column('Capacidade')
    duracao = tables.Column('Duração')
    filterset_class = eventofilter
    acoes = tables.Column('Ações', empty_values=(), orderable=False, attrs={"th": {"width": "150"}})

    class Meta:
        template_name = 'evento/bulma_table.html'
        fields = (
            "nome", "tipo_de_eventoid", "aprovado", "dia", "duracao", "campusid", "proponenteutilizadorid",
            "capacidade")

    def render_duracao(self, value):
        if value % 60 != 0:
            return str(int(value / 60)) + 'h' + str(int(value % 60)) + 'm'
        elif int(value) < 60:
            return '00h' + value + 'm'
        else:
            return str(int(value / 60)) + 'h' + '00m'

    def render_hora_de_inicio(self, value):
        return str(value)

    def render_aprovado(self, value):
        if value == '0':
            return format_html(
                '<div><button class="button is-danger small"style="pointer-events:none;">Não Aprovado</button></div>')
        elif value == '1':
            return format_html(
                '<div><button class="button is-success small" style="pointer-events:none;">Aprovado</button></div>')

    def render_acoes(self, record):
        primeiro_botao = f"""
               <a href='#'
                   data-tooltip="Visualizar">
                   <span class="icon">
                       <i class="mdi mdi-magnify mdi-24px"></i>
                   </span>
               </a>
               """
        alertt = 'Tem a certeza que quer eleminar o evento?'
        segundo_botao = f"""
                <a onclick=""
                    data-tooltip="Apagar">
                    <span class="icon has-text-danger">
                        <i class="mdi mdi-trash-can mdi-24px"></i>
                    </span>
                </a>
            """
        return format_html(
            f"""<div class="columns is-gapless"><div class=column>{primeiro_botao}</div><div class=column>{segundo_botao}</div></div>""")


class meuseventos(tables.Table):
    id = tables.Column('id')
    aprovado = tables.Column('Estado')
    nome = tables.Column('Nome')
    proponenteutilizadorid = tables.Column('Nome do Proponente')
    tipo_de_eventoid = tables.Column('Tipo de Evento')
    campusid = tables.Column('Campus')
    dia = tables.Column('dia')
    capacidade = tables.Column('Capacidade')
    duracao = tables.Column('Duração')
    filterset_class = eventofilter
    acoes = tables.Column('Ações', empty_values=(), orderable=False, attrs={"th": {"width": "150"}})

    def before_render(self, request):
        self.columns.hide('id')

    class Meta:
        template_name = 'evento/bulma_table.html'
        fields = (
            "id", "nome", "tipo_de_eventoid", "aprovado", "dia", "duracao", "campusid", "proponenteutilizadorid",
            "capacidade")

    def render_duracao(self, value):
        if value % 60 != 0:
            return str(int(value / 60)) + 'h' + str(int(value % 60)) + 'm'
        elif int(value) < 60:
            return '00h' + value + 'm'
        else:
            return str(int(value / 60)) + 'h' + '00m'

    def render_hora_de_inicio(self, value):
        return str(value)

    def render_aprovado(self, value):
        if value == '0':
            return format_html(
                '<div><button class="button is-danger small"style="pointer-events:none;">Não Aprovado</button></div>')
        elif value == '1':
            return format_html(
                '<div><button class="button is-success small" style="pointer-events:none;">Aprovado</button></div>')

    def render_acoes(self, record):
        primeiro_botao = f"""
               <a href='{reverse('editar_evento', args={record.id})}'
                   data-tooltip="Editar">
                   <span class="icon">
                       <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                   </span>
               </a>
               """
        alertt = 'Tem a certeza que quer eleminar o evento?'
        segundo_botao =  f"""
                <a onclick="alert.render('{alertt}','{reverse('apagar_evento', args=[record.id])}')"
                    data-tooltip="Apagar">
                    <span class="icon has-text-danger">
                        <i class="mdi mdi-trash-can mdi-24px"></i>
                    </span>
                </a>
            """
        return format_html(
            f"""<div class="columns is-gapless"><div class=column>{primeiro_botao}</div><div class=column>{segundo_botao}</div></div>""")
