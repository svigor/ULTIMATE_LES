from django import forms
from .models import TipoDeEvento, Campus, TipoServico, TipoEquipamento, Periodo_logistica, Inscricao, Formulario, \
    TipoDeFormulario


class opcaoevento(forms.ModelForm):
    nome = forms.ModelChoiceField(
        queryset=TipoDeEvento.objects.all(),
        empty_label='Escolha uma das Soluções:',
        label='',
        widget=forms.Select(attrs={'class': 'input'})
    )

    class Meta:
        model = TipoDeEvento
        fields = ['nome']


class c_s_form(forms.Form):
    dict = []
    campus = Campus.objects.all()
    for choice in campus:
        dict.append(choice)
    c_s = forms.ChoiceField(choices=dict, label='', widget=forms.Select({'class': 'input'}))


class i_s_form(forms.Form):
    dict = []
    tf = TipoDeFormulario.objects.get(nome='Inscrição')
    Fo = Formulario.objects.all().filter(tipo_de_formularioid=tf)
    for choice in Fo:
        dict.append(choice)
    c_s = forms.ChoiceField(choices=dict, label='', widget=forms.Select({'class': 'input'}))


yesnoChoices = (
    ("0", "Seleciona uma opção"),
    ("Sim", "Sim"),
    ("Não", "Não")
)


class LogisticaOpcoesForm_1(forms.Form):
    yesnoSala = forms.ChoiceField(
        choices=yesnoChoices,

        label="Precisa de salas?",
        widget=forms.Select(
            attrs={'class': 'input'}
        )
    )

    yesnoEquipamento = forms.ChoiceField(
        choices=yesnoChoices,
        label="Precisa de equipamentos?",
        widget=forms.Select(
            attrs={'class': 'input'}
        )
    )

    yesnoServico = forms.ChoiceField(
        choices=yesnoChoices,
        label="Precisa de servicos?",
        widget=forms.Select(
            attrs={'class': 'input'}
        )
    )


class LogisticaOpcoesForm_2(forms.Form):
    numeroSalas = forms.IntegerField(label='Quantas salas', required=False, initial=1, widget=forms.NumberInput(
        attrs={'class': 'input'}
    ))

    numeroEquipamentos = forms.IntegerField(label='Quantos equipamentos?', required=False, initial=1,
                                            widget=forms.NumberInput(
                                                attrs={'class': 'input'}
                                            ))

    numeroServicos = forms.IntegerField(label='Quantos serviços?', required=False, initial=1, widget=forms.NumberInput(
        attrs={'class': 'input'}
    ))


class LogisticaQuantitySalas(forms.Form):
    numeroSalas = forms.IntegerField(label='Quantas salas', initial=1, widget=forms.NumberInput(
        attrs={'class': 'input'}
    ))


class LogisticaQuantityEquipamentos(forms.Form):
    numeroEquipamentos = forms.IntegerField(label='Quantos equipamentos?', initial=1, widget=forms.NumberInput(
        attrs={'class': 'input'}
    ))


class LogisticaQuantityServicos(forms.Form):
    numeroServicos = forms.IntegerField(label='Quantos serviços?', initial=1, widget=forms.NumberInput(
        attrs={'class': 'input'}
    ))


class LogisticaOpcoesForm_3(forms.Form):
    dia_inicial = forms.DateField(label='Dia inicial', required=False, widget=forms.DateInput(
        attrs={'class': 'input'}
    ))

    dia_final = forms.DateField(label='Dia final', required=False, widget=forms.DateInput(
        attrs={'class': 'input'}
    ))

    hora_de_inicio = forms.TimeField(label='Hora inicial', required=False, widget=forms.TimeInput(
        attrs={'class': 'input'}
    ))

    hora_de_fim = forms.TimeField(label='Hora final', required=False, widget=forms.TimeInput(
        attrs={'class': 'input'}
    ))

    capacidade = forms.IntegerField(label='Capacidade', max_value=2000, required=False, widget=forms.NumberInput(
        attrs={'class': 'input'}
    ))

    tipo_equipamentoid = forms.ModelChoiceField(
        required=False,
        queryset=TipoEquipamento.objects.all(),
        label='Tipo de quipamento',
        empty_label='Escolhe um tipo',
        widget=forms.Select(
            attrs={'class': 'input'}
        )
    )

    tipo_de_servico = forms.ModelChoiceField(
        required=False,
        queryset=TipoServico.objects.all(),
        label='Tipo de serviço',
        empty_label='Escolhe um serviço',
        widget=forms.Select(
            attrs={'class': 'input'}
        )
    )

    class Meta:
        model = Periodo_logistica
        fields = ['dia_inicial', 'dia_final', 'hora_de_inicio', 'hora_de_fim', 'capacidade', 'tipo_equipamentoid',
                  'tipo_de_servico']


class ValidarLogistica(forms.Form):
    CHOICES = [(1, 'validar'),
               (0, 'nao validar')]
    decision = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
