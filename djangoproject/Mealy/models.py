from django.db import models

# Create your models here.


class Mealy(models.Model):
    name = models.CharField(max_length=200)
    q = models.CharField(max_length=200)
    fq0 = models.CharField(max_length=200)
    fq1 = models.CharField(max_length=200)
    hq = models.CharField(max_length=200)
