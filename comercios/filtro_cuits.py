

import pandas as pd
"""
Este script filtra una lista de comercios basada en una lista de CUITs (números de identificación tributaria) y guarda la lista filtrada en un nuevo archivo Excel.

Pasos:
1. Cargar una lista de CUITs desde un archivo Excel.
2. Renombrar la columna 'Cuit Nº' a 'Cuit' en el DataFrame de CUITs.
3. Convertir la columna 'Cuit' a tipo numérico, manejando errores y valores faltantes.
4. Cargar una lista de comercios desde otro archivo Excel.
5. Verificar la existencia de las columnas necesarias en ambos DataFrames.
6. Filtrar el DataFrame de comercios para incluir solo aquellos comercios cuyo 'titular_cuit' esté presente en el DataFrame de CUITs.
7. Guardar el DataFrame de comercios filtrados en un nuevo archivo Excel llamado 'comercios_filtrados.xlsx'.

Rutas de archivos:
- Archivo de CUITs: '/home/gcasado0/proyectos/hab-merge/comercios/AIM_Rosario-ATE.xlsx'
- Archivo de comercios: '/home/gcasado0/proyectos/hab-merge/comercios/consolidado-2024-09-20.xlsx'
- Archivo de salida: 'comercios_filtrados.xlsx'
"""


archivo_cuits = '/home/gcasado0/proyectos/hab-merge/comercios/AIM_Rosario-ATE.xlsx'
df_cuits = pd.read_excel(archivo_cuits, dtype=str)
# renombrar la columna Cuit Nº por Cuit
df_cuits.rename(columns={'Cuit Nº': 'Cuit'}, inplace=True)
df_cuits['Cuit'] = pd.to_numeric(df_cuits['Cuit'], errors='coerce').fillna(0).astype(int)
print(df_cuits.head())
print(df_cuits.info())

archivo_comercios = '/home/gcasado0/proyectos/hab-merge/comercios/consolidado-2024-09-20.xlsx'
df_comercios = pd.read_excel(archivo_comercios)
print(df_comercios.head())
print(df_comercios.info())


# Verificar si las columnas necesarias existen en los DataFrames
if 'Cuit' not in df_cuits.columns:
    raise ValueError("La columna 'Cuit' no se encuentra en el archivo de CUITs.")
if 'titular_cuit' not in df_comercios.columns:
    raise ValueError("La columna 'titular_cuit' no se encuentra en el archivo de comercios.")

# filtrar los comercios que titular_cuit esté en df_cuits en la columna: Cuit
df_comercios_filtrados = df_comercios[df_comercios['titular_cuit'].isin(df_cuits['Cuit'])]

# Verificar si el DataFrame filtrado está vacío
if df_comercios_filtrados.empty:
    print("No se encontraron comercios con los CUITs proporcionados.")
else:
    # guardar el resultado en archivo excel en el directorio actual con el nombre: comercios_filtrados.xlsx
    df_comercios_filtrados.to_excel("./comercios/comercios_filtrados.xlsx", index=False)
    print("Archivo guardado exitosamente.")

