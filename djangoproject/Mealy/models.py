from django.db import models

# Create your models here.
class Machine_name_Mealy(models.Model):
    name = models.CharField(max_length=200)
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['name'], name='unique_name_Mealy')
        ]
    def __str__(self):
        return self.name

class Mealy(models.Model):
    name= models.ForeignKey(Machine_name_Mealy, on_delete=models.CASCADE)
    q = models.CharField(max_length=200)
    fq0 = models.CharField(max_length=200)
    fq1 = models.CharField(max_length=200)
    hq = models.CharField(max_length=200)
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['q'], name='unique_name_Mealy_State')
        ]
    def __str__(self):
        return self.q

