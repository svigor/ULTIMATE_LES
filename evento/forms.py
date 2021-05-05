from django import forms
from .models import TipoDeEvento, Campus


class returnedstring():
    def __init__(self, name):
        self.name = name


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


class r_c_form_dis(forms.Form):
    r_c = forms.CharField(label='', required=True, max_length=255,
                          widget=forms.TextInput(
                              attrs={'class': 'input', 'style': 'background: #eef6fc; color: black'}),
                          disabled=True)


class c_s_form(forms.Form):
    dict = []
    campus = Campus.objects.all()
    for choice in campus:
        dict.append(choice)
    c_s = forms.ChoiceField(choices=dict, label='', widget=forms.Select({'class': 'input'}))


class n_tel(forms.Form):
    n_tel = forms.IntegerField(label='',
                               widget=forms.NumberInput(attrs={'class': 'input', 'style': 'background: #eef6fc; '
                                                                                          'color: black'}),
                               disabled=True)
