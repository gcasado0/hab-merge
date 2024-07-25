import pandas as pd
import numpy as np

#Leo archivo original
usuarios_0 = pd.read_csv('usuario_area/usuarios.csv')
print(usuarios_0.head())

areas_0 = pd.read_csv('usuarios-area.csv')
areas_0.rename(columns={'usuario': 'username'}, inplace=True)
print(areas_0.head())

unificado = pd.merge(usuarios_0, areas_0, on='username', how='left')
print(unificado.head())

unificado.to_csv("unificado.csv")