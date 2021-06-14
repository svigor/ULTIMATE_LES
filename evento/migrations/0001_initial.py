# Generated by Django 3.2 on 2021-06-14 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('campusid', models.ForeignKey(db_column='CampusID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.campus')),
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
                ('nome', models.CharField(blank=True, db_column='Nome', max_length=255, null=True)),
                ('descricao', models.CharField(blank=True, db_column='Descricao', max_length=255, null=True)),
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
                ('aprovado', models.TextField(db_column='Aprovado')),
                ('dia', models.DateField(db_column='Dia')),
                ('hora_de_inicio', models.TimeField(blank=True, db_column='Hora de inicio', null=True)),
                ('duracao', models.IntegerField(db_column='Duracao')),
                ('campusid', models.ForeignKey(db_column='CampusID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.campus')),
            ],
            options={
                'db_table': 'evento',
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
                ('participanteutilizadorid', models.ForeignKey(blank=True, db_column='ParticipanteUtilizadorID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'inscricao',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Logistica',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('valido', models.IntegerField(blank=True, db_column='Valido', null=True)),
                ('eventoid', models.ForeignKey(db_column='EventoID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.evento')),
            ],
            options={
                'db_table': 'logistica',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Notificacoes',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('descricao', models.CharField(blank=True, db_column='Descricao', max_length=255, null=True)),
                ('criadoem', models.IntegerField(blank=True, db_column='CriadoEm', null=True)),
            ],
            options={
                'db_table': 'notificacoes',
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
            name='TipoSala',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('nome', models.CharField(blank=True, db_column='Nome', max_length=255, null=True)),
            ],
            options={
                'db_table': 'tipo de sala',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TiposDeRecursos',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('nome', models.CharField(blank=True, db_column='Nome', max_length=255, null=True)),
                ('tipo_de_recurso', models.IntegerField(blank=True, db_column='Tipo de recurso', null=True)),
            ],
            options={
                'db_table': 'tipos_de_recursos',
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
                ('nome', models.CharField(blank=True, db_column='Nome', max_length=255, null=True)),
                ('descricao', models.CharField(blank=True, db_column='Descricao', max_length=255, null=True)),
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
                ('tipo_salaid', models.ForeignKey(db_column='Tipo_SalaID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.tiposala')),
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
                ('duração', models.IntegerField(db_column='Duração')),
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
        migrations.CreateModel(
            name='Periodo_logistica',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('dia_inicial', models.DateField(blank=True, db_column='Dia inicial', null=True)),
                ('dia_final', models.DateField(blank=True, db_column='Dia final', null=True)),
                ('hora_de_inicio', models.TimeField(blank=True, db_column='Hora de inicio', null=True)),
                ('hora_de_fim', models.TimeField(blank=True, db_column='Hora de fim', null=True)),
                ('logistica_id', models.ForeignKey(db_column='LogisticaID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.logistica')),
                ('tipos_de_recursosid', models.ForeignKey(db_column='Tipos de recursosID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.tiposderecursos')),
            ],
            options={
                'db_table': 'periodo_logistica',
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
        migrations.AddField(
            model_name='formulario',
            name='tipo_de_eventoid',
            field=models.ForeignKey(db_column='Tipo de EventoID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.tipodeevento'),
        ),
        migrations.AddField(
            model_name='formulario',
            name='tipo_de_formularioid',
            field=models.ForeignKey(db_column='Tipo de FormularioID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.tipodeformulario'),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('inscricaoid', models.ForeignKey(db_column='InscricaoID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.inscricao')),
            ],
            options={
                'db_table': 'feedback',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='evento',
            name='formulariofeedbackid',
            field=models.ForeignKey(db_column='FormularioFeedbackID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='formfeedid', to='evento.formulario'),
        ),
        migrations.AddField(
            model_name='evento',
            name='formularioinscricaoid',
            field=models.ForeignKey(db_column='FormularioInscricaoID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='evento.formulario'),
        ),
        migrations.AddField(
            model_name='evento',
            name='proponenteutilizadorid',
            field=models.ForeignKey(blank=True, db_column='ProponenteUtilizadorID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='evento',
            name='tipo_de_eventoid',
            field=models.ForeignKey(db_column='Tipo de EventoID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.tipodeevento'),
        ),
        migrations.AddField(
            model_name='equipamento',
            name='tipo_equipamentoid',
            field=models.ForeignKey(db_column='Tipo_EquipamentoID', on_delete=django.db.models.deletion.DO_NOTHING, to='evento.tipoequipamento'),
        ),
    ]