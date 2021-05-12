import django_filters as filters
from django.forms import SelectMultiple

from .models import Evento
from users.models import MyUser

get_aprovado_reduzida = [
    (1, 'Aprovado'),
    (0, 'Não Aprovado')
]




class eventofilter(filters.FilterSet):
    aprovado = filters.MultipleChoiceFilter(choices=get_aprovado_reduzida)


    class Meta:
        model = Evento
        fields = ('campusid', 'aprovado', 'tipo_de_eventoid', 'proponenteutilizadorid')
