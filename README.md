# Tarea 1 - IN3701 Modelamiento y Optimización

## Cómo ejecutar
Para correr esta tarea se necesita además de gurobipy, las librerías de numpy, matplotlib y faker.
Es posible instalar mediante pip:
```sh
pip install -r requirements.txt
```

Para ejecutar la tarea con una sola instancia, basta con correr el `main.py`:
```sh
python3 main.py
```

Para correr el experimento (Varias instancias) y obtener un lindo gráfico, en `main.py` hay que descomentar la línea que dice `#experimento(5)` y comentar la que dice `main()`.
Cuidado: Una instancia puede demorarse al rededor de los 10 minutos.

## Tabla de valores óptimos por modelo

| Modelo |   Promedio [hr]    | Desv. Estandar [hr] |
|--------|--------------------|---------------------|
|   P2   |        28.0        |  0.6324555320336759 |
|   P3   | 21.466666666666665 |  0.686375342732467  |
|   P4   |        22.6        | 0.38873012632302006 |
|   P5   | 21.187301033058475 |  0.5810824367306066 |

## Tabla de tiempo de ejecución por modelo

| Modelo |     Promedio [s]    |  Desv. Estandar [s] |
|--------|---------------------|---------------------|
|   P2   | 0.06090035438537598 | 0.04689673885232889 |
|   P3   |  0.6413466453552246 |  0.9696129639138895 |
|   P4   |  188.7679304122925  |  136.31151260048068 |
|   P5   |  300.05297927856446 | 0.09120721049937947 |
