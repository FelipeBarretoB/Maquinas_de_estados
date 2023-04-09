from django import forms
class mealy_name(forms.Form):
    name=forms.CharField(max_length=200)

class Create_new_mealy_row(forms.Form):
    name= forms.CharField(max_length=200)
    q = forms.CharField(max_length=200)
    fq0 = forms.CharField(max_length=200)
    fq1 = forms.CharField(max_length=200)
    hq = forms.CharField(max_length=200)