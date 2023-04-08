from django.urls import path
from . import views

urlpatterns = [
    path("", views.showAllMealy),
    path("<str:name>", views.showMealy)
]
