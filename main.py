from models import P2, P3, P4, P5
from faker import Faker
from random import randint, sample, shuffle
import numpy as np
import matplotlib.pyplot as plt

def mean(*a):
    mean = np.mean(np.array(a), axis=0)
    return mean

def std(*a):
    std = np.std(np.array(a), axis=0)
    return std

def main():
    M = [] # Arreglo de personas
    J = [] # Arreglo de tareas
    p = [] # Arreglo de horas por tarea
    a = [] # Arreglo booleano de personas listas
    b = [] # Arreglo booleano de tareas importantes
    c = [] # Arreglo con el índice del grupo para cada persona

    fake = Faker('es_MX')
    for _ in range(20):
        # Nombres falsos para el equipo
        M.append(fake.first_name())
    print("Las personas son:\n{}".format(str(M)))
    for k in range(100):
        # Tareas numeradas desde el 1
        J.append(k+1)
    for _ in range(100):
        # Número de horas de cada tarea
        p.append(randint(1,10))
    sa = sample(range(20), 3)
    a = [False]*20
    for k in sa:
        a[k] = True
        print("{} es una persona lista".format(M[k]))
    sb = sample(range(100), 5)
    b = [0]*100
    for k in sb:
        b[k] = 1
    c = [1]*5 + [2]*5 + [3]*5 + [4]*5
    shuffle(c)

    m1 = P2(M, J, p)
    m2 = P3(M, J, p, a)
    m3 = P4(M, J, p, a, b)
    m4 = P5(M, J, p, a, b, c)

    opti = [0]*4
    time = [0]*4

    opti[0] = m1.ObjVal
    opti[1] = m2.ObjVal
    opti[2] = m3.ObjVal
    opti[3] = m4.ObjVal
    time[0] = m1.Runtime
    time[1] = m2.Runtime
    time[2] = m3.Runtime
    time[3] = m4.Runtime

    return opti,time

def experimento(t):
    optis = []
    times = []
    for v in range(t):
        o,t = main()
        optis.append(o)
        times.append(t)
    print(optis)
    print(times)

    
    plt.figure(1)

    plt.subplot(121)
    plt.errorbar([1,2,3,4],mean(*optis),yerr=std(*optis))
    plt.xlabel('Modelo a optimizar')
    plt.xticks([1,2,3,4],['P2','P3','P4','P5'])
    plt.ylabel('Valor óptimo [hr]')
    plt.title('Valor óptimo por modelo')
    
    plt.subplot(122)
    plt.errorbar([1,2,3,4],mean(*times),yerr=std(*times))
    plt.xlabel('Modelo a optimizar')
    plt.xticks([1,2,3,4],['P2','P3','P4','P5'])
    plt.ylabel('Tiempo de ejecución [s]')
    plt.title('Tiempo de ejecución por modelo')
    
    plt.show()
    

if __name__ == '__main__':
    main()
    #experimento(5)
