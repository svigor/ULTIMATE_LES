from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from users.models import MyUser, Role

admin.site.register(Role)
admin.site.register(MyUser)
admin.site.unregister(Group)
