import sympy as sp

# Para imprimir matrices más fácilmente
sp.init_printing()

def calcular_nueva_base(z_lista, E, B, indices_basicas):
    min_E = z_lista.index(min(z_lista))
    print(f"La variable entrante sería x{min_E+1}")
    Xi = E[:, min_E]  # Seleccionar la columna de E en el índice encontrado
    var_sale = f"x{min_E+1}"
    print(f"Columna de x{min_E+1}:")
    sp.pprint(Xi)

    # Dividir los elementos de b por los de columna_E
    resultado_division = []

    for i in range(len(b)):
        if Xi[i] != 0:  # Evitar divisiones por 0
            resultado_division.append(b[i] / Xi[i])
        else:
            resultado_division.append(sp.oo)  # infinito

    print("Resultado de dividir b por columna_E:")
    sp.pprint(resultado_division)
    min_S = resultado_division.index(min(resultado_division))
    print(f"La variable saliente es {v_basicas[min_S]}")
    
    # Actualizar la base
    v_basicas[min_S] = f"x{min_E+1}"
    print("Base:")
    print(v_basicas)

    # Aquí actualizamos la matriz B, reemplazando la columna correspondiente
    B[:, min_S] = Xi
    indices_basicas[min_S] = min_E  # Guardar el índice de la nueva variable básica
    print("Base actualizada:")
    print(v_basicas)
    print("Índices de las variables básicas actualizados:")
    print(indices_basicas)
    
    # Crear un diccionario automáticamente
    diccionario_basicas = {var: idx for var, idx in zip(v_basicas, indices_basicas)}
    print("Diccionario de variables básicas con sus índices:")
    print(diccionario_basicas)
    return diccionario_basicas

def imprimir_tablero(iteracion, Z, E, vars_no_basicas, rhs_total, vars_basicas):
    print(f"--- Iteración {iteracion} ---")
    encabezado = ['Z'] + [f"x{i+1}" for i in range(len(c))] + ['RHS']
    print(f"{' | '.join(f'{h:>7}' for h in encabezado)}")
    print("-" * (9 * (len(encabezado) + 1)))

    print(f"{str(Z[0]):>7} | " + " | ".join([f"{str(Z[i]):>7}" for i in range(1, len(Z))]) + f" | {str(rhs_total[0]):>7}")
    
    for i in range(E.rows):
        fila = f"{vars_basicas[i]:>7} | " + " | ".join([f"{str(E[i, j]):>7}" for j in range(E.cols)]) + f" | {str(rhs_total[i+1]):>7}"
        print(fila)

def simplex_revisado_con_tablero(A, E, b, c, cb, c1, v_basicas):
    iteracion = 0
    n_vars = len(c)
    n_restricciones = A.rows
    B = sp.eye(3)
    indices_basicas = [2, 3, 5]

    print("Matriz A + la identidad")
    sp.pprint(E)
    print("Vector cb es")
    sp.pprint(cb)
    
    v_n_basicas = [f'x{i+1}' for i in range(len(c)) if (c[i] != 0)]
    
    print("Las variables básicas son:")
    print(v_basicas)
    print("Las variables NO básicas son:")
    print(v_n_basicas)
    
    Z = sp.Matrix([1] + [-ci for ci in c])
    print("Vector Z es:")
    sp.pprint(Z.T)

    rhs = sp.Matrix.hstack(sp.Matrix([0]), b.T)
    print("Prueba del rhs")
    print(rhs)

    if len(rhs) < A.rows:
        raise ValueError("El vector RHS tiene un tamaño incorrecto.")
    
    imprimir_tablero(iteracion, Z, E, v_n_basicas, rhs, v_basicas)

    while True:
        M_val = 10000000
        if all(z.is_positive for z in Z[1:]):
            print("\nSolución óptima encontrada")
            break
        B_inv = B.inv()
        print("B inversa es:")
        sp.pprint(B_inv)
        
        k1 = cb.T * B_inv * A - c1.T
        K2 = B_inv * A
        k3 = cb.T * B_inv
        rhs_z = cb.T * B_inv * b
        rhs = B_inv * b

        primera_fila = sp.Matrix.hstack(k1, k3, rhs_z)
        segunda_fila = sp.Matrix.hstack(K2, B_inv, rhs)
        E = segunda_fila
        E_completa = sp.Matrix.vstack(primera_fila, segunda_fila)

        print("La matriz E unida es:")
        sp.pprint(E_completa)

        rhs_total = sp.Matrix.hstack(rhs_z, rhs.T)
        print("rhs total:")
        sp.pprint(rhs_total)

        Z = sp.Matrix.hstack(k1, k3)
        z_numerico = Z.subs(M, M_val)
        z_lista = list(z_numerico)
        print("Lista con M sustituido por un valor grande:", z_lista)

        index_base = calcular_nueva_base(z_lista, E, B, indices_basicas)
        print("Matriz B actualizada:")
        sp.pprint(B)
        
        cb = sp.zeros(len(index_base), 1)
        for i, (variable, indice) in enumerate(index_base.items()):
            cb[i] = Z[indice]

        sp.pprint(cb)

        iteracion += 1
        Z = sp.Matrix([1] + [z for z in Z])
        imprimir_tablero(iteracion, Z, E, v_n_basicas, rhs_total, v_basicas)
    
    return

# Ejemplo de uso
M = sp.symbols('M')
E = sp.Matrix([[2, 1, 1, 0, 0],
                [1, 2, 0, 1, 0],
                [1, 1, 0, 0, 1]])
A = sp.Matrix([[2, 1, 0],
                [1, 2, 0],
                [1, 1, 0]])
b = sp.Matrix([10, 12, 8])  # Lados derechos de las restricciones
cb = sp.Matrix([0, 0, -M])  # Coeficientes de la función objetivo
c = sp.Matrix([3, 2, 0, 0, 0])  # Coeficientes de la función objetivo
c1 = sp.Matrix([3, 2, -M])  # Coeficientes de las variables básicas
v_basicas = ["x3", "x4", "x5"]

# Llamada al método simplex revisado
solucion = simplex_revisado_con_tablero(A, E, b, c, cb, c1, v_basicas)

print("\nSolución final:")
sp.pprint(solucion)
