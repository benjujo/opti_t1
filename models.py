from gurobipy import *
import numpy as np

def P2(M, J, p):
    people_qty = len(M)
    tasks_qty = len(J)
    
    # Definimos primer modelo
    model = Model("P2")

    # Definimos variables de decisión
    x = np.array(np.zeros(shape=(people_qty,tasks_qty)), dtype=Var)

    for i in range(people_qty):
        for j in range(tasks_qty):
            x[i][j] = model.addVar(vtype="B", name="x{},{}".format(i,j))

    A = model.addVar(vtype="C", lb=0, name="A")

    # Definimos retricciones
    # Una tarea es realizada solo por una persona
    for j in range(tasks_qty):
        model.addConstr(quicksum(x[:,j]) == 1, name="unaPersonaPorTarea{}".format(j))

    # Todos trabajan menos que el máximo
    for i in range(people_qty):
        model.addConstr(quicksum((np.array(p)*x[i,:])) <= A, name="cotaDelMaximo{}".format(i))

    # Definimos la función objetivo
    model.setObjective(A, GRB.MINIMIZE)

    model.Params.TIME_LIMIT = 300
    model.update()
    model.optimize()

    print("Horas de trabajo máximo P2: {}".format(A.X))
    for i in range(people_qty):
        print("{} trabajará un total de {} horas".format(M[i], np.sum(np.array(p)*np.array([v.X for v in x[i,:]]))))

    return model


def P3(M, J, p, a):
    people_qty = len(M)
    tasks_qty = len(J)
    
    # Definimos segundo modelo similar al anterior
    model = Model("P3")

    x = np.array(np.zeros(shape=(people_qty,tasks_qty)), dtype=Var)

    for i in range(people_qty):
        for j in range(tasks_qty):
            x[i][j] = model.addVar(vtype="B", name="x{},{}".format(i,j))

    A = model.addVar(vtype="C", lb=0, name="A")

    for j in range(tasks_qty):
        model.addConstr(quicksum(x[:,j]) == 1, name="unaPersonaPorTarea{}".format(j))

    # Todos trabajan menos que el máximo, considerando ahora a las personas listas
    for i in range(people_qty):
        if a[i]:
            model.addConstr(quicksum((np.array(p)/3*x[i,:])) <= A, name="cotaDelMaximo{}".format(i))
        else:
            model.addConstr(quicksum((np.array(p)*x[i,:])) <= A, name="cotaDelMaximo{}".format(i))

    model.setObjective(A, GRB.MINIMIZE)

    model.Params.TIME_LIMIT = 300
    model.update()
    model.optimize()

    print("Horas de trabajo máximo P3: {}".format(A.X))
    for i in range(people_qty):
        if a[i]:
            print("{} trabajará un total de {} horas".format(M[i], np.sum(np.array(p)/3*np.array([v.X for v in x[i,:]]))))
        else:
            print("{} trabajará un total de {} horas".format(M[i], np.sum(np.array(p)*np.array([v.X for v in x[i,:]]))))

    return model

def P4(M, J, p, a, b):
    people_qty = len(M)
    tasks_qty = len(J)
    
    # Definimos tercer modelo similar al anterior
    model = Model("P4")

    x = np.array(np.zeros(shape=(people_qty,tasks_qty)), dtype=Var)
    for i in range(people_qty):
        for j in range(tasks_qty):
            x[i][j] = model.addVar(vtype="B", name="x{},{}".format(i,j))

    A = model.addVar(vtype="C", lb=0, name="A")

    # Creamos una nueva variable
    z = np.array(np.zeros(people_qty), dtype=Var)
    for i in range(people_qty):
        z[i] = model.addVar(vtype="B", name="z{}".format(i))

    for j in range(tasks_qty):
        model.addConstr(quicksum(x[:,j]) == 1, name="unaPersonaPorTarea{}".format(j))

    for i in range(people_qty):
        if a[i]:
            model.addConstr(quicksum((np.array(p)/3*x[i,:])) <= A, name="cotaDelMaximo{}".format(i))
        else:
            model.addConstr(quicksum((np.array(p)*x[i,:])) <= A, name="cotaDelMaximo{}".format(i))

    # Le agregamos la nueva restricción
    for i in range(people_qty):
        model.addConstr(quicksum(np.array(b)*x[i,:]) >= z[i])
        model.addConstr(2*z[i] >= quicksum(np.array(b)*x[i,:]))
        model.addConstr(quicksum(x[i,:]) <= 2 + tasks_qty*(1-z[i]))

    model.setObjective(A, GRB.MINIMIZE)

    model.Params.TIME_LIMIT = 300
    model.update()
    model.optimize()

    print("Horas de trabajo máximo P4: {}".format(A.X))
    for i in range(people_qty):
        if a[i]:
            print("{} trabajará un total de {} horas con {} tareas".format(M[i], np.sum(np.array(p)/3*np.array([v.X for v in x[i,:]])), np.sum(np.array([v.X for v in x[i,:]]))))
        else:
            print("{} trabajará un total de {} horas con {} tareas".format(M[i], np.sum(np.array(p)*np.array([v.X for v in x[i,:]])), np.sum(np.array([v.X for v in x[i,:]]))))

    return model


def P5(M, J, p, a, b, c):
    people_qty = len(M)
    tasks_qty = len(J)

    C = np.array(np.zeros(shape=(4, people_qty)))
    for i in range(people_qty):
        C[c[i]-1][i] = 1

    
    # Definimos segundo modelo similar al anterior
    model = Model("P5")

    x = np.array(np.zeros(shape=(people_qty,tasks_qty)), dtype=Var)
    t = np.array(np.zeros(shape=(people_qty,tasks_qty)), dtype=Var)
    y = np.array(np.zeros(shape=(4,tasks_qty)), dtype=Var)

    for i in range(people_qty):
        for j in range(tasks_qty):
            x[i][j] = model.addVar(vtype="B", name="x{},{}".format(i,j))
            t[i][j] = model.addVar(vtype="C", lb=0, ub=1, name="t{},{}".format(i,j))
    for k in range(4):
        for j in range(tasks_qty):
            y[k][j] = model.addVar(vtype="B", name="y{},{}".format(k,j))

    A = model.addVar(vtype="C", lb=0, name="A")

    # Restricciones
    '''
    for j in range(tasks_qty):
        for k in range(4):
            #print(quicksum(C[k,:]*t[:,j]))
            model.addConstr(quicksum(C[k,:]*t[:,j]) == 1, name="unGrupoPorTarea{},{}".format(j,k))
    '''
    # Una tarea es realizada solo por un grupo
    for j in range(tasks_qty):
        model.addConstr(quicksum(y[:,j]) == 1)

    # Si la tarea es realizada por un grupo, entonces la realizan todos sus integrantes
    for k in range(4):
        for j in range(tasks_qty):
            model.addConstr(quicksum((C[k,:]*x[:,j])) == 5*y[k][j])
    # La tarea debe ser realizada
    for j in range(tasks_qty):
        model.addConstr(quicksum(t[:,j]) == 1)
    
    # Todos trabajan menos que el máximo, considerando ahora a las personas listas
    for i in range(people_qty):
        if a[i]:
            model.addConstr(quicksum((np.array(p)/3*t[i,:])) <= A, name="cotaDelMaximo{}".format(i))
        else:
            model.addConstr(quicksum((np.array(p)*t[i,:])) <= A, name="cotaDelMaximo{}".format(i))
    # Restricción de relación
    for i in range(people_qty):
        for j in range(tasks_qty):
            model.addConstr(x[i][j] >= t[i][j], name="restrRelac{},{}".format(i,j))

    model.setObjective(A, GRB.MINIMIZE)

    model.Params.TIME_LIMIT = 300
    model.update()
    model.optimize()

    print("Horas de trabajo máximo P5: {}".format(A.X))
    for i in range(people_qty):
        if a[i]:
            print("{} trabajará un total de {} horas".format(M[i], np.sum(np.array(p)/3*np.array([v.X for v in t[i,:]]))))
        else:
            print("{} trabajará un total de {} horas".format(M[i], np.sum(np.array(p)*np.array([v.X for v in t[i,:]]))))

    return model
