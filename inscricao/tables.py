import django_tables2 as django_tables
from evento.models import Inscricao, Evento
from django.utils.html import format_html
from django.urls import reverse
from .filters import InscricaoFilter
from users.models import MyUser


class InscricaoTable(django_tables.Table):
    # Os nomes que aparecem na tabela
    eventoid = django_tables.Column('Evento')
    requer_certificado = django_tables.Column('Pretende Receber um Certificado?')
    presenca = django_tables.Column('Esteve Presente no Evento?')
    datainscricao = django_tables.Column('Realizou a inscrição no dia:')
    estado = django_tables.Column('Estado')
    acoes = django_tables.Column('Ações', empty_values=(),
                                 orderable=False, attrs={"th": {"width": "150"}})

    class Meta:
        model = Inscricao
        template_name = 'inscricao/bulma_table.html'
        sequence = ('eventoid', 'requer_certificado', 'presenca', 'datainscricao')

    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('participanteutilizadorid')

    def render_requer_certificado(self, value):
        if value == True:
            return "Sim"
        else:
            return "Não"

    def render_presenca(self, value):
        if value == True:
            return format_html(
                '<div><button class="button is-success small"style="pointer-events:none;">Presente</button></div>')
        else:
            return format_html(
                '<div><button class="button is-danger small"style="pointer-events:none;">Ausente</button></div>')

    def render_estado(self, value):
        if value == 1:
            return format_html(
                '<div><button class="button is-warning small"style="pointer-events:none;">Pendente</button></div>')
        elif value == 2:
            return format_html(
                '<div><button class="button is-success small"style="pointer-events:none;">Aprovado</button></div>')
        elif value == 3:
            return format_html(
                '<div><button class="button is-danger small"style="pointer-events:none;">Não Aprovado</button></div>')

    def render_acoes(self, record):
        primeiro_botao = """<span class="icon"></span>"""

        primeiro_botao = ""
        try:
            evento1 = Inscricao.objects.get(id=record.id).eventoid
            Inscricao.objects.get(eventoid=evento1, participanteutilizadorid=self.request.user.id)
            primeiro_botao = f"""
            <a href='{reverse('alterarinscricao', args={record.id})}'
                data-tooltip="Editar">
                <span class="icon">
                    <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                </span>
            </a>
            """
        except Inscricao.DoesNotExist:
            return 0

        segundo_botao = ""
        alerta = "Tem certeza que quer apagar a sua inscrição?"
        if segundo_botao == "":
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


class InscricaoTableProponente(django_tables.Table):
    # Os nomes que aparecem na tabela
    id = django_tables.Column(visible=False)
    presenca = django_tables.Column(visible=False)
    eventoid = django_tables.Column('Evento')
    requer_certificado = django_tables.Column('Pretende Receber um Certificado?')
    datainscricao = django_tables.Column('Realizou a inscrição no dia')
    participanteutilizadorid = django_tables.Column('Participante')
    estado = django_tables.Column('Estado')
    acoes = django_tables.Column('Ações', empty_values=(),
                                 orderable=False, attrs={"th": {"width": "150"}})

    class Meta:
        template_name = 'inscricao/bulma_table.html'
        sequence = ('eventoid', 'requer_certificado', 'presenca', 'datainscricao')

    def render_requer_certificado(self, value):
        if value == True:
            return "Sim"
        else:
            return "Não"

    def render_estado(self, value):
        if value == 1:
            return format_html(
                '<div><button class="button is-warning small"style="pointer-events:none;">Pendente</button></div>')
        elif value == 2:
            return format_html(
                '<div><button class="button is-success small"style="pointer-events:none;">Aprovado</button></div>')
        elif value == 3:
            return format_html(
                '<div><button class="button is-danger small"style="pointer-events:none;">Não Aprovado</button></div>')

    def render_acoes(self, record):
        primeiro_botao = """<span class="icon"></span>"""

        primeiro_botao = ""
        if self.request.user.id == Evento.objects.get(id=record.id).proponenteutilizadorid.id:
            primeiro_botao = f"""
            <a href='{reverse('validarInscricao', args={record.id})}'
                data-tooltip="Validar">
                <span class="icon">
                    <i class="mdi mdi-magnify mdi-24px"></i>
                </span>
            </a>
            """

        segundo_botao = ""
        alerta = "Tem certeza que quer apagar a sala?"
        if segundo_botao == "":
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


class InscricaoTableProponenteValidados(django_tables.Table):
    # Os nomes que aparecem na tabela
    id = django_tables.Column(visible=False)
    eventoid = django_tables.Column('Evento')
    requer_certificado = django_tables.Column('Pretende Receber um Certificado?')
    presenca = django_tables.Column('Esteve Presente no Evento?')
    datainscricao = django_tables.Column('Realizou a inscrição no dia')
    participanteutilizadorid = django_tables.Column('Participante')
    estado = django_tables.Column(visible=False)
    filterset_class = InscricaoFilter
    acoes = django_tables.Column('Ações', empty_values=(),
                                 orderable=False, attrs={"th": {"width": "150"}})

    class Meta:
        template_name = 'inscricao/bulma_table.html'
        sequence = ('eventoid', 'requer_certificado', 'presenca', 'datainscricao')

    def render_requer_certificado(self, value):
        if value == True:
            return "Sim"
        else:
            return "Não"

    def render_presenca(self, value, record):
        if value == True:
            return format_html(f"""
                <div><a class="button is-success small" href='{reverse('checkout', args=[record.id])}'>Presente</a></div>""")
        else:
            return format_html(f"""
                <div><a class="button is-danger small" href='{reverse('checkin', args=[record.id])}'>Ausente</a></div>""")

    def render_estado(self, value):
        if value == 1:
            return format_html(
                '<div><button class="button is-warning small"style="pointer-events:none;">Pendente</button></div>')
        elif value == 2:
            return format_html(
                '<div><button class="button is-success small"style="pointer-events:none;">Aprovado</button></div>')
        elif value == 3:
            return format_html(
                '<div><button class="button is-danger small"style="pointer-events:none;">Não Aprovado</button></div>')

    def render_acoes(self, record):
        primeiro_botao = """<span class="icon"></span>"""

        primeiro_botao = ""
        if self.request.user.role.role == 'Proponente':
            primeiro_botao = f"""
            <a href='#'
                data-tooltip="Editar">
                <span class="icon">
                    <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                </span>
            </a>
            """

        segundo_botao = ""
        alerta = "Tem certeza que quer apagar a inscricao?"
        if segundo_botao == "":
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
