import sympy as sp

# Para imprimir matrices más fácilmente
sp.init_printing()

# Imprimir el tablero para cualquier matriz ingresada, de cualquier tamaño
def imprimir_tablero(iteracion, Z, A, vars_no_basicas, rhs, vars_basicas):
    # Imprimir el tablero de simplex
    print(f"--- Iteración {iteracion} ---")
    encabezado = ['Z'] + [f"x{i+1}" for i in range(len(cb))] + ['RHS']
    print(f"{' | '.join(f'{h:>7}' for h in encabezado)}")  # Encabezado con formato
    print("-" * (9 * (len(encabezado) + 1)))  # Línea divisoria ajustada al número de columnas
    
    # Imprimir fila Z (primera fila de la tabla)
    # Convertir a cadena para evitar errores de formato
    print(f"{str(Z[0]):>7} | " + " | ".join([f"{str(Z[i]):>7}" for i in range(1, len(Z))]) + f" | {str(rhs[0]):>7}")
    
    # Imprimir las filas del resto de la tabla
    for i in range(A.rows):  # Usar A.rows para el número de filas de A
        fila = f"{vars_basicas[i]:>7} | " + " | ".join([f"{str(A[i, j]):>7}" for j in range(A.cols)]) + f" | {str(rhs[i]):>7}"
        print(fila)

# Método Simplex Revisado con SymPy
def simplex_revisado_con_tablero(A, b, c, cb):
    iteracion = 0
    n_vars = len(c)
    n_restricciones = A.rows  # Número de restricciones (filas de A)
    
    print("Matriz A + la identidad")
    sp.pprint(A)
    print("Vector c es")
    sp.pprint(c)
    
    # Identificar variables básicas y no básicas
    v_basicas = [f'x{i+1}' for i in range(len(cb)) if cb[i] == 0]
    v_n_basicas = [f'x{i+1}' for i in range(len(cb)) if (cb[i] != 0) or (cb[i] == M)]
    
    print("Las variables básicas son: ")
    print(v_basicas)
    print("Las variables NO básicas son: ")
    print(v_n_basicas)
    
    # Inicialización de Z (fila de la función objetivo)
    Z = sp.Matrix([1] + [-ci for ci in cb])
    print("Vector Z es:")
    sp.pprint(Z)
    
    # Usar b como el vector rhs
    rhs = b

    # Verificar que `rhs` tenga la longitud correcta antes de imprimir
    if len(rhs) < A.rows:
        raise ValueError("El vector RHS tiene un tamaño incorrecto.")
    
    # Imprimir tablero inicial
    imprimir_tablero(iteracion, Z, A, v_n_basicas, rhs, v_basicas)

    #iteraciones del simplex
    while True:
        # Verificar si hemos alcanzado la solución óptima (todos los coeficientes en Z no negativos)
        if all(z >= 0 for z in Z[1:]):
            print("\nSolución óptima encontrada")
            break
        
        

        break
    return

# Ejemplo de uso
M = sp.symbols('M')
A = sp.Matrix([[2, 1, 1, 0, 0, 0],
               [1, 1, 0, 1, 0, 0],
               [1, 2, 0, 0, -1, 1]])
b = sp.Matrix([20, 18, 12])  # Lados derechos de las restricciones
c = sp.Matrix([0, 0, -M])  # Coeficientes de la función objetivo
cb = sp.Matrix([5, 4, 0, 0, 0, -M])  # Coeficientes de las variables básicas

# Llamada al método simplex revisado
solucion = simplex_revisado_con_tablero(A, b, c, cb)

print("\nSolución final:")
sp.pprint(solucion)
