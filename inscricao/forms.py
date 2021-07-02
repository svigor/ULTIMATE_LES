from django import forms
from evento.models import Inscricao


class InserirInscricao(forms.ModelForm):
    requer_certificado = forms.BooleanField(label='requer_certificado', required=False, initial=False,
                                            widget=forms.CheckboxInput(
                                                attrs={'class': ''}
                                            )
                                            )

    class Meta:
        model = Inscricao
        fields = ['requer_certificado']


class AlterarInscricao(forms.ModelForm):
    presenca = forms.BooleanField(label='presenca', required=False, initial=False,
                                  widget=forms.CheckboxInput(
                                      attrs={'class': ''}
                                  )
                                  )

    class Meta:
        model = Inscricao
        fields = ['presenca']
