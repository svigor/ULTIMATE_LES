import django_tables2 as django_tables
from utilizadores.models import Administrador, Utilizador
from evento.models import Sala
from django.utils.html import format_html
from django.urls import reverse

class SalaTable(django_tables.Table):
    capacidade = django_tables.Column(empty_values=(), order_by='capacidade')
    nome = django_tables.Column('Nome')
    mobilidade_reduzida = django_tables.Column('mobilidade_reduzida')
    edificioid = django_tables.Column('edificioid')

    class Meta:
        model = Sala
        sequence = ('capacidade', 'nome', 'mobilidade_reduzida', 'edificioid')

    def before_render(self,request):
        self.columns.hide('fotos')
