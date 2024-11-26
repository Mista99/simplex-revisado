# Guía para la instalación de librerías y orden de ingreso de inputs

## Instalación de Librerías

Para este proyecto, es necesario instalar las siguientes librerías, las cuales se encuentran en el archivo `requirements.txt`. Puedes instalarlas fácilmente utilizando `pip` ejecutando el siguiente comando en la terminal:

```bash
pip install -r requirements.txt
```
# Ejecutar el proyecto

Para ejecutar el proyecto correctamente debes ir al archivo main.py y ejecutarlo.

# Orden de Ingreso de Inputs

Para el correcto funcionamiento del proyecto, es necesario ingresar los datos en el siguiente orden. A continuación, te presento un ejemplo completo del problema Wyndor, con los inputs organizados para ambos métodos: Simplex Tabular y Gráfico.

## Método Simplex Tabular

1. **Número de variables de decisión**:  
   Ejemplo: `2`

2. **Coeficientes de la función objetivo** (separados por espacios):  
   Ejemplo: `-3 -5`

3. **Número de restricciones**:  
   Ejemplo: `3`

4. **Matriz de coeficientes de las restricciones** (una fila por línea):  
   Ejemplo:  
   ```plaintext
   1 0  
   0 2  
   3 2  
5. **Lado derecho de las restricciones** (valores separados por espacios):
    Ejemplo: 4 12 18

## Método Gráfico

1. **Valor del coeficiente para \(x_1\)** de la función objetivo:  
   Ejemplo: `3`

2. **Valor del coeficiente para \(x_2\)** de la función objetivo:  
   Ejemplo: `5`

3. **Número de restricciones**:  
   Ejemplo: `3`

4. **Restricciones**:

   - **Restricción 1**:  
     Coeficiente de \(x_1\): `1`  
     Coeficiente de \(x_2\): `0`  
     Signo: `<=`  
     Lado derecho: `4`

   - **Restricción 2**:  
     Coeficiente de \(x_1\): `0`  
     Coeficiente de \(x_2\): `2`  
     Signo: `<=`  
     Lado derecho: `12`

   - **Restricción 3**:  
     Coeficiente de \(x_1\): `3`  
     Coeficiente de \(x_2\): `2`  
     Signo: `<=`  
     Lado derecho: `18`

Con estos inputs, puedes ejecutar correctamente el programa para ambos métodos.
