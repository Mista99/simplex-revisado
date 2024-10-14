import numpy as np

np.set_printoptions(suppress=True, precision=2) #PARA Llos puntos en las matrices
#imprime el tablero para cualquier matriz ingresadam de cualquier tamaño
def imprimir_tablero(iteracion, Z, A, vars_no_basicas, rhs):
    # Imprimir el tablero de simplex
    print(f"--- Iteración {iteracion} ---")
    encabezado = ['Z'] + vars_no_basicas + ['RHS']
    print(f"{' | '.join(encabezado)}") #reemplaza las coma por |
    print("-" * 50)
    
    # Imprimir fila Z, es deicr primera fila de la tabla
    print(f"{Z[0]:7.2f} | " + " | ".join([f"{Z[i]:7.2f}" for i in range(1, len(Z))]) + f" | {rhs[0]:7.2f}")
    
    # Imprimir las filas del resto de la tabla
    for i in range(len(A)): 
        print(f"{rhs[i + 1]:7.2f} | " + " | ".join([f"{A[i][j]:7.2f}" for j in range(len(A[i]))]) + f" | {rhs[i + 1]:7.2f}")

def simplex_revisado_con_tablero(c, A, b):

    iteracion = 0

    n_vars = len(c)
    n_restricciones = len(A)
    
    A = np.hstack([A, np.eye(n_restricciones)]) #une la matriz colocandola al lado derecho, o "apilandola"
    c = np.hstack([c, np.zeros(n_restricciones)])

    print("matriz A + la identidad")
    print(A)
    print("matriz c convertida, vars en z")
    print(c)
    
    # Variables básicas y no básicas
    vars_basicas = [f's{i+1}' for i in range(n_restricciones)] #como esta entre corchetes genera una lista, la lista tiene el atributo f's{i+1}', que seria s1, s2, .. sn
    vars_no_basicas = [f'x{i+1}' for i in range(n_vars)] + vars_basicas
    print("las vars basicas son")
    print(vars_basicas)
    
    # Inicialización de Z (fila de la función objetivo)
    Z = np.hstack([1, -c])
    
    rhs = np.hstack([0, b]) #es el vector columna al final
    print("rhs es")
    print(rhs)
    print("Z es")
    print(Z)
    # Imprimir la primera tabla
    imprimir_tablero(iteracion, Z, A, vars_no_basicas, rhs)
    
    #iteraciones del simplex
    while True:
        # Verificar si hemos alcanzado la solución óptima (todos los coeficientes en Z no negativos)
        if all(Z[1:] >= 0):
            print("\nSolución óptima encontrada")
            break
        
        # Seleccionar la columna pivote (la columna más negativa en Z)
        col_pivote = np.argmin(Z[1:]) + 1 #devuelve el inidice del valor minimo, le sumamos +1 debido al "slice" o recorte que hicimos
        
         #----------- Hacer el pivoteo -----------#
        # Calcular los cocientes para la regla del mínimo ratio
        ratios = []
        for i in range(len(b)):
            if A[i][col_pivote - 1] > 0: #compara todos los terminos de la columna pivote
                ratios.append(rhs[i + 1] / A[i][col_pivote - 1])
            else:
                ratios.append(np.inf)
        
        # Seleccionar la fila pivote (mínimo ratio positivo)
        print("los ratios fueron")
        for fila in ratios:
            print(fila)
        fila_pivote = np.argmin(ratios)
        
        # imprimir el pivoteo
        pivote = A[fila_pivote][col_pivote - 1]
        A[fila_pivote] /= A[fila_pivote][col_pivote - 1]
        rhs[fila_pivote + 1] /= pivote

        rhs_col = rhs.reshape(-1, 1)  # Convertir rhs en una columna con la misma cantidad de filas que A
        print("fila ",fila_pivote, " columna ", col_pivote-1)
        print("Haciendo el pivote: ", pivote)
        rhs_col[fila_pivote+1]=rhs_col[fila_pivote+1]
        tabla = np.hstack([A, rhs_col[1:]])
        print(tabla)
        #----------- Hacer el pivoteo end -----------#
        #-----------  -----------#
        for i in range(len(A)):
            if i != fila_pivote:
                factor = A[i][col_pivote - 1]
                A[i] -= factor * A[fila_pivote]
                rhs[i + 1] -= factor * rhs[fila_pivote + 1]
        
        factor = Z[col_pivote]
        Z[1:] -= factor * A[fila_pivote]  # Solo restar a partir del índice 1
        rhs[0] -= factor * rhs[fila_pivote + 1]
        
        # Actualizar las variables básicas y no básicas
        vars_basicas[fila_pivote] = vars_no_basicas[col_pivote - 1]
        
        # Imprimir el tablero después de esta iteración
        iteracion += 1
        imprimir_tablero(iteracion, Z, A, vars_no_basicas, rhs)
     
    # La solución óptima está en la RHS
    return rhs[1:]

# Ejemplo de uso con más iteraciones
# Maximizar z = 3x1 + 5x2
# Sujeto a:
# 2x1 + 3x2 ≤ 12
# x1 + x2 ≤ 6
# x1 + 2x2 ≤ 8
# x1, x2 ≥ 0

c = np.array([3, 5])  # Coeficientes de la función objetivo
#A es la matriz de coeficientes de las vars de las restricciones
A = np.array([[1, 0],
              [0, 2],
              [3, 2]])  # Matriz de coeficientes de restricciones
b = np.array([4, 12, 18])  # Lados derechos de las restricciones

# Llamada al método simplex revisado
solucion = simplex_revisado_con_tablero(c, A, b)
print("\nSolución final:", solucion)
