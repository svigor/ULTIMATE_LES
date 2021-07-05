import django_filters as filters
from django.forms import SelectMultiple

from .models import Evento, Logistica
from users.models import MyUser

get_aprovado = [
    (0, 'Não Aprovado'),
    (1, 'Pendente')
]

get_valido_choices = [
    (1,'Sim'),
    (0,'Não')
]


class eventofilter(filters.FilterSet):
    aprovado = filters.MultipleChoiceFilter(choices=get_aprovado)


    class Meta:
        model = Evento
        fields = ('campusid', 'aprovado', 'tipo_de_eventoid', 'proponenteutilizadorid')

class LogisticasFilter(filters.FilterSet):
    valido = filters.MultipleChoiceFilter(choices=get_valido_choices)
    class Meta:
        model = Logistica
        fields = ['valido']
