from django import forms
from .models import Sala, Edificio, TipoDeFormulario, Formulario, Pergunta, TipoDeEvento



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
        widget= forms.Select(
           attrs= {'class': 'input'}
        )    
    )


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

class EscolherTipoDeEvento(forms.ModelForm):
    nome = forms.ModelChoiceField(
        queryset=TipoDeEvento.objects.all(),
        label='Tipo de Evento',
        empty_label='(Selecione um tipo de evento)',
        widget= forms.Select(
           attrs= {'class': 'input'}
        )    
    )

    class Meta:
        model = TipoDeEvento
        fields = ['nome']
        
class EscolherPergunta(forms.ModelForm):
    # nome = forms.ModelT(
    #     label='Pergunta x',
        
    # )

    class Meta:
        model = Pergunta
        fields = ['titulo', 'tipo_de_perguntaid']

