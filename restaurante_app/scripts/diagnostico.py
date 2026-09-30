import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from servicios.restaurante import Restaurante

r = Restaurante()
print('Rutas:')
print(' productos.json ->', r.productos_path)
print(' usuarios.json  ->', r.usuarios_path)

print('\nUsuarios cargados:', len(r.usuarios))
for u in r.usuarios:
    print('-', u)

print('\nProductos cargados:', len(r.productos))
for p in r.productos:
    print('-', p)

print('\nCategorías:', r.obtener_categorias())
