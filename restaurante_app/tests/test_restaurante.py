from uuid import uuid4

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante import Restaurante


def test_registro_y_busqueda_de_producto():
    restaurante = Restaurante()
    producto = Producto("P001", "Pizza Margarita", "Pizzas", 12000)

    assert restaurante.registrar_producto(producto) is True
    assert restaurante.buscar_producto_por_codigo("P001") == producto
    assert restaurante.registrar_producto(producto) is False


def test_actualizacion_y_eliminacion_de_producto():
    restaurante = Restaurante()
    restaurante.registrar_producto(Producto("P002", "Hamburguesa", "Fast Food", 8500))

    assert restaurante.actualizar_producto("P002", "Hamburguesa Doble", "Fast Food", 9500) is True
    assert restaurante.buscar_producto_por_codigo("P002").nombre == "Hamburguesa Doble"
    assert restaurante.eliminar_producto("P002") is True
    assert restaurante.buscar_producto_por_codigo("P002") is None


def test_registro_y_listado_de_usuarios():
    restaurante = Restaurante()
    identificacion = f"TEST-{uuid4().hex}"
    usuario = Usuario(identificacion, "Ana Gómez", "ana@restaurante.com")

    assert restaurante.registrar_usuario(usuario) is True
    assert usuario in restaurante.listar_usuarios()
    assert restaurante.registrar_usuario(usuario) is False


def test_categorias_unicas():
    restaurante = Restaurante()
    restaurante.registrar_producto(Producto("P010", "Café", "Bebidas", 3000))
    restaurante.registrar_producto(Producto("P011", "Té", "Bebidas", 2500))
    restaurante.registrar_producto(Producto("P012", "Ensalada", "Entradas", 6000))

    assert restaurante.obtener_categorias() == {"Bebidas", "Entradas"}


def test_venta_descuenta_stock_y_rechaza_exceso():
    usuario = Usuario("U-VENTA", "Cliente", "cliente@example.com")
    producto = Producto("P-VENTA", "Jugo", "Bebidas", 5.0, 3)
    restaurante = Restaurante([producto], [usuario])

    assert restaurante.vender_producto("P-VENTA", "U-VENTA", 2) is True
    assert producto.stock == 1
    assert len(restaurante.consultar_ventas_usuario("U-VENTA")) == 1
    assert restaurante.vender_producto("P-VENTA", "U-VENTA", 2) is False
    assert producto.stock == 1
    assert len(restaurante.listar_ventas()) == 1


def test_persistencia_de_tres_colecciones(tmp_path):
    archivo = ArchivoServicio(tmp_path)
    usuario = Usuario("U-JSON", "Cliente", "cliente@example.com")
    producto = Producto("P-JSON", "Sopa", "Entradas", 8.0, 4)
    restaurante = Restaurante([producto], [usuario])

    assert restaurante.vender_producto("P-JSON", "U-JSON", 1) is True
    archivo.guardar_productos(restaurante.listar_productos())
    archivo.guardar_usuarios(restaurante.listar_usuarios())
    archivo.guardar_ventas(restaurante.listar_ventas())

    productos = archivo.cargar_productos()
    usuarios = archivo.cargar_usuarios()
    ventas = archivo.cargar_ventas()
    assert productos[0].stock == 3
    assert usuarios[0] == usuario
    assert ventas[0].producto_codigo == "P-JSON"


def test_indices_se_reconstruyen_y_se_mantienen_sincronizados():
    usuario = Usuario("U-INDICE", "Cliente", "cliente@example.com")
    producto = Producto("P-INDICE", "Cafe", "Bebidas", 3.0, 5)
    venta = Venta("U-INDICE", "P-INDICE", 1)
    restaurante = Restaurante([producto], [usuario], [venta])

    assert restaurante.buscar_producto_por_codigo("P-INDICE") is producto
    assert restaurante.buscar_usuario("U-INDICE") is usuario
    assert restaurante.consultar_ventas_usuario("U-INDICE") == [venta]

    nuevo_producto = Producto("P-NUEVO", "Te", "Bebidas", 2.0, 2)
    nuevo_usuario = Usuario("U-NUEVO", "Otra persona", "otra@example.com")
    assert restaurante.registrar_producto(nuevo_producto) is True
    assert restaurante.registrar_usuario(nuevo_usuario) is True
    assert restaurante.buscar_producto_por_codigo("P-NUEVO") is nuevo_producto
    assert restaurante.buscar_usuario("U-NUEVO") is nuevo_usuario

    assert restaurante.actualizar_producto("P-NUEVO", "Te verde", "Bebidas", 2.5, 4)
    assert restaurante.buscar_producto_por_codigo("P-NUEVO").stock == 4
    assert restaurante.eliminar_producto("P-NUEVO") is True
    assert restaurante.buscar_producto_por_codigo("P-NUEVO") is None
    assert restaurante.eliminar_usuario("U-NUEVO") is True
    assert restaurante.buscar_usuario("U-NUEVO") is None


def test_usuario_con_rol_y_actualizacion_de_rol():
    restaurante = Restaurante()
    usuario = Usuario("U-ROL", "Carlos", "carlos@restaurante.com", "Cliente")

    assert restaurante.registrar_usuario(usuario) is True
    assert restaurante.buscar_usuario("U-ROL").rol == "Cliente"
    assert restaurante.actualizar_usuario("U-ROL", "Carlos", "carlos@restaurante.com", "Empleado") is True
    assert restaurante.buscar_usuario("U-ROL").rol == "Empleado"
    assert usuario.to_dict()["rol"] == "Cliente"
