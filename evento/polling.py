from .models import Notificacoes
from users.models import MyUser
from django.http import JsonResponse


def getData(request):
    return JsonResponse(Notificacoes.objects.all().filter(recetor=request.user))
