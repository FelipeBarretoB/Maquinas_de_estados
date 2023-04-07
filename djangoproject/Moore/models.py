from django.db import models

# Create your models here.
class Moore(models.Model):
    name = models.CharField(max_length=200)
    q = models.CharField(max_length=200)
    fq0 = models.CharField(max_length=200)
    fq1 = models.CharField(max_length=200)
    gq0 = models.CharField(max_length=200)
    gq1 = models.CharField(max_length=200)
