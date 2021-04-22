from django import forms
from .models import Sala, Edificio



class InserirSalaForm(forms.ModelForm):
    capacidade = forms.IntegerField(label='Capacidade',max_value=2000, widget = forms.NumberInput (
        attrs= {'class': 'input'}
    ) )

    fotos = forms.ImageField(label='Fotos'
    ) 

    nome = forms.CharField(label='Nome',max_length=255, widget = forms.TextInput (
        attrs= {'class': 'input'}
    ) )

    mobilidade_reduzida = forms.BooleanField( label='Mobilidade reduzida',required=False, initial=False,
        widget= forms.CheckboxInput(
           attrs= {'class': 'box'}
        )
    )
   
    edificioid = forms.ModelChoiceField(
        queryset=Edificio.objects.all(),
        label='Edifício',
        empty_label='Escolhe uma das opções',
        widget= forms.Select(
           attrs= {'class': 'input'}
        )    
    )


    class Meta:
        model = Sala
        fields = ['capacidade', 'fotos', 'nome', 'mobilidade_reduzida', 'edificioid']


class InscricaoForm(forms.ModelForm):
    requer_certificado = forms.BooleanField( label='Requer certificado?',required=False, initial=False,
        widget= forms.CheckboxInput(
           attrs= {'class': 'box'}
        )
    )


    class Meta:
        model = Sala
        fields = ['requer_certificado']



    
