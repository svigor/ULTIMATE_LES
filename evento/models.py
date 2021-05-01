# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse
from utilizadores.models import Participante, Proponente, Administrador
from django.db.models.signals import pre_save
import os


class Campus(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    nome = models.IntegerField(db_column='Nome', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'campus'

    def __str__(slef):
        return slef.nome


class Edificio(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    nome = models.CharField(
        db_column='Nome', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    campusid = models.ForeignKey(
        Campus, models.DO_NOTHING, db_column='CampusID')

    def __str__(self):
        return self.nome

    class Meta:
        managed = True
        db_table = 'edificio'


class Equipamento(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    quantidade = models.IntegerField(db_column='Quantidade')
    # Field name made lowercase.
    tipo_equipamentoid = models.ForeignKey(
        'TipoEquipamento', models.DO_NOTHING, db_column='Tipo_EquipamentoID')

    class Meta:
        managed = True
        db_table = 'equipamento'


class Evento(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    capacidade = models.IntegerField(db_column='Capacidade')
    # Field name made lowercase.
    tipo = models.IntegerField(db_column='Tipo', blank=True, null=True)
    # Field name made lowercase. This field type is a guess.
    aprovado = models.TextField(db_column='Aprovado')
    dia = models.DateField(db_column='Dia')  # Field name made lowercase.
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    hora_de_inicio = models.TimeField(
        db_column='Hora de inicio', blank=True, null=True)
    # Field name made lowercase.
    duracao = models.IntegerField(db_column='Duracao')
    # Field name made lowercase.
    campusid = models.IntegerField(db_column='CampusID', blank=True, null=True)
    # Field name made lowercase.
    formularioinscricaoid = models.ForeignKey(
        'Formulario', models.DO_NOTHING, db_column='FormularioInscricaoID', related_name='capacidade')
    # Field name made lowercase.
    formulariofeedbackid = models.ForeignKey(
        'Formulario', models.DO_NOTHING, db_column='FormularioFeedbackID', related_name='tipo')
    # Field name made lowercase.
    proponenteutilizadorid = models.ForeignKey(
        Proponente, models.DO_NOTHING, db_column='ProponenteUtilizadorID', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'evento'


class Feedback(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    eventoid = models.ForeignKey(
        Evento, models.DO_NOTHING, db_column='EventoID')
    # Field name made lowercase.
    participanteutilizadorid = models.ForeignKey(
        Participante, models.DO_NOTHING, db_column='ParticipanteUtilizadorID', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'feedback'


class Formulario(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    tipo_de_eventoid = models.ForeignKey(
        'TipoDeEvento', models.DO_NOTHING, db_column='Tipo de EventoID')
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    tipo_de_formularioid = models.ForeignKey(
        'TipoDeFormulario', models.DO_NOTHING, db_column='Tipo de FormularioID')

    class Meta:
        managed = True
        db_table = 'formulario'


class Inscricao(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    eventoid = models.ForeignKey(
        Evento, models.DO_NOTHING, db_column='EventoID')
    # Field name made lowercase. Field renamed to remove unsuitable characters. This field type is a guess.
    requer_certificado = models.TextField(
        db_column='Requer Certificado', blank=True, null=True)
    # Field name made lowercase. This field type is a guess.
    presenca = models.TextField(db_column='Presenca', blank=True, null=True)
    # Field name made lowercase.
    participanteutilizadorid = models.ForeignKey(
        Participante, models.DO_NOTHING, db_column='ParticipanteUtilizadorID', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'inscricao'


class Logistica(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    eventoid = models.ForeignKey(
        Evento, models.DO_NOTHING, db_column='EventoID')
    # Field name made lowercase.
    quantidade = models.IntegerField(
        db_column='Quantidade', blank=True, null=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    dia_inicial = models.DateField(
        db_column='Dia inicial', blank=True, null=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    dia_final = models.DateField(db_column='Dia final', blank=True, null=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    hora_de_inicio = models.TimeField(
        db_column='Hora de inicio', blank=True, null=True)
    # Field name made lowercase.
    duracao = models.IntegerField(db_column='Duracao', blank=True, null=True)
    # Field name made lowercase. This field type is a guess.
    valido = models.TextField(db_column='Valido', blank=True, null=True)
    # Field name made lowercase.
    capacidade = models.IntegerField(
        db_column='Capacidade', blank=True, null=True)
    # Field name made lowercase.
    tipo_servicoid = models.ForeignKey(
        'TipoServico', models.DO_NOTHING, db_column='Tipo_ServicoID')
    # Field name made lowercase.
    tipo_equipamentoid = models.ForeignKey(
        'TipoEquipamento', models.DO_NOTHING, db_column='Tipo_EquipamentoID')
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    tipos_de_recursosid = models.ForeignKey(
        'TiposDeRecursos', models.DO_NOTHING, db_column='Tipos de recursosID')

    class Meta:
        managed = True
        db_table = 'logistica'


class Opcoes(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    texto = models.CharField(
        db_column='Texto', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    perguntaid = models.ForeignKey(
        'Pergunta', models.DO_NOTHING, db_column='PerguntaID')

    class Meta:
        managed = True
        db_table = 'opcoes'


class Pergunta(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    titulo = models.CharField(
        db_column='Titulo', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    formularioid = models.ForeignKey(
        Formulario, models.DO_NOTHING, db_column='FormularioID')
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    tipo_de_perguntaid = models.ForeignKey(
        'TipoDePergunta', models.DO_NOTHING, db_column='Tipo de PerguntaID')

    class Meta:
        managed = True
        db_table = 'pergunta'


class PeriodoEquipamento(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    dia_inicial = models.DateField(
        db_column='Dia inicial', blank=True, null=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    dia_final = models.DateField(db_column='Dia final', blank=True, null=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    hora_de_inicio = models.TimeField(
        db_column='Hora de inicio', blank=True, null=True)
    # Field name made lowercase.
    duracao = models.IntegerField(db_column='Duracao', blank=True, null=True)
    # Field name made lowercase.
    equipamentoid = models.ForeignKey(
        Equipamento, models.DO_NOTHING, db_column='EquipamentoID')
    # Field name made lowercase.
    eventoid = models.ForeignKey(
        Evento, models.DO_NOTHING, db_column='EventoID')

    class Meta:
        managed = True
        db_table = 'periodo_equipamento'


class PeriodoSala(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    dia_inicial = models.DateField(
        db_column='Dia inicial', blank=True, null=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    dia_final = models.DateField(db_column='Dia final', blank=True, null=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    hora_de_inicio = models.TimeField(
        db_column='Hora de inicio', blank=True, null=True)
    # Field name made lowercase.
    duraco = models.IntegerField(db_column='Duracao')
    # Field name made lowercase.
    salaid = models.ForeignKey('Sala', models.DO_NOTHING, db_column='SalaID')
    # Field name made lowercase.
    eventoid = models.ForeignKey(
        Evento, models.DO_NOTHING, db_column='EventoID')

    class Meta:
        managed = True
        db_table = 'periodo_sala'


class PeriodoServico(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    dia_inicial = models.DateField(
        db_column='Dia inicial', blank=True, null=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    dia_final = models.DateField(db_column='Dia final', blank=True, null=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    hora_de_inicio = models.TimeField(
        db_column='Hora de inicio', blank=True, null=True)
    # Field name made lowercase.
    duracao = models.IntegerField(db_column='Duracao', blank=True, null=True)
    # Field name made lowercase.
    servicosid = models.ForeignKey(
        'Servicos', models.DO_NOTHING, db_column='ServicosID')
    # Field name made lowercase.
    eventoid = models.ForeignKey(
        Evento, models.DO_NOTHING, db_column='EventoID')

    class Meta:
        managed = True
        db_table = 'periodo_servico'


class Respostas(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    perguntaid = models.ForeignKey(
        Pergunta, models.DO_NOTHING, db_column='PerguntaID')
    # Field name made lowercase.
    texto = models.CharField(
        db_column='Texto', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    opcoesid = models.ForeignKey(
        Opcoes, models.DO_NOTHING, db_column='OpcoesID')
    # Field name made lowercase.
    eventoid = models.ForeignKey(
        Evento, models.DO_NOTHING, db_column='EventoID')
    # Field name made lowercase.
    inscricaoid = models.ForeignKey(
        Inscricao, models.DO_NOTHING, db_column='InscricaoID')

    class Meta:
        managed = True
        db_table = 'respostas'


class Sala(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    capacidade = models.IntegerField(db_column='Capacidade')
    # Field name made lowercase.
    fotos = models.ImageField(
        db_column='Fotos', upload_to='salas', null=True, blank=True)
    # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters. This field type is a guess.
    mobilidade_reduzida = models.BooleanField(db_column='Mobilidade reduzida')
    # Field name made lowercase.
    edificioid = models.ForeignKey(
        Edificio, models.DO_NOTHING, db_column='EdificioID')

    class Meta:
        managed = True
        db_table = 'sala'

    def get_absolute_url(self):
        return reverse('home')

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.image.storage, self.image.path
        # Delete the model before the file
        super(Sala, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)


class Servicos(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    tipo = models.CharField(
        db_column='Tipo', max_length=255, blank=True, null=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    preco_base = models.FloatField(db_column='Preco base')
    # Field name made lowercase.
    tipo_servicoid = models.ForeignKey(
        'TipoServico', models.DO_NOTHING, db_column='Tipo_ServicoID')

    class Meta:
        managed = True
        db_table = 'servicos'


class TipoDeEvento(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    nome = models.CharField(
        db_column='Nome', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    eventoid = models.ForeignKey(
        Evento, models.DO_NOTHING, db_column='EventoID')

    class Meta:
        managed = True
        db_table = 'tipo de evento'


class TipoDeFormulario(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    nome = models.CharField(
        db_column='Nome', max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tipo de formulario'


class TipoDePergunta(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    nome = models.CharField(
        db_column='Nome', max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tipo de pergunta'


class TipoEquipamento(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    nome = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tipo_equipamento'


class TipoServico(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    nome = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tipo_servico'


class TiposDeRecursos(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    tipo_de_recurso = models.IntegerField(
        db_column='Tipo de recurso', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tipos de recursos'
