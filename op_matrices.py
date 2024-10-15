import sympy as sp

# Definir el símbolo M
M = sp.symbols('M')

# Definir la matriz A
A = sp.Matrix([[2, 1, 1, 0, 0, 0],
               [1, 1, 0, 1, 0, 0],
               [1, 2, 0, 0, -1, 1]])

# Definir los vectores C, b y C1
C = sp.Matrix([0, 0, -M])
b = sp.Matrix([20, 18, 12])
C1 = sp.Matrix([5, 4, 0, 0, 0, -M])

# Realizar la operación C * A - C1
resultado = C.T * A - C1.T  # Usamos C.T para la transpuesta de C y C1.T para la transpuesta de C1

# Mostrar el resultado
print("Resultado de C * A - C1:")
sp.pprint(resultado)
