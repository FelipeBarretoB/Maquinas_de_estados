from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Mealy, Moore
from django.shortcuts import get_list_or_404
from django.forms.models import model_to_dict

# Create your views here.
def index(request):
    return render(request, 'index.html')

def renderMealy(request):
    return render(request,'mealy.html')

def renderMoore(request):
    return render(request,'moore.html')



def showAllMealy(request):
    machines = list(Mealy.objects.values())
    return JsonResponse(machines, safe=False)

def showMealy(request,name):
    specific_Machine=get_list_or_404(Mealy,name=name)
    specific_Machine_dict=[model_to_dict(machine) for machine in specific_Machine]
    return JsonResponse(specific_Machine_dict,safe=False)

def showMoore(request):
    machines = list(Moore.objects.values())
    return JsonResponse(machines, safe=False)

def showMealy(request,name):
    specificMachine = get_list_or_404(Moore,name=name)
    return JsonResponse(specificMachine)