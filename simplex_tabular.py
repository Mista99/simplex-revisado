import numpy as np
from colorama import Fore, init
from tabulate import tabulate  # Librería para organizar la tabla
from scipy.optimize import linprog
import distutils
import analisis_sensibilidad as ans

# Inicializar colorama
init(autoreset=True)

np.set_printoptions(suppress=True, precision=2)  # Para los puntos en las matrices

# Función para imprimir el tablero con color en los pivotes
def colorear_pivotes(iteracion, Z, A, vars_no_basicas, rhs, vars_basicas, i_col_pivote, i_fila_pivote):
    print(Fore.CYAN + f"--- Iteración {iteracion} ---")
    
    # Colorear la columna pivote en el encabezado
    encabezado = [
        Fore.RED + var + Fore.RESET if j == i_col_pivote else var
        for j, var in enumerate(vars_no_basicas + ['RHS'])
    ]
    col_piv_col = i_col_pivote + 1
    # Formatear fila Z, coloreando la columna pivote
    fila_z = ['Z'] + [
        Fore.RED + f"{Z[i]:7.2f}" + Fore.RESET if i == col_piv_col else f"{Z[i]:7.2f}"
        for i in range(len(Z))
    ] + [f"{rhs[0]:7.2f}"]

    # Formatear las filas de las restricciones, coloreando la fila y columna pivote
    filas = [
        [
            vars_basicas[i] + (Fore.RED + " (Fila pivote)" + Fore.RESET if i == i_fila_pivote else ''),
            0
        ] + [
            Fore.YELLOW + f"{A[i][j]:7.2f}" + Fore.RESET if (i == i_fila_pivote or j == i_col_pivote) 
            else f"{A[i][j]:7.2f}" 
            for j in range(len(A[i]))
        ] + [f"{rhs[i + 1]:7.2f}"]
        for i in range(len(A))
    ]
    
    print(tabulate([fila_z] + filas, headers=encabezado, tablefmt="grid"))


def imprimir_tablero(iteracion, Z, A, vars_no_basicas, rhs, vars_basicas):
    print(Fore.CYAN + f"--- Iteración {iteracion} ---")
    encabezado = vars_no_basicas + ['RHS']
    
    fila_z = ['Z'] + [f"{Z[i]:7.2f}" for i in range(len(Z))] + [f"{rhs[0]:7.2f}"]
    filas = [[vars_basicas[i]] + [0] + [f"{A[i][j]:7.2f}" for j in range(len(A[i]))] + [f"{rhs[i + 1]:7.2f}"] for i in range(len(A))]
    

    print(tabulate([fila_z] + filas, headers=encabezado, tablefmt="grid"))

# Función principal del método simplex revisado
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
    imprimir_tablero(iteracion, Z, A, vars_no_basicas, rhs, vars_basicas)
    
    while True:
        if all(Z[1:] >= 0):
            print(Fore.GREEN + "\nSolución óptima encontrada")
            break
        
        # Seleccionar la columna pivote
        i_col_pivote = np.argmin(Z[1:]) + 1
        
        ratios = []
        for i in range(len(b)):
            if A[i][i_col_pivote - 1] > 0:
                ratios.append(rhs[i + 1] / A[i][i_col_pivote - 1])
            else:
                ratios.append(np.inf)
        
        i_fila_pivote = np.argmin(ratios)

        print(Fore.YELLOW + f"\nColumna pivote: {i_col_pivote} (Variable {vars_no_basicas[i_col_pivote - 1]})")
        print(Fore.RED + f"Fila pivote: {i_fila_pivote} (Variable {vars_basicas[i_fila_pivote]})\n")
        
        colorear_pivotes(iteracion, Z, A, vars_no_basicas, rhs, vars_basicas, i_col_pivote-1, i_fila_pivote)

        print(Fore.YELLOW + "----------Realizando pivoteo----------")
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

        iteracion += 1
        colorear_pivotes(iteracion, Z, A, vars_no_basicas, rhs, vars_basicas, i_col_pivote-1, i_fila_pivote)

    return rhs[1:]
def capturar_parametros():
    n = int(input("Ingrese el número de variables de decisión: "))
    c = input(f"Ingrese los coeficientes de la función objetivo (separados por espacios, para {n} variables): ")
    c = np.array([float(coef) for coef in c.split()])
    m = int(input("Ingrese el número de restricciones: "))
    
    # Solicitar las restricciones (matriz A)
    A = []
    for i in range(m):
        restriccion = input(f"Ingrese los coeficientes de la restricción {i+1} (separados por espacios, para {n} variables): ")
        A.append([float(coef) for coef in restriccion.split()])
    A = np.array(A)
    
    b = input(f"Ingrese los valores del lado derecho de las restricciones (separados por espacios, para {m} restricciones): ")
    b = np.array([float(valor) for valor in b.split()])
    
    return c, A, b

def resolver_simplex(c, A, b):
    solucion = simplex_revisado_con_tablero(-1*c, A, b)
    res = linprog(c, A_ub=A, b_ub=b, method='highs')

    if res.success:
        print("Solución óptima:", res.x)
        print("Valor óptimo de la función objetivo:", -res.fun)  # Negar el resultado para maximizar
    else:
        print("No se encontró solución óptima.")
    
    ans.analisis_sensibilidad(c, A, b, res)

c, A, b = capturar_parametros()

resolver_simplex(c, A, b)

# # Parámetros para el problema
# c = np.array([-3, -5])
# A = np.array([[1, 0],   # x1 <= 4
#               [0, 2],   # x2 <= 6
#               [3, 2]])  # 3x1 + 2x2 <= 18
# b = np.array([4, 12, 18])

# solucion = simplex_revisado_con_tablero(-1*c, A, b)

# res = linprog(c, A_ub=A, b_ub=b, method='highs')

# if res.success:
#     print("Solución óptima:", res.x)
#     print("Valor óptimo de la función objetivo:", -res.fun)  # Negar el resultado para maximizar
# else:
#     print("No se encontró solución óptima.")

# ans.analisis_sensibilidad(c, A, b, res)
