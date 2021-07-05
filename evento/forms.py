from django import forms
from django.db.models import query
from django.forms.models import ModelChoiceField
from .models import Pergunta, Sala, Edificio, Campus, TipoDeEvento, TipoDeFormulario, TipoDePergunta



class InserirSalaForm(forms.ModelForm):
    capacidade = forms.IntegerField(label='Capacidade',max_value=2000, widget = forms.NumberInput (
        attrs= {'class': 'input'}
    ) )

    fotos = forms.ImageField(label='Fotos',required=False,
    widget=forms.FileInput()
    ) 

    nome = forms.CharField(label='Nome',max_length=255, widget = forms.TextInput (
        attrs= {'class': 'input'}
    ) )

    mobilidade_reduzida = forms.BooleanField(label='Mobilidade reduzida',required=False, initial=False,
        widget= forms.CheckboxInput(
           attrs= {'class': 'box'}
        )
    )
   
    campus = forms.ModelChoiceField(
        queryset=Campus.objects.all(),
        label='Campus',
        empty_label='Escolhe uma das opções',
        widget= forms.Select(
           attrs= {'class': 'input'}
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
        fields = ['capacidade', 'fotos', 'nome', 'mobilidade_reduzida','campus' ,'edificioid']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['edificioid'].queryset = Edificio.objects.none()
    
        if 'campus' in self.data:
            try:
                campus_id = int(self.data.get('campus'))
                self.fields['edificioid'].queryset = Edificio.objects.all()
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['edificioid'].queryset = Edificio.objects.all()

    


class AlterarSalaForm(forms.ModelForm):
    
    capacidade = forms.IntegerField(label='Capacidade',max_value=2000, widget = forms.NumberInput (
        attrs= {'class': 'input'}
    ) )

    fotos = forms.ImageField(label='Fotos', required=False,
        widget=forms.ClearableFileInput()
    ) 

    nome = forms.CharField(label='Nome',max_length=255, widget = forms.TextInput (
        attrs= {'class': 'input'}
    ) )

    mobilidade_reduzida = forms.BooleanField( label='Mobilidade reduzida',required=False, initial=False,
        widget= forms.CheckboxInput(
           attrs= {'class': 'box'}
        )
    )
   
    campus = forms.ModelChoiceField(
        queryset=Campus.objects.all(),
        label='Campus',
        empty_label='Escolhe uma das opções',
        widget= forms.Select(
           attrs= {'class': 'input'}
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
        fields = ['capacidade', 'fotos', 'nome', 'mobilidade_reduzida','campus' ,'edificioid']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['edificioid'].queryset = Edificio.objects.none()
    
        if 'campus' in self.data:
            try:
                campus_id = int(self.data.get('campus'))
                self.fields['edificioid'].queryset = Edificio.objects.filter(campusid=campus_id).order_by("nome")
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            print("PK",self.instance.pk)
            self.fields['edificioid'].queryset = Edificio.objects.filter(campusid=self.instance.edificioid.campusid)
            
    
    def clean(self):
        capacidade = self.cleaned_data.get('capacidade')
        fotos = self.cleaned_data.get('fotos')
        nome = self.cleaned_data.get('nome')
        mobilidade_reduzida = self.cleaned_data.get('mobilidade_reduzida')
        edificioid = self.cleaned_data.get('edificioid')
        erros = []

        if capacidade == '' or nome == '' or edificioid == None:
            raise forms.ValidationError(f'Todos os campos são o brigatórios!')
        if len(erros) > 0:
            raise ValidationError([erros])

class InscricaoForm(forms.ModelForm):
    requer_certificado = forms.BooleanField( label='Requer certificado?',required=False, initial=False,
        widget= forms.CheckboxInput(
           attrs= {'class': 'box'}
        )
    )


    class Meta:
        model = Sala
        fields = ['requer_certificado']


class CriarFormularioForm(forms.Form):
    tipo_form = forms.ModelChoiceField(
        queryset=TipoDeFormulario.objects.all(), 
        label='Tipo de formulário',
        empty_label='Escolha uma opção',
        widget= forms.Select(
           attrs= {'class': 'input'})
    )
    
    tipo_evento = forms.ModelChoiceField(
        queryset=TipoDeEvento.objects.all(),
        label='Tipo de evento',
        empty_label='Escolha um tipo de evento',
        widget= forms.Select(
           attrs= {'class': 'input'})
    )

    pergunta = forms.ModelChoiceField(
        queryset=Pergunta.objects.filter(formularioid=None),
        label='Primeira pergunta',
        empty_label='Escolha uma pergunta',
        widget= forms.Select(
           attrs= {'class': 'input'})
    )

class AlterarFormularioForm(forms.Form):
    tipo_form = forms.ModelChoiceField(
        queryset=TipoDeFormulario.objects.all(), 
        label='Tipo de formulário',
        empty_label='Escolha uma opção',
        widget= forms.Select(
           attrs= {'class': 'input'})
    )
    
    tipo_evento = forms.ModelChoiceField(
        queryset=TipoDeEvento.objects.all(),
        label='Tipo de evento',
        empty_label='Escolha um tipo de evento',
        widget= forms.Select(
           attrs= {'class': 'input'})
    )

    pergunta = forms.ModelChoiceField(
        queryset=Pergunta.objects.filter(formularioid=None),
        label='Adicionar pergunta',
        empty_label='Escolha uma pergunta',
        widget= forms.Select(
           attrs= {'class': 'input'}),
        required=False
    )

class CriarPerguntaForm(forms.Form):
    titulo = forms.CharField(label="Título", max_length=255, required=True, widget = forms.TextInput (
        attrs= {'class': 'input'}
    ) )
    
    tipo_pergunta = forms.ModelChoiceField(
        queryset=TipoDePergunta.objects.all(),
        label='Tipo de pergunta',
        empty_label='Escolha um tipo de pergunta',
        widget= forms.Select(
           attrs= {'class': 'input'})
    )

    opcao1 = forms.CharField(label="Primeira opção", max_length=128, required=True, widget = forms.TextInput (
        attrs= {'class': 'input'}
    ) )

    opcao2 = forms.CharField(label="Segunda opção", max_length=128, required=True, widget = forms.TextInput (
        attrs= {'class': 'input'}
    ) )

class AlterarPerguntaForm(forms.Form):
    titulo = forms.CharField(label="Título", max_length=255, required=True, widget = forms.TextInput (
        attrs= {'class': 'input'}
    ) )
    
    tipo_pergunta = forms.ModelChoiceField(
        queryset=TipoDePergunta.objects.all(),
        label='Tipo de pergunta',
        empty_label='Escolha um tipo de pergunta',
        widget= forms.Select(
           attrs= {'class': 'input'})
    )

    opcao = forms.CharField(label="Adicionar opção", max_length=128, required=False, widget = forms.TextInput (
        attrs= {'class': 'input'}
    ) )