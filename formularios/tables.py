import django_tables2 as django_tables
from evento.models import Evento, Pergunta, Formulario
from django.utils.html import format_html
from django.urls import reverse


class FormularioTable(django_tables.Table):
    tipo_de_formularioid = django_tables.Column('Tipo de Formulário')
    tipo_de_eventoid = django_tables.Column('Tipo de Evento')
    disponibilidade = django_tables.Column('Disponibilidade')
    acoes = django_tables.Column('Ações', empty_values=(), orderable=False, attrs={"th": {"width": "150"}})

    def render_tipo_de_formularioid(self, value):
        return value.nome

    def render_tipo_de_eventoid(self, value):
        return value.nome

    def render_disponibilidade(self, value):
        if value == 0:
            return format_html(
                '<div><button class="button is-danger small"style="pointer-events:none;">Privado</button></div>')
        elif value == 1:
            return format_html(
                '<div><button class="button is-success small"style="pointer-events:none;">Disponível</button></div>')

    # def before_render(self,request):
    #     self.columns.hide('id')

    def render_acoes(self, record):
        if Formulario.objects.get(pk=record.id).disponibilidade == 0:
            primeiro_botao = f"""
                <a href='{reverse('disponibilizar-formulario', args={record.id})}'
                    data-tooltip="Disponibilizar">
                    <span class="icon">
                        <i class="mdi mdi-inbox-arrow-up mdi-24px" style="color:green;"></i>
                    </span>
                </a>
                """
        else:
            primeiro_botao = ''

        segundo_botao = f"""
            <a href='{reverse('consultar-perguntas-formulario', args={record.id})}'
                data-tooltip="Visualizar">
                <span class="icon">
                    <i class="mdi mdi-magnify mdi-24px"></i>
                </span>
            </a>
            """
        if not Evento.objects.filter(
                formularioinscricaoid=Formulario.objects.get(id=record.id)) and not Evento.objects.filter(
                formulariofeedbackid=Formulario.objects.get(id=record.id)):
            terceiro_botao = f"""
                <a href='{reverse('alterar-formulario', args={record.id})}'
                    data-tooltip="Editar">
                    <span class="icon">
                        <i class="mdi mdi-pencil mdi-24px"></i>
                    </span>
                </a>
                """
        else:
            terceiro_botao = f"""
                    <span class="icon">
                        <i class="mdi mdi-pencil mdi-24px" style='color:gray;'></i>
                    </span>
                """

        if not Evento.objects.filter(
                formularioinscricaoid=Formulario.objects.get(id=record.id)) and not Evento.objects.filter(
                formulariofeedbackid=Formulario.objects.get(id=record.id)):
            alerta = "Tem certeza que quer apagar a sala?"
            quarto_botao = f"""
                <a onclick="alert.render('{alerta}','{reverse('apagar-form', args=[record.id])}')"
                    data-tooltip="Apagar">
                    <span class="icon has-text-danger">
                        <i class="mdi mdi-trash-can mdi-24px"></i>
                    </span>
                </a>
            """
        else:
            quarto_botao = f"""
                    <span class="icon">
                        <i class="mdi mdi-trash-can mdi-24px" style="color: gray"></i>
                    </span>
            """
        return format_html(f"""
        <div>
            {primeiro_botao}
            {segundo_botao}
            {terceiro_botao}
            {quarto_botao}
        </div>
        """)

    class Meta:
        model = Formulario
        template_name = 'recursos/bulma_table.html'
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
        if not value.tipo_de_formularioid.nome == "Evento":
            return "(%d) " % value.id + "%s" % value.tipo_de_formularioid.nome
        else:
            return "(%d) " % value.id + "%s " % value.tipo_de_formularioid.nome + "%s " % value.tipo_de_eventoid.nome

    def before_render(self, request):
        self.columns.hide('id')

    def render_acoes(self, record):
        tipo = Pergunta.objects.get(id=record.id).tipo_de_perguntaid.nome
        if tipo == 'Caixa de seleção' or tipo == 'Escolha múltipla':
            primeiro_botao = f"""
                <a href='{reverse('consultar-opcoes', args={record.id})}'
                    data-tooltip="Visualizar Opções">
                    <span class="icon">
                        <i class="mdi mdi-magnify mdi-24px"></i>
                    </span>
                </a>
                """
        else:
            primeiro_botao = f"""
            <span class="icon">
                <i class="mdi mdi-magnify mdi-24px" style="color: gray"></i>
            </span>
            """
        formulario = Pergunta.objects.get(id=record.id).formularioid
        if not Evento.objects.filter(formularioinscricaoid=formulario) and not Evento.objects.filter(
                formulariofeedbackid=formulario):
            segundo_botao = f"""
                <a href='{reverse('alterar-pergunta', args={record.id})}'
                    data-tooltip="Editar">
                    <span class="icon">
                        <i class="mdi mdi-pencil mdi-24px"></i>
                    </span>
                </a>
                """
        else:
            segundo_botao = f"""
                    <span class="icon">
                        <i class="mdi mdi-pencil mdi-24px" style='color:gray;'></i>
                    </span>
                """

        if not Evento.objects.filter(formularioinscricaoid=formulario) and not Evento.objects.filter(
                formulariofeedbackid=formulario):
            alerta = "Tem certeza que quer apagar a sala?"
            terceiro_botao = f"""
                <a onclick="alert.render('{alerta}','{reverse('apagar-pergunta', args=[record.id])}')"
                    data-tooltip="Apagar">
                    <span class="icon has-text-danger">
                        <i class="mdi mdi-trash-can mdi-24px"></i>
                    </span>
                </a>
            """
        else:
            terceiro_botao = f"""
                    <span class="icon">
                        <i class="mdi mdi-trash-can mdi-24px" style="color: gray"></i>
                    </span>
            """
        return format_html(f"""
        <div>
            {primeiro_botao}
            {segundo_botao}
            {terceiro_botao}
        </div>
        """)

    class Meta:
        model = Pergunta
        template_name = 'formularios/bulma_table.html'
        fields = ('id', 'titulo', 'tipo_de_perguntaid', 'formularioid')
