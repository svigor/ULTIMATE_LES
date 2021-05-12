from django_tables2 import tables
from users.models import MyUser


class Myuserstable(tables.Table):
    n_telefone = tables.columns.Column('telefone')
    email = tables.columns.Column('email')

    def render_interno(self, value):
        if value == True:
            return 'Yes'
        else:
            return 'No'
    class Meta:
        model = MyUser
        template_name = 'users/bulma_table.html'
        fields = ('id', 'email', 'NomeProprio', 'SecondName', 'date_of_birth', 'n_telefone', 'interno', 'role')