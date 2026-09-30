from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.restaurante import Restaurante

r = Restaurante()
print('Inicial -> productos:', len(r.productos), 'usuarios:', len(r.usuarios))

p = Producto('TEST-P1', 'Producto Test', 'Categoría Test', 99.9)
u = Usuario('TEST-U1', 'Usuario Test', 'test@example.com')

ok_p = r.registrar_producto(p)
ok_u = r.registrar_usuario(u)
print('Registro producto ok:', ok_p)
print('Registro usuario ok:', ok_u)

print('\nProductos en memoria:')
for prod in r.productos:
    print('-', prod)

print('\nUsuarios en memoria:')
for usr in r.usuarios:
    print('-', usr)

print('\nContenido productos.json:')
print(r.productos_path.read_text(encoding='utf-8'))
print('\nContenido usuarios.json:')
print(r.usuarios_path.read_text(encoding='utf-8'))
