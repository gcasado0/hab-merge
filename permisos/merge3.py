import pandas as pd

# Leer el archivo CSV y seleccionar solo las columnas "nombreaccion" y "nombremetodo"

df1 = pd.read_csv('/home/gcasado0/proyectos/hab-utilities/hab-merge/permisos/permisos_prod_swe.csv', usecols=['codigo','nombreaccion', 'nombremetodo'])
df2 = pd.read_csv('/home/gcasado0/proyectos/hab-utilities/hab-merge/permisos/permisos_test_swe.csv', usecols=['codigo','nombreaccion', 'nombremetodo'])

# Eliminar espacios en blanco en los campos
df1 = df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
df2 = df2.apply(lambda x: x.str.strip() if x.dtype == "object" else x)


# Merge los DataFrames con indicador
merged_df = df1.merge(df2, on=['codigo','nombreaccion', 'nombremetodo'], how='outer', indicator=True)

# Filtrar registros que están solo en df1
#only_in_df1 = merged_df[merged_df['_merge'] == 'left_only']

# Filtrar registros que están solo en df2
#only_in_df2 = merged_df[merged_df['_merge'] == 'right_only']


# Agrupar por 'codigo' y luego por '_merge'
grouped = merged_df.groupby(['codigo', '_merge'], observed=True)

# Mostrar la información agrupada
for (codigo, merge_type), group in grouped:
    if merge_type=='both':
        continue
    if merge_type=='right_only':
        origen='solo en testing'
    if merge_type=='left_only':
        origen='solo en produccion'        
    print(f"Rol: {codigo}, Origen: {origen}")
    print(group[['nombreaccion', 'nombremetodo']])
    print()

