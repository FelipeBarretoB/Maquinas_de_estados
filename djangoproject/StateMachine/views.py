from django.shortcuts import render
from .models import Machine_name_Moore, Moore, Mealy, Machine_name_Mealy

#INDEX
def index(request):
    return render(request, 'index.html')

#MOORE
def render_Moore(request):
    if request.method == 'POST':
        #almacenamos todos los datos que nos llegan desde el post
        name = request.POST.get('input-value')
        listq = request.POST.getlist('form-q')
        listfq0 = request.POST.getlist('form-fq0')
        listfq1 = request.POST.getlist('form-fq1')
        listh = request.POST.getlist('form-hq')
        
        #manego de excepciones
        if not listq:
            raise Exception("la maquina debe tener por lo menos un estado")

        try:
            machine = Machine_name_Moore.objects.get(name=name)
            raise Exception("Ya existe una maquina con este nombre")
        except Machine_name_Moore.DoesNotExist:
            pass
        if (len(listq) != len(set(listq))):
            raise Exception("No pueden haber estados duplicados")
        for h in listh:
            if h != '0' not in ['0', '1']:
                raise Exception("Solo se permiten las entradas 0 y 1")
        #creamos una maquina nueva solo con el nombre 
        machine = Machine_name_Moore.objects.create(name=name)
        i = 0
        states = {}
        #se crean todos los estados de la maquina de moore
        for q in listq:
            Moore.objects.create(
                name=machine, q=q, fq0=listfq0[i], fq1=listfq1[i], hq=listh[i])
            states[q] = [listfq0[i], listfq1[i], listh[i]]
            i += 1
        #se reduce la maquina
        reachable_states = reduce(listq[0],states)
        #se crea de nuevo el diccionario pero con los estados reducidos
        states = {q: states[q] for q in reachable_states if q in states}
        states=minimize_Moore(states)
        name="mini_"+name
        create_new_Moore(states,name)
        
    return render(request, 'moore.html', )


def reduce(q, states):
    #q se añade a la lista de estados a los que se puede llegar, al ser el estado inicial
    reachable_states = set([q])

    #se añaden al set de estados a que se puede llegar los dos estados de los que se puede llegar desde q
    # '*_' representa n elementos adentro de la lista dentro de la dirección del diccionario states[q]
    for fq0, fq1, *_ in [states[q]]:
        reachable_states.add(fq0)
        reachable_states.add(fq1)

    #Se pone esto como verdadero para que entre al while
    added_new_state=True
    #Se inicial el while donde se repetira hasta que no se añadan más estados
    while added_new_state:
        added_new_state = False
        #se usa una copia de reachable_states por si se añade un nuevo elemento a el original, este nuevo elemento sera visitado en el proximo loop
        #state representa un estado q que se encuentre en rechable_states
        for state in reachable_states.copy():
            #usamos el state como llave en el diccionario original, para ver cuales son sus estados de transición
            for fq0, fq1, *_ in [states[state]]:
                #Verificamos si fq0 o fq1 se encuentran ya en los estados a los cuales podemos llegar
                if fq0 not in reachable_states:
                    reachable_states.add(fq0)
                    added_new_state = True
                if fq1 not in reachable_states:
                    reachable_states.add(fq1)
                    added_new_state = True
    return reachable_states


def minimize_Moore(states):
    # Se crea un partición para los estados de aceptación y no aceptación
    #donde k es un estado, y v[2] es el estado de aceptación 
    accepting = set(k for k, v in states.items() if v[2] == '1')
    non_accepting = set(k for k, v in states.items() if v[2] == '0')
    
    #Se crea la lista de particiones
    partition = [accepting, non_accepting]
    
    #Se inicia un while que funcionara hasta que no se encuentre cambio en las particiones
    while True:
        #Se llama al metodo new_partition con la maquina de estados y las particiones actuales para encontrar una nueva partición
        next_partition=new_partition(
            states,partition
        )
        #Se verifica si hubo algun cambio en las particiones   
        if partition ==next_partition:
            #Como no se encontro ningun cambio se sale del loop
            break
        #como se encontro algun cambio, se asiga la partición nueva a la partición actual
        partition = next_partition
    states=create_mini_Moore(states,partition)
    return states


def new_partition(states, partition):
    #iniciamos la lista de sets
    current_partition=[]
    i=0;
    #recorremos el dictionario que representa la maquina de estados
    for key in states:
        already_in= False
        #miramos si el current key ya esta en alguna partición, si lo esta lo saltamos
        for group in current_partition:
            if key in group:
                already_in=True
        #Si no lo esta, hacemos todos los pares de este con todas las otras keys
        if not already_in:
            current_partition.append(set(key))
            #Conseguimos un segundo contador de llaves para el mismo diccionario
            for key2 in states:
                #Observamos que las llaves no sean igual, de igual manera no deberia importar porque al ser set no se deberia poder repetir elementos
                if key2 != key:
                    #Si ambas pair son verdaderas, significa que en algun grupo de las particiones, fq0 o fq1 estan en el mismo grupo
                    pair1=False
                    pair2 =False
                    #hacemos un recorrido de todas las particiones de la vuelta anterior
                    for group in partition:
                        #Miramos si ambas fq0 estan en el mismo grupo
                        if (states[key][0] in group and states[key2][0] in group):
                            pair1 =True
                        #Miramos si ambas fq1 estan en el mismo grupo
                        if(states[key][1] in group and states[key2][1] in group):
                            pair2 = True
                    #Si lo estan, lo añadimos al set en el que estamos
                    if pair2 and pair1:
                        current_partition[i].add(key2)
            #pasamos a un nuevo set
            i+=1
         
    return current_partition

def create_mini_Moore(states,partitions):
    #Creamos un nuevo diccionario que representara la nueva maquina
    new_machine={}
    #recorremos todos los estados posibles de la maquina original
    for key in states:
        #Instanciamos los valores del estado de la maquina original, dado que, puede que los valores de este estado no cambien
        new_key=key
        new_fq0=states[key][0]
        new_fq1=states[key][1]
        #recorremos todas las particiones finales
        for group in partitions:
            #Creamos este atributo para decidir si ya añadir el estado o no
            change =False
            #''.join(list(group)) representa la union de todos los valores del set: group, es decir, si el group es un set = {'a','b'} el join devolveria la string ab
            #revisamos que el join del grupo no este en la nueva maquina, dado que darle dos llaves iguales a un dictionario puede causar problemas
            if ''.join(list(group)) not in new_machine:
                #revisamos si cualquiera de los estados esta en una partición (group), si lo esta, significa que debemos hacerle el join
                #con cualquiera de los estados me refiero al estado actual y los estados de transición
                if key in group:
                    new_key =''.join(list(group))
                if new_fq0 in group:
                    new_fq0=''.join(list(group))
                if new_fq1 in group:
                    new_fq1=''.join(list(group))
                #añadimos que tenemos un cambio, por ende, hasta ahora se deberia añadir 
                change=True
        #recorremos los estados presentes en la nueva maquina
        for key2 in new_machine:
            #si el nuevo esta ya esta presente (de alguna forma) en la nueva maquina
            if new_key in key2:
                #si ya lo esta, no se deberia añadir
                change=False
        #Se verifica el estado de change, y se añado (o no) el nuevo estado al nuevo diccionario
        if change:                 
            new_machine[new_key]=[new_fq0,new_fq1,states[key][2]]    
        
    return new_machine

def create_new_Moore(states,name):
    #se recorre los nuevos estados
    machine=Machine_name_Moore.objects.create(name=name)
    for key in states:
        #se crean los datos en la base de datos
        Moore.objects.create(name=machine,q=key,fq0=states[key][0],fq1=states[key][1],hq=states[key][2])

#MEALY
def render_Mealy(request):
    if request.method == 'POST':
        #almacenamos todos los datos que nos llegan desde el post
        name = request.POST.get('input-value')
        listq = request.POST.getlist('form-q')
        listfq0 = request.POST.getlist('form-fq0')
        listfq1 = request.POST.getlist('form-fq1')
        listgq0 = request.POST.getlist('form-gq0')
        listgq1 = request.POST.getlist('form-gq1')
        #manego de excepciones
        if not listq:
            raise Exception("la maquina debe tener por lo menos un estado")

        try:
            machine = Machine_name_Moore.objects.get(name=name)
            raise Exception("Ya existe una maquina con este nombre")
        except Machine_name_Moore.DoesNotExist:
            pass
        if (len(listq) != len(set(listq))):
            raise Exception("No pueden haber estados duplicados")
        for h in listgq0:
            if h != '0' not in ['0', '1']:
                raise Exception("Solo se permiten las entradas 0 y 1")
        for h in listgq1:
            if h != '0' not in ['0', '1']:
                raise Exception("Solo se permiten las entradas 0 y 1")

        machine = Machine_name_Mealy.objects.create(name=name)
        states={}
        i=0
        for q in listq:
            Mealy.objects.create(
                name=machine,q=q,fq0=listfq0[i],fq1=listfq1[i],gq0=listgq0[i],gq1=listgq1[i]
            )
            states[q]=[listfq0[i],listfq1[i],listgq0[i],listgq1[i]]
            i+=1
            
        #se reduce la maquina
        reachable_states = reduce(listq[0],states)
        #se crea de nuevo el diccionario pero con los estados reducidos
        states = {q: states[q] for q in reachable_states if q in states}
        states=minimize_Mealy(states)
        
        name="Mini_"+name
        create_new_Mealy(states,name)

    return render(request, 'mealy.html')

def minimize_Mealy(states):
    accepting = set(k for k, v in states.items() if v[2] == '1' and v[3]=='1')
    middle = set(k for k, v in states.items() if (v[2] == '0' and v[3]=='1') or (v[2] == '1' and v[3]=='0'))
    non_accepting= set(k for k, v in states.items() if v[2] == '0' and v[3]=='0')

    partition=[accepting,middle,non_accepting]
     #Se inicia un while que funcionara hasta que no se encuentre cambio en las particiones
    while True:
        #Se llama al metodo new_partition con la maquina de estados y las particiones actuales para encontrar una nueva partición
  
        next_partition=new_partition(
            states,partition
        )
        
        #Se verifica si hubo algun cambio en las particiones   
        if partition ==next_partition:
            
            #Como no se encontro ningun cambio se sale del loop
            break
        #como se encontro algun cambio, se asiga la partición nueva a la partición actual
        partition = next_partition
    return create_mini_Mealy(states,partition)
    
#mismo metodo que en moore, solo cambia la ultima parte gracias a gq0 y gq1, se que se puede optimizar usando solo un metodo, pero no estoy bien de tiempo
def create_mini_Mealy(states,partitions):
    
    new_machine={}
    
    for key in states:
       
        new_key=key
        new_fq0=states[key][0]
        new_fq1=states[key][1]
        
        for group in partitions:
            
            change =False
            
            if ''.join(list(group)) not in new_machine:
                
                if key in group:
                    new_key =''.join(list(group))
                if new_fq0 in group:
                    new_fq0=''.join(list(group))
                if new_fq1 in group:
                    new_fq1=''.join(list(group))
                
                change=True
        
        for key2 in new_machine:
            
            if new_key in key2:
               
                change=False
        
        if change:                 
            new_machine[new_key]=[new_fq0,new_fq1,states[key][2],states[key][3]]    
        
    return new_machine

def create_new_Mealy(states,name):
    #se recorre los nuevos estados
    machine=Machine_name_Mealy.objects.create(name=name)
    for key in states:
        #se crean los datos en la base de datos
        Mealy.objects.create(name=machine,q=key,fq0=states[key][0],fq1=states[key][1],gq0=states[key][2],gq1=states[key][3])

#ver maquinas
def render_machines(request):
    mealy = Mealy.objects.all()
    moore = Moore.objects.all()
    mealy_title= Machine_name_Mealy.objects.all()
    moore_title=Machine_name_Moore.objects.all()
    #Le mandamos los datos que vamos a usar en jinja
    return render(request, 'machines.html',{
        'mealy': mealy, 
        'moore':moore,
        'mealy_title':mealy_title,
        'moore_title':moore_title
        })

