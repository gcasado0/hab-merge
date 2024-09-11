import pandas as pd

#Leo archivo original
usuarios_0 = pd.read_csv('comercios/usuarios_202407251030.csv')
usuarios_0.rename(columns={'usuario': 'username'}, inplace=True)
usuarios_0['username'] = usuarios_0['username'].str.strip()
usuarios_0['nombre'] = usuarios_0['nombre'].str.strip()
usuarios_0['apellido'] = usuarios_0['apellido'].str.strip()
print(usuarios_0.head())

roles_0 = pd.read_csv('usuario_rol/usuarios_roles_202407251033.csv')
roles_0['username'] = roles_0['username'].str.strip()
print(roles_0.head())

# Verificar si la columna 'username' está presente en ambos DataFrames
if 'username' in usuarios_0.columns and 'username' in roles_0.columns:
    unificado = pd.merge(usuarios_0, roles_0, on='username', how='left')
    print("Unificado:")
    print(unificado.head())
    unificado.to_csv("usuario_rol/unificado.csv")

    # Definir las columnas del segundo archivo
    columns_to_concatenate = roles_0.columns.difference(['username'])

    # Agrupar y concatenar
    unificado_agrupado = unificado.groupby('username').agg(lambda x: ' | '.join(x.astype(str)) if x.name in columns_to_concatenate else x.iloc[0]).reset_index()

    # Guardar el resultado
    unificado_agrupado.to_excel("usuario_rol/usuarios_area_roles.xlsx", index=False)


else:
    print("La columna 'username' no se encuentra en uno o ambos DataFrames")

