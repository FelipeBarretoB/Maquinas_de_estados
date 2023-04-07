from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Mealy

# Create your views here.
def showMealy(request):
    machines = list(Mealy.objects.values())
    return JsonResponse(machines, safe=False)
