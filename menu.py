import simplex_tabular  # Importa el módulo que contiene el código del simplex revisado
import grafico  # Importa el módulo que contendrá el método gráfico

def mostrar_menu():
    print("------------------------------------")
    print("Seleccione el método de resolución:")
    print("1. Método Gráfico")
    print("2. Método Simplex Revisado Tabular")
    print("0. Salir")

def ejecutar_menu():
    while True:
        mostrar_menu()
        opcion = input("Ingrese el número de su elección: ")

        if opcion == '1':
            print("Has seleccionado el Método Gráfico.")
            grafico.metodo_grafico()  # Llama al método gráfico
        elif opcion == '2':
            print("Has seleccionado el Método Simplex Revisado Tabular.")
            c, A, b = simplex_tabular.capturar_parametros()  # Captura los parámetros
            simplex_tabular.resolver_simplex(c, A, b)  # Resuelve usando el método simplex
        elif opcion == '0':
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida, por favor intente nuevamente.")
