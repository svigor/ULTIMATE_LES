from django import forms
from users.models import MyUser 
from evento.models import (Inscricao, Evento, Opcoes, Pergunta)



class InserirInscricao(forms.ModelForm):
    requer_certificado = forms.BooleanField( label='requer_certificado',required=False, initial=False,
        widget= forms.CheckboxInput(
           attrs= {'class': ''}
        )
    )

    class Meta:
        model = Inscricao
        fields = ['requer_certificado']


class AlterarInscricao(forms.ModelForm):
    presenca = forms.BooleanField(label='presenca', required=False, initial=False,
        widget= forms.CheckboxInput(
            attrs={'class': ''}
        )
    )

    class Meta:
        model = Inscricao
        fields = ['presenca']

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
    choices = Opcoes.objects.all()
    for choice in choices:
       dict.append(choice)
    c_s = forms.ChoiceField(choices=dict, label='', widget=forms.Select({'class': 'input'}))