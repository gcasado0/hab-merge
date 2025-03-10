import pandas as pd


def get_idaccmodapl(nombreaccion, nombremetodo):
    # Consulta a la base de datos para obtener el idaccmodapl
    """
    SELECT id, idaplicacion, idmodapl, descripcion, nombreaccion, nombremetodo, usuario, fechaultmdf, estado
    FROM swe:informix.swe_accmodapl
    WHERE idaplicacion =12;
    """
    acciones = pd.read_csv('permisos/datos/acciones_202503051124_test_swe.csv')
    acciones = acciones[(acciones['nombreaccion'] == nombreaccion) & (acciones['nombremetodo'] == nombremetodo)]
    if len(acciones) == 1:
        return acciones['id'].values[0]
    else:
        return None

# Leer el archivo CSV y seleccionar solo las columnas "nombreaccion" y "nombremetodo"
archivo_rol1='permisos/datos/AdministrativoNivel1_202503101320_prod_swe.csv'
archivo_rol2='permisos/datos/ConsultaNivel3_202503101207_prod_swe.csv'

df1 = pd.read_csv(archivo_rol1, usecols=['nombreaccion', 'nombremetodo'])
df2 = pd.read_csv(archivo_rol2, usecols=['nombreaccion', 'nombremetodo'])

# Eliminar espacios en blanco en los campos
df1 = df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
df2 = df2.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# mostrar registros duplicados
duplicates_df1 = df1[df1.duplicated()]
duplicates_df2 = df2[df2.duplicated()]
if len(duplicates_df1) > 0:
    print('Registros duplicados en df1:')
    print(duplicates_df1)
    print() 
if len(duplicates_df2) > 0:
    print('Registros duplicados en df2:')
    print(duplicates_df2)
    print()

# Merge los DataFrames con indicador
merged_df = df1.merge(df2, on=['nombreaccion', 'nombremetodo'], how='outer', indicator=True)

# Filtrar registros que están solo en df1
#only_in_df1 = merged_df[merged_df['_merge'] == 'left_only']

# Filtrar registros que están solo en df2
#only_in_df2 = merged_df[merged_df['_merge'] == 'right_only']


# Agrupar por 'codigo' y luego por '_merge'
grouped = merged_df.groupby(['_merge'], observed=True)

# borrar archivo sql
with open('permisos/sincronizar.sql', 'w') as f:
    f.write('')    

origen=""
rol_testing = 414
# Mostrar la información agrupada
for (merge_type,), group in grouped:
    if merge_type=='both':
        continue
    if merge_type=='right_only':
        origen='solo en testing'
        print(f"Origen: Solo en {archivo_rol2}")
        print(group[['nombreaccion', 'nombremetodo']])
        # generar sql para eliminar acciones
        for index, row in group.iterrows():
            idaccmodapl = get_idaccmodapl(row['nombreaccion'], row['nombremetodo'])
            if idaccmodapl is None:
                print(f"Error: No se encontró el idaccmodapl para la acción {row['nombreaccion']} - {row['nombremetodo']}")
                continue
            sql = f"""DELETE FROM swe:informix.swe_rolaccmodapl
            WHERE idaccmodapl = {idaccmodapl} AND idrolapl = {rol_testing};"""
            # print(sql)
            # guardar en archivo sql
            with open('permisos/sincronizar.sql', 'a') as f:
                f.write(sql)
                f.write('\n')            

    if merge_type=='left_only':
        origen='solo en produccion'     
        # generar sql para insertar nuevas acciones
        print(f"Origen: Solo en {archivo_rol1}")    
        print(group[['nombreaccion', 'nombremetodo']])
        for index, row in group.iterrows():
            idaccmodapl = get_idaccmodapl(row['nombreaccion'], row['nombremetodo'])
            if idaccmodapl is None:
                print(f"Error: No se encontró el idaccmodapl para la acción {row['nombreaccion']} - {row['nombremetodo']}")
                continue
            sql = f"""INSERT INTO swe:informix.swe_rolaccmodapl
            (id, idaccmodapl, idrolapl, usuario, fechaultmdf, estado)
            VALUES (0, {idaccmodapl}, {rol_testing}, 'gcasado0', CURRENT YEAR TO second, 1);"""
            # print(sql)
            # guardar en archivo sql
            with open('permisos/sincronizar.sql', 'a') as f:
                f.write(sql)
                f.write('\n')
            
