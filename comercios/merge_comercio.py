"""
Este script realiza la consolidación de datos de comercios a partir de un archivo CSV.

Pasos realizados:
1. Registra la fecha y hora de inicio del proceso.
2. Lee un archivo CSV que contiene información sobre comercios y convierte ciertas columnas a tipo numérico.
3. Imprime las primeras filas y la información del DataFrame para verificar la carga de datos.
4. Define las columnas que se van a concatenar, excluyendo la columna 'id'.
5. Agrupa las filas por 'id' y concatena los valores únicos de las columnas seleccionadas, separándolos por ' | '.
6. Guarda el DataFrame consolidado en un archivo Excel.
7. Registra la fecha y hora de finalización del proceso.

Dependencias:
- pandas: Para la manipulación de datos.
- datetime: Para el manejo de fechas y horas.

Uso:
Ejecutar el script en un entorno donde se tenga acceso al archivo CSV especificado y se desee generar un archivo Excel consolidado.
"""
import pandas as pd
from datetime import datetime

# Registrar fecha y hora de inicio
start_time = datetime.now()
print(f"Inicio del proceso: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")


#Leo archivo de comercios
data_0 = pd.read_csv('comercios/comercios_202409111429_prod_comercio.csv', dtype=str)
print(data_0.head())
print(data_0.info())

# Definir las columnas a concatenar
columns_to_concatenate = data_0.columns.difference(['id'])

# Agrupar filas por comercio_id y concatenar los valores de las columnas
consolidado = data_0.groupby('id').agg(lambda x: ' | '.join(pd.Series(x.astype(str).unique()).str.strip()) if x.name in columns_to_concatenate else x.iloc[0]).reset_index()

# Guardar el resultado
consolidado.to_excel("comercios/consolidado.xlsx", index=False)

# Registrar fecha y hora de fin
end_time = datetime.now()
print(f"Fin del proceso: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
