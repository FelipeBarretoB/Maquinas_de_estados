from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("moore/",views.render_Moore),
    path("mealy/",views.render_Mealy),
    path("machine/",views.render_machines)
]
