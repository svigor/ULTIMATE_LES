from django import forms
from .models import TipoDeEvento, Campus


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
