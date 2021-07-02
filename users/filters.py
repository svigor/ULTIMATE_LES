import django_filters as filters
from django.forms import SelectMultiple
from users.models import MyUser

get_interno_reduzida = [
    (1, 'Interno'),
    (0, 'Externo')
]

get_roles = [
    (1, 'Participante'),
    (2, 'Proponente'),
    (3, 'Administrador')
]


class usersfilter(filters.FilterSet):
    interno = filters.MultipleChoiceFilter(choices=get_interno_reduzida)
    role = filters.MultipleChoiceFilter(choices=get_roles)

    class Meta:
        model = MyUser
        fields = ('interno', 'role')
