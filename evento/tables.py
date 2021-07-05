from datetime import date

import django_tables2 as tables
import django_filters.views
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from .models import Evento, Respostas, Logistica, Inscricao
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
        elif value == 2:
            return format_html(
                '<div><button class="button is-success small" style="pointer-events:none;">Aprovado</button></div>')

    def render_acoes(self, record):
        segundo_botao = ''
        primeiro_botao = f"""
               <a href='{reverse('mudarevento', args={record.id})}'
                   data-tooltip="Visualizar">
                   <span class="icon">
                       <i class="mdi mdi-magnify mdi-24px"></i>
                   </span>
               </a>
               """
        try:
            Logistica.objects.get(eventoid=record.id)
            segundo_botao = f"""
               <a href='{reverse('validar_logistica', args={record.id})}'
                   data-tooltip="Aprovar Logistica">
                   <span class="icon">
                       <i class="mdi mdi-check mdi-24px"></i>
                   </span>
               </a>
               """
            return format_html(
                f"""<div class="columns is-gapless"><div class=column>{primeiro_botao}</div><div class=column>{segundo_botao}</div></div>""")
        except Logistica.DoesNotExist:
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
        elif value == 2:
            return format_html(
                '<div><button class="button is-success small" style="pointer-events:none;">Aprovado</button></div>')

    def render_acoes(self, record):
        # terceiro_butao = ""
        primeiro_botao = f"""
                <a href='{reverse('editar_evento', args={record.id})}'
                    data-tooltip="Editar">
                    <span class="icon">
                        <i class="mdi mdi-pencil mdi-24px"></i>
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
        if record.aprovado == 1:
            terceiro_butao = f"""
                <a href='{reverse('criar-logistica1', args={record.id})}'
                 data-tooltip="Adicionar Logistica">
                    <span class="icon">
                        <i class="mdi mdi-clipboard-flow mdi-24px"></i>
                    </span>
                </a>
            """
            return format_html(
                f"""<div class="columns is-gapless"><div class=column>{primeiro_botao}</div><div class=column>{segundo_botao}</div><div class=column>{terceiro_butao}</div></div>""")
        elif record.aprovado == 2:
            quarto_butao = f"""
                            <a href='{reverse('viewinscricaomeuevento', args={record.id})}'
                             data-tooltip="Validar Inscrições">
                                <span class="icon">
                                    <i class="mdi mdi-account-arrow-right mdi-24px"></i>
                                </span>
                            </a>
                        """
            quinto_butao = f"""
                            <a href='{reverse('inscricaovalidadas', args={record.id})}'
                            data-tooltip="Realizar check In/Out">
                               <span class="icon">
                                    <i class="mdi mdi-account-check mdi-24px"></i>
                               </span>
                            </a>
                        """
            return format_html(
                f"""<div class="columns is-gapless"><div class=column>{primeiro_botao}</div><div class=column>{segundo_botao}</div></div><div class="columns is-gapless"><div class=column>{quarto_butao}</div><div class=column>{quinto_butao}</div></div>""")
        else:

            return format_html(
                f"""<div class="columns is-gapless"><div class=column>{primeiro_botao}</div><div class=column>{segundo_botao}</div></div>""")


class LogisticaTable(tables.Table):
    # Os nomes que aparecem na tabela
    eventoid = tables.Column('Evento', order_by='eventoid', accessor='eventoid.id')
    valido = tables.Column('Estado')
    acoes = tables.Column('Ações', empty_values=(
    ), orderable=False, attrs={"th": {"width": "150"}})

    class Meta:
        template_name = 'evento/bulma_tables.html'
        model = Logistica
        sequence = ('eventoid', 'valido', 'acoes')

    def before_render(self, request):
        self.columns.hide('id')

    def render_eventoid(self, value):
        evento_object = Evento.objects.get(id=value)
        return '(' + str(value) + ')' + ' ' + str(evento_object.tipo_de_eventoid.nome)

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
        alerta = "Tem a certeza que quer apagar a logistica?"
        if segundo_botao == "":
            segundo_botao = f"""
                <a onclick="alert.render('{alerta}','{reverse('apagar-logistica', args=[record.id])}')"
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


class consultarEventosaprovados(tables.Table):
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
        self.columns.hide('aprovado')

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

    def render_acoes(self, record):
        if record.proponenteutilizadorid.id != self.request.user.id:
            primeiro_botao = ""
            try:
                Inscricao.objects.get(eventoid=record.id, participanteutilizadorid=self.request.user)
                primeiro_botao = f"""<a style="cursor:not-allowed; color:grey;" href=''
                                            data-tooltip="Já se Inscreveu neste Evento">
                                               <span class="icon">
                                                    <i class="mdi mdi-account-check mdi-24px"></i>
                                               </span>
                                            </a>
                                        """
            except Inscricao.DoesNotExist:
                primeiro_botao = f"""<a href='{reverse('criarinscricao', args={record.id})}'
                            data-tooltip="Inscrever no Evento">
                               <span class="icon">
                                    <i class="mdi mdi-account-check mdi-24px"></i>
                               </span>
                            </a>
                        """
            return format_html(
                f"""<div class="columns is-gapless"><div class=column>{primeiro_botao}</div></div>""")
        else:
            primeiro_botao = f"""<a style="cursor:not-allowed; color:grey;" href=''
                                        data-tooltip="E o proponente deste Evento">
                                           <span class="icon">
                                                <i class="mdi mdi-account-check mdi-24px"></i>
                                           </span>
                                        </a>
                                    """
            return format_html(
                f"""<div class="columns is-gapless"><div class=column>{primeiro_botao}</div></div>""")
