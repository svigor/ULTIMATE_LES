# Generated by Django 3.2 on 2021-05-17 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evento', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pergunta',
            name='formularioid',
            field=models.ForeignKey(db_column='FormularioID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='evento.formulario'),
        ),
    ]