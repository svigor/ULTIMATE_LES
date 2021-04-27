import django_filters
from evento.models import Sala
from django.db.models import Q



class SalasFilter(django_filters.FilterSet):
 
    class Meta:
        model = Sala
        fields = ['capacidade', 'nome', 'mobilidade_reduzida', 'edificioid']
