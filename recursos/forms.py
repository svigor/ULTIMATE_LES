from django import forms
from evento.models import Campus, Sala, Edificio, TipoSala, TipoServico, Servicos, Equipamento, TipoEquipamento


class InserirSalaForm(forms.ModelForm):
    capacidade = forms.IntegerField(label='Capacidade', max_value=2000, widget=forms.NumberInput(
        attrs={'class': 'input'}
    ))

    fotos = forms.ImageField(label='Fotos', required=False,
                             widget=forms.FileInput(
                                 attrs={'class': ''}
                             ))

    nome = forms.CharField(label='Nome', max_length=255, widget=forms.TextInput(
        attrs={'class': 'input'}
    ))

    mobilidade_reduzida = forms.BooleanField(label='Mobilidade reduzida', required=False, initial=False,
                                             widget=forms.CheckboxInput(
                                                 attrs={'class': 'box'}
                                             )
                                             )

    campus = forms.ModelChoiceField(
        queryset=Campus.objects.all(),
        label='Campus',
        empty_label='Escolhe uma das opções',
        widget=forms.Select(
            attrs={'class': 'input'}
        )
    )

    tipo_salaid = forms.ModelChoiceField(
        queryset=TipoSala.objects.all(),
        label='Tipo de Sala',
        empty_label='Escolhe uma das opções',
        widget=forms.Select(
            attrs={'class': 'input'}
        )
    )

    edificioid = forms.ModelChoiceField(
        queryset=Edificio.objects.all(),
        label='Edifício',
        empty_label='Escolhe uma das opções',
        widget=forms.Select(
            attrs={'class': 'input'}
        )
    )

    class Meta:
        model = Sala
        fields = ['capacidade', 'fotos', 'nome', 'mobilidade_reduzida', 'campus', 'edificioid']

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
    capacidade = forms.IntegerField(label='Capacidade', max_value=2000, widget=forms.NumberInput(
        attrs={'class': 'input'}
    ))

    fotos = forms.ImageField(label='Fotos', required=False,
                             widget=forms.ClearableFileInput()
                             )

    nome = forms.CharField(label='Nome', max_length=255, widget=forms.TextInput(
        attrs={'class': 'input'}
    ))

    mobilidade_reduzida = forms.BooleanField(label='Mobilidade reduzida', required=False, initial=False,
                                             widget=forms.CheckboxInput(
                                                 attrs={'class': 'box'}
                                             )
                                             )

    tipo_salaid = forms.ModelChoiceField(
        queryset=TipoSala.objects.all(),
        label='Tipo de Sala',
        empty_label='Escolhe uma das opções',
        widget=forms.Select(
            attrs={'class': 'input'}
        )
    )

    campus = forms.ModelChoiceField(
        queryset=Campus.objects.all(),
        label='Campus',
        empty_label='Escolhe uma das opções',
        widget=forms.Select(
            attrs={'class': 'input'}
        )
    )

    edificioid = forms.ModelChoiceField(
        queryset=Edificio.objects.all(),
        label='Edifício',
        empty_label='Escolhe uma das opções',
        widget=forms.Select(
            attrs={'class': 'input'}
        )
    )

    class Meta:
        model = Sala
        fields = ['capacidade', 'fotos', 'nome', 'mobilidade_reduzida', 'tipo_salaid', 'campus', 'edificioid']

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
            print("PK", self.instance.pk)
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
    nome = forms.CharField(label='Nome', max_length=255, widget=forms.TextInput(
        attrs={'class': 'input'}
    ))

    descricao = forms.CharField(label='Descricao', max_length=255, required=False, widget=forms.Textarea(
        attrs={'class': 'textarea', 'style': 'resize:none'}
    ))

    preco_base = forms.IntegerField(label='Preço', widget=forms.NumberInput(
        attrs={'class': 'input'}
    ))

    tipo_de_servico = forms.ModelChoiceField(
        queryset=TipoServico.objects.all(),
        label='Tipo de serviço',
        empty_label='Escolhe um serviço',
        widget=forms.Select(
            attrs={'class': 'input'}
        )
    )

    class Meta:
        model = Servicos
        fields = ['nome', 'descricao', 'preco_base', 'tipo_de_servico']


class AlterarServicoForm(forms.ModelForm):
    nome = forms.CharField(label='Nome', max_length=255, widget=forms.TextInput(
        attrs={'class': 'input'}
    ))

    descricao = forms.CharField(label='Descricao', max_length=255, required=False, widget=forms.Textarea(
        attrs={'class': 'textarea', 'style': 'resize:none'}
    ))

    preco_base = forms.IntegerField(label='Preço', widget=forms.NumberInput(
        attrs={'class': 'input'}
    ))

    tipo_de_servico = forms.ModelChoiceField(
        queryset=TipoServico.objects.all(),
        label='Tipo de serviço',
        empty_label='Escolhe um serviço',
        widget=forms.Select(
            attrs={'class': 'input'}
        )
    )

    class Meta:
        model = Servicos
        fields = ['nome', 'descricao', 'preco_base', 'tipo_de_servico']


class CriarEquipamentoForm(forms.ModelForm):
    tipo_equipamentoid = forms.ModelChoiceField(
        queryset=TipoEquipamento.objects.all(),
        label='Tipo de quipamento',
        empty_label='Escolhe um tipo',
        widget=forms.Select(
            attrs={'class': 'input'}
        )
    )

    nome = forms.CharField(label='Nome', max_length=255, required=False, widget=forms.TextInput(
        attrs={'class': 'input'}
    ))

    descricao = forms.CharField(label='Descricao', max_length=255, required=False, widget=forms.Textarea(
        attrs={'class': 'textarea', 'style': 'resize:none'}
    ))

    class Meta:
        model = Equipamento
        fields = ['tipo_equipamentoid', 'nome', 'descricao']


class AlterarEquipamentoForm(forms.ModelForm):
    tipo_equipamentoid = forms.ModelChoiceField(
        queryset=TipoEquipamento.objects.all(),
        label='Tipo de quipamento',
        empty_label=None,
        widget=forms.Select(
            attrs={'class': 'input'}
        )
    )

    nome = forms.CharField(label='Nome', max_length=255, required=False, widget=forms.TextInput(
        attrs={'class': 'input'}
    ))

    descricao = forms.CharField(label='Descricao', max_length=255, required=False, widget=forms.Textarea(
        attrs={'class': 'textarea', 'style': 'resize:none'}
    ))

    class Meta:
        model = Equipamento
        fields = ['tipo_equipamentoid', 'nome', 'descricao']