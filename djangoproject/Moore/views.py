from django.shortcuts import render
from models import Moore
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404

# Create your views here.
def showMoore(request):
    machines = list(Moore.objects.values())
    return JsonResponse(machines, safe=False)

def showMealy(request,name):
    specificMachine = get_list_or_404(Moore,name=name)
    return JsonResponse(specificMachine)