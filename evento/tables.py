import django_tables2 as django_tables
from utilizadores.models import Administrador, Utilizador
from evento.models import Sala
from evento.models import Sala
from django.utils.html import format_html
from django.urls import reverse

class SalaTable(django_tables.Table):
    #Os nomes que aparecem na tabela
    capacidade = django_tables.Column(empty_values=(), order_by='Capacidade')
    nome = django_tables.Column('Nome')
    mobilidade_reduzida = django_tables.Column('Apropriado para as pessoas com a mobilidade reduzida?')
    edificioid = django_tables.Column('Edifício')
    acoes = django_tables.Column('Ações', empty_values=(),
                                 orderable=False, attrs={"th": {"width": "150"}})

    class Meta:
        model = Sala
        sequence = ('capacidade', 'nome', 'mobilidade_reduzida', 'edificioid', 'acoes')

    def before_render(self,request):
        self.columns.hide('fotos')
        self.columns.hide('id')
       
    def render_mobilidade_reduzida(self,value):
        print(value)
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
