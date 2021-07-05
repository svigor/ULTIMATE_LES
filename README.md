# ULTIMATE_LES
Gestão de eventos

## No ficheiro Setting não estão as credenciais da base de dados.
### Para poder usar 100% o potencial do software têm que criar um superuser
    1. Fazer make migrations -> python manage.py makemigrations evento formulario inscricao recursos users (Poderão ter que fazer drop das tabelas na base de dados)
    2. Fazer migrate -> python manage.py migrate (Atenção se aparecer um erro como les.campus nao existir ou algo parecido vou a evento/forms e no c_s_form comentei tudo dessa classe depois quando fizerem o migrate descomentem)
    3. adicionar manualmente os campus na base de dados (Gambelas, Penha, Portimão)
    4. Por fim fazer superuser -> python manage.py createsuperuser
