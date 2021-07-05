from django import forms
from evento.models import Pergunta, TipoDeEvento, TipoDeFormulario, TipoDePergunta


class CriarFormularioForm(forms.Form):
    tipo_form = forms.ModelChoiceField(
        queryset=TipoDeFormulario.objects.all(),
        label='Tipo de formulário',
        empty_label='Escolha uma opção',
        widget=forms.Select(
            attrs={'class': 'input'})
    )

    tipo_evento = forms.ModelChoiceField(
        queryset=TipoDeEvento.objects.all(),
        label='Tipo de Evento',
        empty_label='Escolha um tipo de Evento',
        widget=forms.Select(
            attrs={'class': 'input'})
    )

    pergunta = forms.ModelChoiceField(
        queryset=Pergunta.objects.filter(formularioid=None),
        label='Primeira pergunta',
        empty_label='Escolha uma pergunta',
        widget=forms.Select(
            attrs={'class': 'input'})
    )


class AlterarFormularioForm(forms.Form):
    tipo_form = forms.ModelChoiceField(
        queryset=TipoDeFormulario.objects.all(),
        label='Tipo de formulário',
        empty_label='Escolha uma opção',
        widget=forms.Select(
            attrs={'class': 'input'})
    )

    tipo_evento = forms.ModelChoiceField(
        queryset=TipoDeEvento.objects.all(),
        label='Tipo de Evento',
        empty_label='Escolha um tipo de Evento',
        widget=forms.Select(
            attrs={'class': 'input'})
    )

    pergunta = forms.ModelChoiceField(
        queryset=Pergunta.objects.filter(formularioid=None),
        label='Adicionar pergunta',
        empty_label='Escolha uma pergunta',
        widget=forms.Select(
            attrs={'class': 'input'}),
        required=False
    )


class CriarPerguntaForm(forms.Form):
    titulo = forms.CharField(label="Título", max_length=255, required=True, widget=forms.TextInput(
        attrs={'class': 'input'}
    ))

    tipo_pergunta = forms.ModelChoiceField(
        queryset=TipoDePergunta.objects.all(),
        label='Tipo de pergunta',
        empty_label='Escolha um tipo de pergunta',
        widget=forms.Select(
            attrs={'class': 'input'})
    )

    opcao1 = forms.CharField(label="Primeira opção", max_length=128, required=True, widget=forms.TextInput(
        attrs={'class': 'input'}
    ))

    opcao2 = forms.CharField(label="Segunda opção", max_length=128, required=True, widget=forms.TextInput(
        attrs={'class': 'input'}
    ))


class AlterarPerguntaForm(forms.Form):
    titulo = forms.CharField(label="Título", max_length=255, required=True, widget=forms.TextInput(
        attrs={'class': 'input'}
    ))

    tipo_pergunta = forms.ModelChoiceField(
        queryset=TipoDePergunta.objects.all(),
        label='Tipo de pergunta',
        empty_label='Escolha um tipo de pergunta',
        widget=forms.Select(
            attrs={'class': 'input'})
    )

    opcao = forms.CharField(label="Adicionar opção", max_length=128, required=False, widget=forms.TextInput(
        attrs={'class': 'input'}
    ))
