from models import P2, P3, P4, P5
from faker import Faker
from random import randint, sample

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
