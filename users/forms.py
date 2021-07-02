from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .models import MyUser, Role


class registerForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='*', widget=forms.EmailInput(attrs={'class': 'input'}))
    NomeProprio = forms.CharField(label='Nome Próprio', help_text='*', max_length=255,
                                  widget=forms.TextInput(attrs={'class': 'input'}))
    SecondName = forms.CharField(label='Apelido', help_text='*', max_length=255,
                                 widget=forms.TextInput(attrs={'class': 'input'}))
    date_of_birth = forms.CharField(label='Data de Nascimento', help_text='*',
                                    widget=forms.TextInput(attrs={'class': 'input'}))
    n_telefone = forms.IntegerField(label='Numero de Telemovel', help_text='*',
                                    widget=forms.NumberInput(attrs={'class': 'input'}))
    interno = forms.BooleanField(label='Interno', required=False, widget=forms.CheckboxInput())
    username = forms.CharField(label='Username', help_text='*', max_length=255,
                               widget=forms.TextInput(attrs={'class': 'input'}))
    password1 = forms.CharField(max_length=255, label='Password', help_text='*',
                                widget=forms.PasswordInput(attrs={'class': 'input'}))
    password2 = forms.CharField(max_length=255, label='Password Confirmation', help_text='*',
                                widget=forms.PasswordInput(attrs={'class': 'input'}))

    class Meta:
        model = MyUser
        fields = (
            'email', 'NomeProprio', 'SecondName', 'date_of_birth', 'n_telefone', 'interno', 'username', 'password1',
            'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user = MyUser.objects.get(email=email)
            if user is not None:
                raise ValidationError('Email já existente')
        except ObjectDoesNotExist:
            return email

    def set_role(self):
        role = Role.objects.get(pk=1)
        return role

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = MyUser.objects.get(username=self.cleaned_data.get(('username')))
            if user is not None:
                raise ValidationError('Username já existente')
        except ObjectDoesNotExist:
            return username

    def clean_n_telefone(self):
        n_telefone = self.cleaned_data.get('n_telefone')
        try:
            user = MyUser.objects.get(n_telefone=n_telefone)
            if user is not None:
                raise ValidationError('A username if that already had already that cellphone number')
        except ObjectDoesNotExist:
            return n_telefone


class loginForm(forms.ModelForm):
    email = forms.EmailField(max_length=255, label='Email', help_text='*',
                             widget=forms.EmailInput(attrs={'class': 'input'}))
    password1 = forms.CharField(max_length=255, help_text='*', label='Password',
                                widget=forms.PasswordInput(attrs={'class': 'input'}))

    class Meta:
        model = MyUser
        fields = ('email', 'password1')

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        if not authenticate(email=email,password=password):
            raise ValidationError('Email ou password não estão corretos')

