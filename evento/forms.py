from django import forms
<<<<<<< Updated upstream
from .models import Sala
=======
from .models import Sala, Edificio, TipoDeFormulario, Formulario


>>>>>>> Stashed changes

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

    mobilidade_reduzida = forms.BooleanField( label='mobilidade_reduzida',required=True, initial=False,
        widget= forms.CheckboxInput(
           attrs= {'class': ''}
        )
    )

    
    #edificioid = forms.CharField( label='edificioid',max_length=255,
     #   widget= forms.Select(
      #     attrs= {'class': ''}
       # )
    #)
    

    class Meta:
        model = Sala
        fields = ['capacidade', 'fotos', 'nome', 'mobilidade_reduzida', 'edificioid']

    
class CriarFormulario(forms.ModelForm):
    tipo_de_formulario = forms.ModelChoiceField(
        queryset=TipoDeFormulario.objects.all(),
        label='Tipo de Formulário',
        empty_label='(Selecione um tipo de formulário)',
        widget= forms.Select(
           attrs= {'class': 'input'}
        )    
    )

    class Meta:
        model = Formulario
        fields = ['tipo_de_formulario']
        