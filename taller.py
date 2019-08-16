from gurobipy import *
from faker import Faker
from random import randint, sample
import numpy as np

M = [] # Arreglo de personas
J = [] # Arreglo de tareas
p = [] # Arreglo de horas por tarea
l = [] # Arreglo booleano de personas listas

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
s = sample(range(20), 3)
l = [False]*20
for k in s:
    l[k] = True
    print("{} es una persona lista".format(M[k]))


people_qty = len(M)
tasks_qty = len(J)

# Definimos primer modelo
model1 = Model("P2")

# Definimos variables de decisión
x1 = np.array(np.zeros(shape=(people_qty,tasks_qty)), dtype=Var)

for i in range(people_qty):
    for j in range(tasks_qty):
        x1[i][j] = model1.addVar(vtype="B", name="x{},{}".format(i,j))

A1 = model1.addVar(vtype="C", lb=0, name="A")

# Definimos retricciones
# Una tarea es realizada solo por una persona
for j in range(tasks_qty):
    model1.addConstr(quicksum(x1[:,j]) == 1, name="unaPersonaPorTarea{}".format(j))

# Todos trabajan menos que el máximo
for i in range(people_qty):
    model1.addConstr(quicksum((np.array(p)*x1[i,:])) <= A1, name="cotaDelMaximo{}".format(i))
    
# Definimos la función objetivo
model1.setObjective(A1, GRB.MINIMIZE)

model1.update()
model1.optimize()

print("Horas de trabajo máximo: {}".format(A1.X))
for i in range(people_qty):
    print("{} trabajará un total de {} horas".format(M[i], np.sum(np.array(p)*np.array([v.X for v in x1[i,:]]))))



# Definimos segundo modelo similar al anterior
model2 = Model("P3")

x2 = np.array(np.zeros(shape=(people_qty,tasks_qty)), dtype=Var)

for i in range(people_qty):
    for j in range(tasks_qty):
        x2[i][j] = model2.addVar(vtype="B", name="x{},{}".format(i,j))

A2 = model2.addVar(vtype="C", lb=0, name="A")

for j in range(tasks_qty):
    model2.addConstr(quicksum(x2[:,j]) == 1, name="unaPersonaPorTarea{}".format(j))

# Todos trabajan menos que el máximo, considerando ahora a lxs listxs
for i in range(people_qty):
    if l[i]:
        model2.addConstr(quicksum((np.array(p)/3*x2[i,:])) <= A2, name="cotaDelMaximo{}".format(i))
    else:
        model2.addConstr(quicksum((np.array(p)*x2[i,:])) <= A2, name="cotaDelMaximo{}".format(i))
        
model2.setObjective(A2, GRB.MINIMIZE)

model2.update()
model2.optimize()

print("Horas de trabajo máximo P3: {}".format(A2.X))
for i in range(people_qty):
    if l[i]:
        print("{} trabajará un total de {} horas".format(M[i], np.sum(np.array(p)/3*np.array([v.X for v in x2[i,:]]))))
    else:
        print("{} trabajará un total de {} horas".format(M[i], np.sum(np.array(p)*np.array([v.X for v in x2[i,:]]))))




# Definimos tercer modelo similar al anterior
model3 = Model("P4")

x3 = np.array(np.zeros(shape=(people_qty,tasks_qty)), dtype=Var)

for i in range(people_qty):
    for j in range(tasks_qty):
        x3[i][j] = model3.addVar(vtype="B", name="x{},{}".format(i,j))

A3 = model3.addVar(vtype="C", lb=0, name="A")

for j in range(tasks_qty):
    model3.addConstr(quicksum(x3[:,j]) == 1, name="unaPersonaPorTarea{}".format(j))

for i in range(people_qty):
    if l[i]:
        model3.addConstr(quicksum((np.array(p)/3*x3[i,:])) <= A3, name="cotaDelMaximo{}".format(i))
    else:
        model3.addConstr(quicksum((np.array(p)*x3[i,:])) <= A3, name="cotaDelMaximo{}".format(i))
        
model3.setObjective(A3, GRB.MINIMIZE)

model3.update()
model3.optimize()

print("Horas de trabajo máximo P4: {}".format(A3.X))
for i in range(people_qty):
    if l[i]:
        print("{} trabajará un total de {} horas".format(M[i], np.sum(np.array(p)/3*np.array([v.X for v in x2[i,:]]))))
    else:
        print("{} trabajará un total de {} horas".format(M[i], np.sum(np.array(p)*np.array([v.X for v in x2[i,:]]))))
