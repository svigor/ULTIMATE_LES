# Generated by Django 3.2 on 2021-05-12 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('nome', models.IntegerField(blank=True, db_column='Nome', null=True)),
            ],
            options={
                'db_table': 'campus',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Edificio',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('nome', models.CharField(blank=True, db_column='Nome', max_length=255, null=True)),
            ],
            options={
                'db_table': 'edificio',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Equipamento',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('quantidade', models.IntegerField(db_column='Quantidade')),
            ],
            options={
                'db_table': 'equipamento',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('capacidade', models.IntegerField(db_column='Capacidade')),
                ('tipo', models.IntegerField(blank=True, db_column='Tipo', null=True)),
                ('aprovado', models.TextField(db_column='Aprovado')),
                ('dia', models.DateField(db_column='Dia')),
                ('hora_de_inicio', models.TimeField(blank=True, db_column='Hora de inicio', null=True)),
                ('duracao', models.IntegerField(db_column='Duracao')),
                ('campusid', models.IntegerField(blank=True, db_column='CampusID', null=True)),
            ],
            options={
                'db_table': 'evento',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'feedback',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Formulario',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'formulario',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Inscricao',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('requer_certificado', models.TextField(blank=True, db_column='Requer Certificado', null=True)),
                ('presenca', models.TextField(blank=True, db_column='Presenca', null=True)),
                ('eventoid', models.ForeignKey(db_column='EventoID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.evento')),
            ],
            options={
                'db_table': 'inscricao',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Opcoes',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('texto', models.CharField(blank=True, db_column='Texto', max_length=255, null=True)),
            ],
            options={
                'db_table': 'opcoes',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Pergunta',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('titulo', models.CharField(blank=True, db_column='Titulo', max_length=255, null=True)),
                ('formularioid', models.ForeignKey(db_column='FormularioID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.formulario')),
            ],
            options={
                'db_table': 'pergunta',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TipoDeEvento',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('nome', models.CharField(blank=True, db_column='Nome', max_length=255, null=True)),
            ],
            options={
                'db_table': 'tipo de evento',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TipoDeFormulario',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('nome', models.CharField(blank=True, db_column='Nome', max_length=255, null=True)),
            ],
            options={
                'db_table': 'tipo de formulario',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TipoDePergunta',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('nome', models.CharField(blank=True, db_column='Nome', max_length=255, null=True)),
            ],
            options={
                'db_table': 'tipo de pergunta',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TipoEquipamento',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('nome', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'tipo_equipamento',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TiposDeRecursos',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('tipo_de_recurso', models.IntegerField(blank=True, db_column='Tipo de recurso', null=True)),
            ],
            options={
                'db_table': 'tipos de recursos',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TipoServico',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('nome', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'tipo_servico',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Servicos',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('tipo', models.CharField(blank=True, db_column='Tipo', max_length=255, null=True)),
                ('preco_base', models.FloatField(db_column='Preco base')),
                ('tipo_servicoid', models.ForeignKey(db_column='Tipo_ServicoID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.tiposervico')),
            ],
            options={
                'db_table': 'servicos',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('capacidade', models.IntegerField(db_column='Capacidade')),
                ('fotos', models.ImageField(blank=True, db_column='Fotos', null=True, upload_to='salas')),
                ('nome', models.CharField(blank=True, db_column='Nome', max_length=255)),
                ('mobilidade_reduzida', models.BooleanField(db_column='Mobilidade reduzida')),
                ('edificioid', models.ForeignKey(db_column='EdificioID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.edificio')),
            ],
            options={
                'db_table': 'sala',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Respostas',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('texto', models.CharField(blank=True, db_column='Texto', max_length=255, null=True)),
                ('eventoid', models.ForeignKey(db_column='EventoID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.evento')),
                ('inscricaoid', models.ForeignKey(db_column='InscricaoID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.inscricao')),
                ('opcoesid', models.ForeignKey(db_column='OpcoesID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.opcoes')),
                ('perguntaid', models.ForeignKey(db_column='PerguntaID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.pergunta')),
            ],
            options={
                'db_table': 'respostas',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PeriodoServico',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('dia_inicial', models.DateField(blank=True, db_column='Dia inicial', null=True)),
                ('dia_final', models.DateField(blank=True, db_column='Dia final', null=True)),
                ('hora_de_inicio', models.TimeField(blank=True, db_column='Hora de inicio', null=True)),
                ('duracao', models.IntegerField(blank=True, db_column='Duracao', null=True)),
                ('eventoid', models.ForeignKey(db_column='EventoID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.evento')),
                ('servicosid', models.ForeignKey(db_column='ServicosID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.servicos')),
            ],
            options={
                'db_table': 'periodo_servico',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PeriodoSala',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('dia_inicial', models.DateField(blank=True, db_column='Dia inicial', null=True)),
                ('dia_final', models.DateField(blank=True, db_column='Dia final', null=True)),
                ('hora_de_inicio', models.TimeField(blank=True, db_column='Hora de inicio', null=True)),
                ('duraco', models.IntegerField(db_column='Duracao')),
                ('eventoid', models.ForeignKey(db_column='EventoID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.evento')),
                ('salaid', models.ForeignKey(db_column='SalaID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.sala')),
            ],
            options={
                'db_table': 'periodo_sala',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PeriodoEquipamento',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('dia_inicial', models.DateField(blank=True, db_column='Dia inicial', null=True)),
                ('dia_final', models.DateField(blank=True, db_column='Dia final', null=True)),
                ('hora_de_inicio', models.TimeField(blank=True, db_column='Hora de inicio', null=True)),
                ('duracao', models.IntegerField(blank=True, db_column='Duracao', null=True)),
                ('equipamentoid', models.ForeignKey(db_column='EquipamentoID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.equipamento')),
                ('eventoid', models.ForeignKey(db_column='EventoID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.evento')),
            ],
            options={
                'db_table': 'periodo_equipamento',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='pergunta',
            name='tipo_de_perguntaid',
            field=models.ForeignKey(db_column='Tipo de PerguntaID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.tipodepergunta'),
        ),
        migrations.AddField(
            model_name='opcoes',
            name='perguntaid',
            field=models.ForeignKey(db_column='PerguntaID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.pergunta'),
        ),
        migrations.CreateModel(
            name='Logistica',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('quantidade', models.IntegerField(blank=True, db_column='Quantidade', null=True)),
                ('dia_inicial', models.DateField(blank=True, db_column='Dia inicial', null=True)),
                ('dia_final', models.DateField(blank=True, db_column='Dia final', null=True)),
                ('hora_de_inicio', models.TimeField(blank=True, db_column='Hora de inicio', null=True)),
                ('duracao', models.IntegerField(blank=True, db_column='Duracao', null=True)),
                ('valido', models.TextField(blank=True, db_column='Valido', null=True)),
                ('capacidade', models.IntegerField(blank=True, db_column='Capacidade', null=True)),
                ('eventoid', models.ForeignKey(db_column='EventoID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.evento')),
                ('tipo_equipamentoid', models.ForeignKey(db_column='Tipo_EquipamentoID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.tipoequipamento')),
                ('tipo_servicoid', models.ForeignKey(db_column='Tipo_ServicoID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.tiposervico')),
                ('tipos_de_recursosid', models.ForeignKey(db_column='Tipos de recursosID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.tiposderecursos')),
            ],
            options={
                'db_table': 'logistica',
                'managed': True,
            },
        ),
    ]
