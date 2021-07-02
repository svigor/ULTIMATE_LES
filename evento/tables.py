from datetime import date

import django_tables2 as tables
import django_filters.views
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from .models import Evento, Respostas
from .filters import eventofilter
from users.models import MyUser
from django.urls import reverse
from datetime import datetime


class consultarEvento(tables.Table):
    aprovado = tables.Column('Estado', attrs={"th": {"style": "padding-right:5em"}})
    nome = tables.Column('Nome')
    proponenteutilizadorid = tables.Column('Proponente')
    tipo_de_eventoid = tables.Column('Tipo')
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
        if int(value) % 60 != 0:
            return str(int(value / 60)) + 'h' + str(int(value % 60)) + 'm'
        elif int(value) < 60:
            return '00h' + value + 'm'
        else:
            return str(int(value / 60)) + 'h' + '00m'

    def render_hora_de_inicio(self, value):
        return str(value)

    def render_dia(self, value):
        return value.strftime("%d/%m/%y")

    def render_aprovado(self, value):
        if value == 0:
            return format_html(
                '<div><button class="button is-danger small"style="pointer-events:none;">Não Aprovado</button></div>')
        elif value == 1:
            return format_html(
                '<div><button class="button is-warning small" style="pointer-events:none;">Pendente</button></div>')

    def render_acoes(self, record):
        primeiro_botao = f"""
               <a href='{reverse('mudarevento', args={record.id})}'
                   data-tooltip="Visualizar">
                   <span class="icon">
                       <i class="mdi mdi-magnify mdi-24px"></i>
                   </span>
               </a>
               """
        return format_html(
            f"""<div class="columns is-gapless"><div class=column>{primeiro_botao}</div></div>""")


class meuseventos(tables.Table):
    id = tables.Column('id')
    aprovado = tables.Column('Estado')
    nome = tables.Column('Nome')
    proponenteutilizadorid = tables.Column('Proponente')
    tipo_de_eventoid = tables.Column('Tipo')
    campusid = tables.Column('Campus')
    dia = tables.Column('dia')
    capacidade = tables.Column('Capacidade')
    duracao = tables.Column('Duração')
    filterset_class = eventofilter
    acoes = tables.Column('Ações', empty_values=(), orderable=False, attrs={"th": {"width": "150"}})
    diaFinal = tables.Column('Dia Final')

    def before_render(self, request):
        self.columns.hide('id')

    class Meta:
        template_name = 'evento/bulma_table.html'
        fields = (
            "id", "nome", "tipo_de_eventoid", "aprovado", "dia", "duracao", "campusid", "proponenteutilizadorid",
            "capacidade", "diaFinal")

    def render_dia(self, value):
        tempo = str(value)
        data = tempo.split('-')
        result = data[2] + '-' + data[1] + '-' + data[0]
        return result

    def render_diaFinal(self, value):
        tempo = str(value)
        data = tempo.split('-')
        result = data[2] + '-' + data[1] + '-' + data[0]
        return result

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
        if value == 0:
            return format_html(
                '<div><button class="button is-danger small"style="pointer-events:none;">Não Aprovado</button></div>')
        elif value == 1:
            return format_html(
                '<div><button class="button is-warning small" style="pointer-events:none;">Pendente</button></div>')

    def render_acoes(self, record):
        # terceiro_butao = ""
        primeiro_botao = f"""
                <a href='{reverse('editar_evento', args={record.id})}'
                    data-tooltip="Editar">
                    <span class="icon">
                        <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                    </span>
                </a>
                """
        alertt = 'Tem a certeza que quer eleminar o recursos?'
        segundo_botao = f"""
                 <a onclick="alert.render('{alertt}','{reverse('apagar_evento', args=[record.id])}')"
                     data-tooltip="Apagar">
                     <span class="icon has-text-danger">
                         <i class="mdi mdi-trash-can mdi-24px"></i>
                     </span>
                 </a>
             """
        # ##if record.aprovado == 1:
        # ## terceiro_butao = f"""
        # ##    <a href='{reverse('associarsala', args={record.id})}'
        # ##     data-tooltip="Adicionar Logistica">
        # ##   <span class="icon">
        # ##     <i class="mdi mdi-clipboard-flow mdi-24px"></i>
        # ##</span>
        # ##</a>
        # ##"""
        # ##return format_html(
        # ##      f"""<div class="columns is-gapless"><div class=column>{primeiro_botao}</div><div class=column>{segundo_botao}</div><div class=column>{terceiro_butao}</div></div>""")
        # # else:

        return format_html(
            f"""<div class="columns is-gapless"><div class=column>{primeiro_botao}</div><div class=column>{segundo_botao}</div></div>""")
