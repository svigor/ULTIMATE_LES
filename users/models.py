from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class Role(models.Model):
    role = models.CharField(max_length=40, verbose_name='Perfil', db_column='Perfil')

    def __str__(self):
        return self.role


class MyUserManager(BaseUserManager):
    def create_user(self, email, NomeProprio, SecondName, date_of_birth, n_telefone, interno, username,
                    password=None):
        if not email:
            raise ValueError('Usuarios têm que ter email')
        role = Role.objects.get(pk=1)
        print(role)
        user = self.model(email=self.normalize_email(email),
                          NomeProprio=NomeProprio,
                          SecondName=SecondName,
                          date_of_birth=date_of_birth,
                          n_telefone=n_telefone,
                          interno=interno,
                          username=username,
                          role=role)
        print(role.id)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, NomeProprio, SecondName, date_of_birth, n_telefone, interno, username,
                         password=None):
        user = self.create_user(email, password=password, n_telefone=n_telefone, NomeProprio=NomeProprio,
                                SecondName=SecondName, date_of_birth=date_of_birth,
                                interno=interno, username=username)
        role = Role.objects.get(pk=3)
        user.role = role
        user.is_admin = True
        user.save(using=self.db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address',
                              max_length=255, unique=True)
    NomeProprio = models.CharField(verbose_name='Primeiro Nome', max_length=255)
    SecondName = models.CharField(verbose_name='Apelido', max_length=255)
    date_of_birth = models.DateField(default='1900-01-01')
    n_telefone = models.IntegerField(verbose_name='numero de telefone', unique=True, default=900000001)
    interno = models.BooleanField(default=False, verbose_name='interno', null=True)
    username = models.CharField(verbose_name='Username', max_length=255, unique=True)
    role = models.ForeignKey(Role, models.DO_NOTHING, db_column='roleid')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['NomeProprio', 'SecondName', 'date_of_birth', 'n_telefone', 'interno', 'username']

    def __str__(self):
        return self.NomeProprio + " " + self.SecondName

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
