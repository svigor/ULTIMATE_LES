from datetime import date

from django.db import models
from django.urls import reverse

from users.models import MyUser


class Campus(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Campus'

    def __str__(self):
        return self.nome


class Edificio(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    campusid = models.ForeignKey(Campus, models.DO_NOTHING, db_column='CampusID')  # Field name made lowercase.

    def __str__(self):
        return self.nome

    class Meta:
        managed = True
        db_table = 'edificio'


class Equipamento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)
    descricao = models.CharField(db_column='Descricao', max_length=255, blank=True, null=True)
    tipo_equipamentoid = models.ForeignKey('TipoEquipamento', models.DO_NOTHING,
                                           db_column='Tipo_EquipamentoID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'equipamento'


class Evento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)
    capacidade = models.IntegerField(db_column='Capacidade')  # Field name made lowercase.
    aprovado = models.IntegerField(db_column='Aprovado')  # Field name made lowercase. This field type is a guess.
    dia = models.DateField(db_column='Dia')  # Field name made lowercase.
    diaFinal = models.DateField(db_column='Dia Final')
    hora_de_inicio = models.TimeField(db_column='Hora de inicio', blank=True,
                                      null=True)
    duracao = models.IntegerField(db_column='Duracao')  # Field name made lowercase.
    campusid = models.ForeignKey(Campus, models.DO_NOTHING, db_column='CampusID')  # Field name made lowercase.
    formularioinscricaoid = models.ForeignKey('Formulario', models.DO_NOTHING,
                                              db_column='FormularioInscricaoID',
                                              null=True)  # Field name made lowercase.
    formulariofeedbackid = models.ForeignKey('Formulario', models.DO_NOTHING, db_column='FormularioFeedbackID',
                                             related_name='formfeedid', null=True)  # Field name made lowercase.
    proponenteutilizadorid = models.ForeignKey(MyUser, models.DO_NOTHING, db_column='ProponenteUtilizadorID',
                                               blank=True, null=True)  # Field name made lowercase.
    tipo_de_eventoid = models.ForeignKey('TipoDeEvento', models.DO_NOTHING,
                                         db_column='Tipo de EventoID')  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = True
        db_table = 'evento'

    def __str__(self):
        return self.nome


class Feedback(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    inscricaoid = models.ForeignKey('Inscricao', models.DO_NOTHING,
                                    db_column='InscricaoID')

    class Meta:
        managed = True
        db_table = 'feedback'


class Formulario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    tipo_de_eventoid = models.ForeignKey('TipoDeEvento', models.DO_NOTHING,
                                         db_column='Tipo de EventoID',
                                         null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tipo_de_formularioid = models.ForeignKey('TipoDeFormulario', models.DO_NOTHING,
                                             db_column='Tipo de FormularioID')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    disponibilidade = models.IntegerField(db_column='disponibilidade', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'formulario'


class Inscricao(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    eventoid = models.ForeignKey(Evento, models.CASCADE, db_column='EventoID')  # Field name made lowercase.
    requer_certificado = models.TextField(db_column='Requer Certificado', blank=True,
                                          null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. This field type is a guess.
    presenca = models.BooleanField(db_column='Presenca', blank=True,
                                   null=True)  # Field name made lowercase. This field type is a guess.
    participanteutilizadorid = models.ForeignKey(MyUser, models.DO_NOTHING,
                                                 db_column='ParticipanteUtilizadorID', blank=True,
                                                 null=True)  # Field name made lowercase.
    datainscricao = models.DateField(db_column='Data de Inscricao', default=date.today, blank=True, null=False)
    estado = models.IntegerField(db_column='Estado', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'inscricao'


class Logistica(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    eventoid = models.ForeignKey(Evento, models.DO_NOTHING, db_column='EventoID')  # Field name made lowercase.
    quantidade = models.IntegerField(db_column='Quantidade', blank=True, null=True)  # Field name made lowercase.
    dia_inicial = models.DateField(db_column='Dia inicial', blank=True,
                                   null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dia_final = models.DateField(db_column='Dia final', blank=True,
                                 null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    hora_de_inicio = models.TimeField(db_column='Hora de inicio', blank=True,
                                      null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    duracao = models.IntegerField(db_column='Duracao', blank=True, null=True)  # Field name made lowercase.
    valido = models.TextField(db_column='Valido', blank=True,
                              null=True)  # Field name made lowercase. This field type is a guess.
    capacidade = models.IntegerField(db_column='Capacidade', blank=True, null=True)  # Field name made lowercase.
    tipo_servicoid = models.ForeignKey('TipoServico', models.DO_NOTHING, db_column='Tipo_ServicoID', blank=True,
                                       null=True)  # Field name made lowercase.
    tipo_equipamentoid = models.ForeignKey('TipoEquipamento', models.DO_NOTHING, db_column='Tipo_EquipamentoID',
                                           blank=True, null=True)  # Field name made lowercase.
    tipos_de_recursosid = models.ForeignKey('TiposDeRecursos', models.DO_NOTHING,
                                            db_column='Tipos de recursosID')  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = True
        db_table = 'logistica'


class Notificacoes(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255, blank=True,
                                 null=True)  # Field name made lowercase.
    criadoem = models.IntegerField(db_column='CriadoEm', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'notificacoes'


class Opcoes(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    texto = models.CharField(db_column='Texto', max_length=255, blank=True, null=True)  # Field name made lowercase.
    perguntaid = models.ForeignKey('Pergunta', models.DO_NOTHING, db_column='PerguntaID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'opcoes'


class Pergunta(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    titulo = models.CharField(db_column='Titulo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    formularioid = models.ForeignKey(Formulario, models.DO_NOTHING,
                                     db_column='FormularioID', null=True)  # Field name made lowercase.
    tipo_de_perguntaid = models.ForeignKey('TipoDePergunta', models.DO_NOTHING,
                                           db_column='Tipo de PerguntaID')  # Field name made lowercase. Field renamed to remove unsuitable characters.

    def __str__(self):
        return self.titulo

    class Meta:
        managed = True
        db_table = 'pergunta'


class PeriodoEquipamento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    dia_inicial = models.DateField(db_column='Dia inicial', blank=True,
                                   null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dia_final = models.DateField(db_column='Dia final', blank=True,
                                 null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    hora_de_inicio = models.TimeField(db_column='Hora de inicio', blank=True,
                                      null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    duracao = models.IntegerField(db_column='Duracao', blank=True, null=True)  # Field name made lowercase.
    equipamentoid = models.ForeignKey(Equipamento, models.DO_NOTHING,
                                      db_column='EquipamentoID')  # Field name made lowercase.
    eventoid = models.ForeignKey(Evento, models.CASCADE, db_column='EventoID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'periodo_equipamento'


class PeriodoSala(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    dia_inicial = models.DateField(db_column='Dia inicial', blank=True,
                                   null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dia_final = models.DateField(db_column='Dia final', blank=True,
                                 null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    hora_de_inicio = models.TimeField(db_column='Hora de inicio', blank=True,
                                      null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    duração = models.IntegerField(db_column='Duração')  # Field name made lowercase.
    salaid = models.ForeignKey('Sala', models.DO_NOTHING, db_column='SalaID')  # Field name made lowercase.
    eventoid = models.ForeignKey(Evento, models.CASCADE, db_column='EventoID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'periodo_sala'


class PeriodoServico(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    dia_inicial = models.DateField(db_column='Dia inicial', blank=True,
                                   null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dia_final = models.DateField(db_column='Dia final', blank=True,
                                 null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    hora_de_inicio = models.TimeField(db_column='Hora de inicio', blank=True,
                                      null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    duracao = models.IntegerField(db_column='Duracao', blank=True, null=True)  # Field name made lowercase.
    servicosid = models.ForeignKey('Servicos', models.DO_NOTHING, db_column='ServicosID')  # Field name made lowercase.
    eventoid = models.ForeignKey(Evento, models.CASCADE, db_column='EventoID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'periodo_servico'


class Respostas(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    perguntaid = models.ForeignKey(Pergunta, models.DO_NOTHING, db_column='PerguntaID')  # Field name made lowercase.
    texto = models.CharField(db_column='Texto', max_length=255, blank=True, null=True)  # Field name made lowercase.
    opcoesid = models.ForeignKey(Opcoes, models.DO_NOTHING, db_column='OpcoesID',
                                 null=True)  # Field name made lowercase.
    eventoid = models.ForeignKey(Evento, models.CASCADE, db_column='EventoID')  # Field name made lowercase.
    inscricaoid = models.ForeignKey(Inscricao, models.DO_NOTHING, db_column='InscricaoID',
                                    null=True)  # Field name made lowercase.

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
    tipo_salaid = models.ForeignKey('TipoSala', models.DO_NOTHING,
                                    db_column='Tipo_SalaID')  # Field name made lowercase.

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


class TipoSala(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.nome

    class Meta:
        managed = True
        db_table = 'tipo de sala'


class Servicos(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255, blank=True, null=True)
    preco_base = models.FloatField(
        db_column='Preco base')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tipo_servicoid = models.ForeignKey('TipoServico', models.DO_NOTHING,
                                       db_column='Tipo_ServicoID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'servicos'


class TipoDeEvento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.nome

    class Meta:
        managed = True
        db_table = 'tipo de evento'


class TipoDeFormulario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'tipo de formulario'

    def __str__(self):
        return self.nome


class TipoDePergunta(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.nome

    class Meta:
        managed = True
        db_table = 'tipo de pergunta'


class TipoEquipamento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        managed = True
        db_table = 'tipo_equipamento'


class TipoServico(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        managed = True
        db_table = 'tipo_servico'


class TiposDeRecursos(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    tipo_de_recurso = models.IntegerField(db_column='Tipo de recurso', blank=True,
                                          null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = True
        db_table = 'tipos de recursos'
