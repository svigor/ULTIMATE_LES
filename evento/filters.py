from django.db.models import query
from django.db.models.query import QuerySet
import django_filters
from evento.models import Equipamento, Logistica, Sala, Campus, Edificio, Servicos
from django.db.models import Q

get_mobilidade_reduzida_choices = [
    ('True','Sim'),
    ('False','Não')
]

get_valido_choices = [
    (1,'Sim'),
    (0,'Não')
]


class SalasFilter(django_filters.FilterSet):
    mobilidade_reduzida = django_filters.MultipleChoiceFilter(choices=get_mobilidade_reduzida_choices)

    class Meta:
        model = Sala
        fields = ['capacidade', 'nome', 'mobilidade_reduzida', 'edificioid','tipo_salaid']

class ServicosFilter(django_filters.FilterSet):
    class Meta:
        model = Servicos
        fields = ['nome', 'preco_base', 'tipo_servicoid']


class EquipamentosFilter(django_filters.FilterSet):
    class Meta:
        model = Equipamento
        fields = ['tipo_equipamentoid', 'nome']


class LogisticasFilter(django_filters.FilterSet):
    valido = django_filters.MultipleChoiceFilter(choices=get_valido_choices)
    class Meta:
        model = Logistica
        fields = ['valido']



