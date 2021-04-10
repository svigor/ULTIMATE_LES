from django import forms
from .models import Sala, Edificio



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
           attrs= {'class': 'box'}
        )
    )
   


    edificioid = forms.ModelChoiceField(
        queryset=Edificio.objects.all(),
        label='edificioid',
        widget= forms.Select(
           attrs= {'class': 'input'}
        )    
    )


    class Meta:
        model = Sala
        fields = ['capacidade', 'fotos', 'nome', 'mobilidade_reduzida', 'edificioid']

    
