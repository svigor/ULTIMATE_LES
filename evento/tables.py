import django_tables2 as django_tables
from utilizadores.models import Administrador, Utilizador
from evento.models import Sala
from django.utils.html import format_html
from django.urls import reverse

class SalaTable(django_tables.Table):
    #Os nomes que aparecem na tabela
    capacidade = django_tables.Column(empty_values=(), order_by='Capacidade')
    nome = django_tables.Column('Nome')
    mobilidade_reduzida = django_tables.Column('Apropriado para a mobilidade reduzida')
    edificioid = django_tables.Column('Edifício')

    class Meta:
        model = Sala
        sequence = ('capacidade', 'nome', 'mobilidade_reduzida', 'edificioid')

    def before_render(self,request):
        self.columns.hide('fotos')
        self.columns.hide('id')
