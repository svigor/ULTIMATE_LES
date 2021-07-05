from django.utils.html import format_html
from django_tables2 import tables
from users.models import MyUser, pedidomudar
from django.urls import reverse


class Myuserstable(tables.Table):
    n_telefone = tables.columns.Column('telefone')
    email = tables.columns.Column('email')

    def render_interno(self, value):
        if value == True:
            return 'Yes'
        else:
            return 'No'

    class Meta:
        model = MyUser
        template_name = 'users/bulma_table.html'
        fields = ('id', 'email', 'NomeProprio', 'SecondName', 'date_of_birth', 'n_telefone', 'interno', 'role')


class pedidos(tables.Table):
    id = tables.columns.Column('id')
    usuario = tables.columns.Column('Nome:')
    email = tables.columns.Column('Email:', accessor='return_email')
    current_role = tables.columns.Column('Perfil Atual', accessor='return_role')
    asked_role = tables.columns.Column('Perfil Pedido')
    acoes = tables.columns.Column('Ações', empty_values=(), orderable=False, attrs={"th": {"width": "150"}})

    class Meta:
        fields = ('id', 'usuario', 'email', 'current_role', 'asked_role')
        model = pedidomudar
        template_name = 'users/bulma_table.html'

    def before_render(self, request):
        self.columns.hide('id')

    def render_acoes(self, record):
        primeiro_botao = f"""
                    <a href='{reverse('aceitar', args=[record.id])}'
                        data-tooltip="Aceitar Pedido">
                        <span class="icon">
                            <i class="mdi mdi-check mdi-24px"></i>
                        </span>
                    </a>
                    """
        segundo_botao = f"""
                    <a href='{reverse('recusar', args=[record.id])}'
                        data-tooltip="Recusar Pedido">
                        <span class="icon">
                            <i style="color:red;" class="mdi mdi-window-close mdi-24px"></i>
                        </span>
                    </a>
                    """
        return format_html(
            f"""<div class="columns is-gapless"><div class=column>{primeiro_botao}</div><div class=column>{segundo_botao}</div></div>""")
