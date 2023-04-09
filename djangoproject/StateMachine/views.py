from .forms import Create_new_mealy_row
from django.shortcuts import render
from django.forms import formset_factory
from .models import Machine_name_Mealy, Mealy
from .forms import Create_new_mealy_row, mealy_name

# Create your views here.


def index(request):
    return render(request, 'index.html')


def renderMealy(request):
    if request.method == 'POST':
        name = request.POST.get('input-value')
        listq = request.POST.getlist('form-q')
        listfq0 = request.POST.getlist('form-fq0')
        listfq1 = request.POST.getlist('form-fq1')
        listh = request.POST.getlist('form-hq')

        if ((len(listq) != len(set(listq)))):
            raise Exception("No pueden haber estados duplicados")
        for h in listh:
            if h != '0' not in ['0', '1']:
                raise Exception("Solo se permiten las entradas 0 y 1")
        machine = Machine_name_Mealy.objects.create(name=name)
        i = 0
        states = {}
        for q in listq:
            Mealy.objects.create(
                name=machine, q=q, fq0=listfq0[i], fq1=listfq1[i], hq=listh[0])
            i += 1
            states[q] = [listfq0[i], listfq1[i], listh[0]]
        reachable_states = reduce(listq[0],states)
        states = {q: states[q] for q in reachable_states if q in states}
    return render(request, 'mealy.html', )


def reduce(q, states):
    reachable_states = set([q])


# Iterate over states that can be reached from q
    for fq0, fq1, h in [states[q]]:
    # Add reachable states to set
        reachable_states.add(fq0)
        reachable_states.add(fq1)

# Keep adding new reachable states until no new states can be added
    added_new_state=True
    while added_new_state:
        added_new_state = False
        for state in reachable_states.copy():
            for fq0, fq1 in [states[state]]:
                if fq0 not in reachable_states:
                    reachable_states.add(fq0)
                    added_new_state = True
                if fq1 not in reachable_states:
                    reachable_states.add(fq1)
                    added_new_state = True
    return reachable_states

def renderMoore(request):
    return render(request, 'moore.html')
