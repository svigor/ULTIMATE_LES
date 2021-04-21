from django import forms
from .models import TipoDeEvento, Campus


class opcaoevento(forms.ModelForm):
    nome = forms.ModelChoiceField(
        queryset=TipoDeEvento.objects.all(),
        empty_label='Escolha uma das Soluções:',
        label='',
        widget=forms.Select(
            attrs={'class': 'input'}
        )
    )

    class Meta:
        model = TipoDeEvento
        fields = ['nome']


class r_a_form(forms.Form):
    r_a = forms.CharField(label='', max_length=1500, required=True, min_length=5,
                          widget=forms.Textarea(attrs={'class': 'textarea', 'style': 'resize: none'}))


class r_c_form(forms.Form):
    r_c = forms.CharField(label='', required=True, max_length=255, widget=forms.TextInput(attrs={'class': 'input'}))


class c_s_form(forms.Form):
    choice = Campus.objects.all()
    choii = []
    for choicez in choice:
        choii.append(choicez.nome)
    c_s = forms.CharField(label='', widget=forms.Select(choices=choii))


class n_tel(forms.Form):
    n_tel = forms.IntegerField(label='', min_value=900000000, max_value=999999999, widget=forms.NumberInput(attrs={'class': 'input' }))
