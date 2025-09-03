import pandas as pd


def get_idaccmodapl(nombreaccion, nombremetodo):
    # Consulta a la base de datos para obtener el idaccmodapl
    """
    SELECT id, idaplicacion, idmodapl, descripcion, nombreaccion, nombremetodo, usuario, fechaultmdf, estado
    FROM swe:informix.swe_accmodapl
    WHERE idaplicacion =12;
    """
    acciones = pd.read_csv('permisos/datos/acciones_202508291201_test_swe.csv')
    acciones = acciones[(acciones['nombreaccion'] == nombreaccion) & (acciones['nombremetodo'] == nombremetodo)]
    if len(acciones) == 1:
        return acciones['id'].values[0]
    else:
        return None

# Leer el archivo CSV y seleccionar solo las columnas "nombreaccion" y "nombremetodo"

"""select r.id, r.idaccmodapl, r.idrolapl, a.id, a.idaplicacion, a.idmodapl,  ra.codigo, a.nombreaccion, a.nombremetodo,r.usuario
from swe_rolaccmodapl r
join informix.swe_accmodapl a on   a.id = r.idaccmodapl
join swe:informix.swe_rolapl ra on r.idrolapl = ra.id
where ra.idaplicacion = 12
AND r.estado = 1
order by ra.codigo, nombreaccion;"""

archivo_rol_prod='permisos/datos/permisos_202508291206_prod_swe.csv'
archivo_rol_test='permisos/datos/permisos_202508291205_test_swe.csv'

df_prod = pd.read_csv(archivo_rol_prod, usecols=['codigo','nombreaccion', 'nombremetodo'])
df_test = pd.read_csv(archivo_rol_test, usecols=['codigo','nombreaccion', 'nombremetodo'])

# Eliminar espacios en blanco en los campos
df_prod = df_prod.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
df_test = df_test.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# mostrar registros duplicados
duplicates_df_prod = df_prod[df_prod.duplicated()]
duplicates_df_test = df_test[df_test.duplicated()]
if len(duplicates_df_prod) > 0:
    print('Registros duplicados en prod:')
    print(duplicates_df_prod)
    print() 
if len(duplicates_df_test) > 0:
    print('Registros duplicados en test:')
    print(duplicates_df_test)
    print()

# Merge los DataFrames con indicador
merged_df = df_prod.merge(df_test, on=['codigo', 'nombreaccion', 'nombremetodo'], how='outer', indicator=True)

#guardar en excel merge_df
merged_df.to_excel('permisos/datos/merge_df.xlsx', index=False)


# Filtrar registros que están solo en df1
#only_in_df1 = merged_df[merged_df['_merge'] == 'left_only']

# Filtrar registros que están solo en df2
#only_in_df2 = merged_df[merged_df['_merge'] == 'right_only']




