import django_filters
from evento.models import Sala
from django.db.models import Q

get_mobilidade_reduzida_choices = [
    ('True','Sim'),
    ('False','Não')
]




class SalasFilter(django_filters.FilterSet):
    mobilidade_reduzida = django_filters.MultipleChoiceFilter(choices=get_mobilidade_reduzida_choices)

    class Meta:
        model = Sala
        fields = ['capacidade', 'nome', 'mobilidade_reduzida', 'edificioid']
