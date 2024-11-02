import numpy as np
from colorama import Fore, init
from tabulate import tabulate  # Nueva librería para organizar la tabla

# Inicializar colorama
init(autoreset=True)

np.set_printoptions(suppress=True, precision=2)  # Para los puntos en las matrices

# Imprime el tablero para cualquier matriz ingresada de cualquier tamaño
def colorear_pivotes(iteracion, Z, A, vars_no_basicas, rhs, vars_basicas, i_col_pivote, i_fila_pivote):
    # Imprimir el tablero de simplex con colores
    print(Fore.CYAN + f"--- Iteración {iteracion} ---")
    encabezado = vars_no_basicas + ['RHS']
    
    # Formatear fila Z
    fila_z = ['Z'] + [f"{Z[i]:7.2f}" for i in range(len(Z))] + [f"{rhs[0]:7.2f}"]
    
    # Formatear las filas de las restricciones (variables básicas)
    filas = [
    [vars_basicas[i]] + [0] + 
    [
        f"{A[i][j]:7.2f}" if not (i == i_fila_pivote and j == i_col_pivote) 
        else Fore.YELLOW + f"{A[i][j]:7.2f}" + Fore.RESET for j in range(len(A[i]))
    ] + 
    [f"{rhs[i + 1]:7.2f}"]  # Corregido aquí: Acceder a rhs fuera del bucle for de filas
    for i in range(len(A))]

        
    
    # Crear la tabla usando tabulate
    print(tabulate([fila_z] + filas, headers=encabezado, tablefmt="grid"))
def imprimir_tablero(iteracion, Z, A, vars_no_basicas, rhs, vars_basicas):
    # Imprimir el tablero de simplex con colores
    print(Fore.CYAN + f"--- Iteración {iteracion} ---")
    encabezado = vars_no_basicas + ['RHS']
    
    # Formatear fila Z
    fila_z = ['Z'] + [f"{Z[i]:7.2f}" for i in range(len(Z))] + [f"{rhs[0]:7.2f}"]
    
    # Formatear las filas de las restricciones (variables básicas)
    filas = [[vars_basicas[i]] + [0] + [f"{A[i][j]:7.2f}" for j in range(len(A[i]))] + [f"{rhs[i + 1]:7.2f}"] for i in range(len(A))]
    
    # Crear la tabla usando tabulate
    print(tabulate([fila_z] + filas, headers=encabezado, tablefmt="grid"))

def simplex_revisado_con_tablero(c, A, b):
    iteracion = 0

    n_vars = len(c)
    n_restricciones = len(A)
    
    A = np.hstack([A, np.eye(n_restricciones)])
    c = np.hstack([c, np.zeros(n_restricciones)])

    # Variables básicas y no básicas
    vars_basicas = [f's{i+1}' for i in range(n_restricciones)]
    vars_no_basicas = [f'x{i+1}' for i in range(n_vars)] + vars_basicas
    
    Z = np.hstack([1, -c])
    rhs = np.hstack([0, b])

    # Imprimir la primera tabla
    print("rhs")
    print(rhs)
    print("Z")
    print(Z)
    imprimir_tablero(iteracion, Z, A, vars_no_basicas, rhs, vars_basicas)
    
    while True:
        if all(Z[1:] >= 0):
            print(Fore.GREEN + "\nSolución óptima encontrada")
            break
        
        # Seleccionar la columna pivote
        i_col_pivote = np.argmin(Z[1:]) + 1
        
        # Hacer el pivoteo
        ratios = []
        for i in range(len(b)):
            if A[i][i_col_pivote - 1] > 0:
                ratios.append(rhs[i + 1] / A[i][i_col_pivote - 1])
            else:
                ratios.append(np.inf)
                print("los ratios fueron")
        #imprimir los ratios
        for fila in ratios:
            print(fila)

        i_fila_pivote = np.argmin(ratios)
        print("imprimiendo fila y columna pivote")
        print("col: ", i_col_pivote)
        print("fila: ", i_fila_pivote)
        print("rhs")
        print(rhs)
        colorear_pivotes(iteracion, Z, A, vars_no_basicas, rhs, vars_basicas, i_col_pivote-1, i_fila_pivote)

        # Imprimir pivoteo
        pivote = A[i_fila_pivote][i_col_pivote - 1]
        A[i_fila_pivote] /= pivote
        rhs[i_fila_pivote + 1] /= pivote

        # Reducir por pivoteo
        for i in range(len(A)):
            if i != i_fila_pivote:
                factor = A[i][i_col_pivote - 1]
                A[i] -= factor * A[i_fila_pivote]
                rhs[i + 1] -= factor * rhs[i_fila_pivote + 1]

        # Reducir por pivote la fila Z
        factor = Z[i_col_pivote]
        Z[1:] -= factor * A[i_fila_pivote]
        rhs[0] -= factor * rhs[i_fila_pivote + 1]
        
        # Actualizar variables básicas
        vars_basicas[i_fila_pivote] = vars_no_basicas[i_col_pivote - 1]

        # Imprimir el tablero después de la iteración
        iteracion += 1
        imprimir_tablero(iteracion, Z, A, vars_no_basicas, rhs, vars_basicas)
    
    return rhs[1:]

# Ejemplo de uso con más iteraciones
c = np.array([3, 5])
A = np.array([[1, 0],
              [0, 2],
              [3, 2]])
b = np.array([4, 12, 18])

solucion = simplex_revisado_con_tablero(c, A, b)
print(Fore.GREEN + f"\nSolución final: {solucion}")
