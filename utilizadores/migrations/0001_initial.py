# Generated by Django 3.2 on 2021-05-09 15:20

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Utilizador',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('contacto', models.CharField(max_length=20)),
                ('valido', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Utilizador',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('utilizador_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='utilizadores.utilizador')),
                ('gabinete', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Administrador',
            },
            bases=('utilizadores.utilizador',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Participante',
            fields=[
                ('utilizador_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='utilizadores.utilizador')),
            ],
            options={
                'db_table': 'Participante',
            },
            bases=('utilizadores.utilizador',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Proponente',
            fields=[
                ('utilizador_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='utilizadores.utilizador')),
            ],
            options={
                'db_table': 'Proponente',
            },
            bases=('utilizadores.utilizador',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
