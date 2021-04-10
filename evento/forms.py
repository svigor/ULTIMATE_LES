from django import forms
from .models import Sala, Edificio

def funcao():
    s = Edificio.objects.all()
    return [(choice.pk,choice.nome) for choice in s] 
    #return [(Edificio.objects(pk=choice.id),choice.nome) for choice in s]


class InserirSalaForm(forms.ModelForm):
    capacidade = forms.IntegerField(label='capacidade',max_value=2000, widget = forms.NumberInput (
        attrs= {'class': 'input'}
    ) )

    fotos = forms.IntegerField(label='fotos',max_value=2000, widget = forms.NumberInput (
        attrs= {'class': 'input'}
    ) )

    nome = forms.CharField(label='nome',max_length=255, widget = forms.TextInput (
        attrs= {'class': 'input'}
    ) )

    mobilidade_reduzida = forms.BooleanField( label='mobilidade_reduzida',required=False, initial=False,
        widget= forms.CheckboxInput(
           attrs= {'class': ''}
        )
    )


    edificioid = forms.ModelChoiceField(
        queryset=Edificio.objects.all(),
        label='edificioid',
        widget= forms.Select(
           attrs= {'class': ''}
        )    
    )


    class Meta:
        model = Sala
        fields = ['capacidade', 'fotos', 'nome', 'mobilidade_reduzida', 'edificioid']

    
