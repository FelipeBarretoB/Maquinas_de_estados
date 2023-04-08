from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("mealy/",views.renderMealy),
    path("moore/",views.renderMoore)
    #path("<str:name>", views.showMealy),
    #path("", views.showMoore),
    #path("<str:name>", views.showMoore)
]
