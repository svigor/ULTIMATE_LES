from django.forms import fields
import django_filters
from evento.models import Sala, Formulario
from django.db.models import Q

get_mobilidade_reduzida_choices = [
    ('True','Sim'),
    ('False','Não')
]

get_tipo_de_formularioid_choices = [
    ('1','Evento'),
    ('2','Inscrição'),
    ('3','Feedback')
]


class SalasFilter(django_filters.FilterSet):
    mobilidade_reduzida = django_filters.MultipleChoiceFilter(choices=get_mobilidade_reduzida_choices)

    class Meta:
        model = Sala
        fields = ['capacidade', 'nome', 'mobilidade_reduzida', 'edificioid']

class FormulariosFilter(django_filters.FilterSet):
    tipo_de_formularioid = django_filters.MultipleChoiceFilter(choices=get_tipo_de_formularioid_choices)
    
    class Meta:
        model = Formulario
        fields = ['tipo_de_formularioid']