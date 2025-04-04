import pandas as pd

# Tengo 2 archivos unos con los datos de los roles del usuario extraido de swe y otro con los datos del usuario extraido de ph

"""
SELECT ua.id, username, ra.codigo, ra.descripcion, date(fechaalta) alta, ura.idrolapl
FROM swe:informix.swe_usrapl ua
JOIN swe_usrrolapl ura ON ura.idusrapl= ua.id
JOIN swe_rolapl ra ON ra.id = ura.idrolapl
WHERE ua.idaplicacion =12
AND fechabaja IS NULL
ORDER BY username, codigo;
"""

archivo_roles='usuario_rol/usuarios_ph_202504031354_prod_swe.csv'

"""
SELECT u.id, u.usuario as username, date(u.create_date) alta_ph, u.nombre, u.apellido, u.clase_cod, u.cuit, u.area_id, ua.codigo, ua.titulo
FROM comercio:informix.usr_usuario u
join usr_area ua on ua.id = u.area_id
where u.tipo_usuario_cod ='INTERNO'
and u.activo_hasta is null;
"""

archivo_usuarios='usuario_rol/usuarios_ph_202504041029_prod_Informix_comercio.csv'

# Leo archivo usuarios
usuarios_0 = pd.read_csv(archivo_usuarios)
usuarios_0['username'] = usuarios_0['username'].str.strip()
usuarios_0['nombre'] = usuarios_0['nombre'].str.strip()
usuarios_0['apellido'] = usuarios_0['apellido'].str.strip()
print(usuarios_0.head())


# Leo archivo roles
roles_0 = pd.read_csv(archivo_roles)
roles_0['username'] = roles_0['username'].str.strip()
print(roles_0.head())

# hago un merge por columna username
# Verificar si la columna 'username' está presente en ambos DataFrames
if 'username' in usuarios_0.columns and 'username' in roles_0.columns:
    unificado = pd.merge(usuarios_0, roles_0, on='username', how='outer', indicator=True)
    # ordenar unificado por username
    unificado = unificado.sort_values(by='username')
    print("Unificado:")
    print(unificado.head())

    # Generar timestamp para agregar al nombre del archivo
    timestamp = pd.Timestamp.now().strftime('%Y%m%d%H%M%S')

    # Guardar el resultado
    unificado.to_excel(f"usuario_rol/usuarios_area_roles_{timestamp}.xlsx", index=False)


else:
    print("La columna 'username' no se encuentra en uno o ambos DataFrames")
