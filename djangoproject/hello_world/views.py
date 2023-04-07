from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def hello(request, user):
    return HttpResponse("<h1>Hello %s</h1>" % user)
