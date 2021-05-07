from django import forms
from .models import TipoDeEvento, Campus, Sala, Edificio, TipoServico, Servicos


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
                self.fields['edificioid'].queryset = Edificio.objects.filter(campusid=campus_id).order_by("nome")
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['edificioid'].queryset = Edificio.objects.filter(campusid=self.instance.edificioid.campusid)


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


class CriarServicoForm(forms.ModelForm):
    nome = forms.CharField(label='Nome',max_length=255, widget=forms.TextInput(
        attrs={'class':'input'}
    ))

    descricao = forms.CharField(label='Descricao',max_length=255, required=False,widget=forms.TextInput(
        attrs={'class':'input'}
    ))

    preco_base = forms.IntegerField(label='Preço', widget= forms.NumberInput(
        attrs={'class':'input'}
    ))

    tipo_de_servico = forms.ModelChoiceField(
        queryset=TipoServico.objects.all(),
        label='Tipo de serviço',
        empty_label='Escolhe um serviço',
        widget = forms.Select(
            attrs= {'class': 'input'}
        )
    )

    class Meta:
        model = Servicos
        fields = ['nome','descricao', 'preco_base', 'tipo_de_servico']