import tkinter as tk
from tkinter import messagebox
import numpy as np
from scipy.optimize import linprog

# Función que se ejecuta al presionar el botón
def resolver_simplex():
    try:
        # Leer la función objetivo ingresada
        objetivo_str = objetivo_entry.get()
        c = np.array(list(map(float, objetivo_str.split(','))))

        # Leer las restricciones ingresadas
        restricciones_str = restricciones_text.get("1.0", tk.END).strip().split("\n")
        A = []
        b = []
        for restriccion in restricciones_str:
            partes = list(map(float, restriccion.split(',')))
            A.append(partes[:-1])  # Coeficientes de las variables
            b.append(partes[-1])   # Término independiente

        A = np.array(A)
        b = np.array(b)

        # Comprobar si se maximiza o minimiza
        if modo.get() == "Maximizar":
            c = -c  # Convertir a minimización si se selecciona maximizar

        # Resolver usando scipy.optimize.linprog
        res = linprog(c, A_ub=A, b_ub=b, method='highs')

        if res.success:
            resultado = f"Solución óptima: {res.x}\nValor óptimo de la función objetivo: {(-res.fun if modo.get() == 'Maximizar' else res.fun)}"
            messagebox.showinfo("Resultado", resultado)
        else:
            messagebox.showerror("Error", "No se encontró solución óptima.")

    except Exception as e:
        messagebox.showerror("Error", f"Error en la entrada de datos: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Método Simplex Revisado")

# Etiqueta y campo de entrada para la función objetivo
tk.Label(root, text="Función objetivo (separada por comas):").pack(pady=5)
objetivo_entry = tk.Entry(root, width=50)
objetivo_entry.pack(pady=5)

# Etiqueta y campo de entrada para las restricciones
tk.Label(root, text="Restricciones (coeficientes separados por comas, una por línea, último valor es RHS):").pack(pady=5)
restricciones_text = tk.Text(root, height=5, width=50)
restricciones_text.pack(pady=5)

# Botón de opción para seleccionar entre maximizar o minimizar
modo = tk.StringVar(value="Maximizar")
tk.Radiobutton(root, text="Maximizar", variable=modo, value="Maximizar").pack(anchor=tk.W)
tk.Radiobutton(root, text="Minimizar", variable=modo, value="Minimizar").pack(anchor=tk.W)

# Botón para resolver el problema
resolver_button = tk.Button(root, text="Resolver", command=resolver_simplex)
resolver_button.pack(pady=20)

# Iniciar la aplicación
root.mainloop()
