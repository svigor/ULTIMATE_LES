from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField


class MyUserManager(BaseUserManager):
    def create_user(self, email, data_de_nascimento, n_telefone, interno, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            data_de_nascimento=data_de_nascimento,
            n_telefone=n_telefone,
            interno=interno,
            username=username,
        )
        user.set_password(password)
        user.save(using=self)
        return user

    def create_superuser(self, email, data_de_nascimento, n_telefone, interno, username, password=None):
        user = self.create_user(
            email,
            password=password,
            data_de_nascimento=data_de_nascimento,
            n_telefone=n_telefone,
            interno=interno,
            username=username
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address',
                              max_length=255,
                              unique=True)
    data_de_nascimento = models.DateField()
    n_telefone = PhoneNumberField()
    interno = models.BooleanField(verbose_name='Interno', default=False)
    username = models.CharField(max_length=255, verbose_name='username')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['data_de_nascimento', 'n_telefone', 'interno', 'username']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def is_staff(self):
        return self.is_admin


class Roles(models.Model):
    participante = models.BooleanField(verbose_name='Participante', default=True)
    Administrador = models.BooleanField(verbose_name='Administrador', default=False)
    proponente = models.BooleanField(verbose_name='Proponente', default=False)
    userid = models.ForeignKey(MyUser, models.CASCADE)

    def change_proponente(self, value):
        if value != 0 or value != 1:
            raise ValueError('O valor tem que ser entre 0 ou 1')
        self.proponente = value

    def change_administrador(self, value):
        if value != 0 or value != 1:
            raise ValueError('O valor tem que ser entre 0 ou 1')
        self.Administrador = value