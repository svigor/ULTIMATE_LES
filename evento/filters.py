import django_filters
from evento.models import Inscricao
from django.db.models import Q

class InscricaoFilter(django_filters.FilterSet):

    class Meta:
        model = Inscricao
        fields =  ['eventoid', 'requer_certificado']