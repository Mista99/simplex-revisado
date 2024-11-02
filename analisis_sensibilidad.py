import numpy as np
from scipy.optimize import linprog
from colorama import Fore, init, Style


def analisis_sensibilidad(c, A, b, res):
    print("\n--- Análisis de Sensibilidad ---")
    print(Fore.GREEN + "Solución óptima: " + Fore.GREEN + np.array2string(res.x) + Style.RESET_ALL)
    print("Valor óptimo de la función objetivo:", -res.fun)  # Negar el valor óptimo para maximización

    # Precios sombra (Dual Prices)
    shadow_prices = res.slack  # Precios sombra
    print("\nPrecios Sombra de las Restricciones:")
    for i, price in enumerate(shadow_prices):
        print(f"Restricción {i + 1}: Precio sombra = {price:.2f}")

    print("\nRango de Sensibilidad para la Función Objetivo:")
    for i in range(len(c)):
        c_temp = c.copy()
        c_temp[i] -= 1  # Aumentar el coeficiente (menos negativo)
        res_temp_high = linprog(c_temp, A_ub=A, b_ub=b, method='highs')

        c_temp[i] += 2  # Disminuir el coeficiente (más negativo)
        res_temp_low = linprog(c_temp, A_ub=A, b_ub=b, method='highs')

        if res_temp_low.success and res_temp_high.success:
            print(f"Coeficiente {i + 1}: {-res_temp_low.fun:.2f} <= z <= {-res_temp_high.fun:.2f}")  # Negar el rango para maximización
        else:
            print(f"Coeficiente {i + 1}: Sin rango definido debido a falta de solución factible.")


