from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Mealy
from django.shortcuts import get_list_or_404
from django.forms.models import model_to_dict

# Create your views here.
def showAllMealy(request):
    machines = list(Mealy.objects.values())
    return JsonResponse(machines, safe=False)

def showMealy(request,name):
    specific_Machine=get_list_or_404(Mealy,name=name)
    specific_Machine_dict=[model_to_dict(machine) for machine in specific_Machine]
    return JsonResponse(specific_Machine_dict,safe=False)

