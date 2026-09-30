from __future__ import annotations

from pathlib import Path
from typing import Optional

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class Restaurante:
    """Administra las colecciones y reglas de negocio del restaurante."""

    def __init__(
        self,
        productos: list[Producto] | None = None,
        usuarios: list[Usuario] | None = None,
        ventas: list[Venta] | None = None,
    ) -> None:
        self.base_dir = Path(__file__).resolve().parents[1]
        self.productos_path = self.base_dir / "datos" / "productos.json"
        self.usuarios_path = self.base_dir / "datos" / "usuarios.json"
        self.ventas_path = self.base_dir / "datos" / "ventas.json"
        self.productos = productos.copy() if productos is not None else []
        self.usuarios = usuarios.copy() if usuarios is not None else []
        self.ventas = ventas.copy() if ventas is not None else []
        self._productos_por_codigo: dict[str, Producto] = {}
        self._usuarios_por_identificacion: dict[str, Usuario] = {}
        self._ventas_por_usuario: dict[str, list[Venta]] = {}
        self._categorias: set[str] = set()
        self._reconstruir_indices()
        self.opciones_menu: tuple[str, ...] = (
            "0. Diagnóstico",
            "1. Registrar producto",
            "2. Buscar producto",
            "3. Actualizar producto",
            "4. Eliminar producto",
            "5. Listar productos",
            "6. Registrar usuario",
            "7. Listar usuarios",
            "8. Mostrar categorías",
            "9. Vender producto",
            "10. Consultar ventas de usuario",
            "11. Salir",
        )
        self.menu_principal: dict[str, str] = {
            str(indice): opcion.split(". ", 1)[1]
            for indice, opcion in enumerate(self.opciones_menu)
            if indice != 11
        }

    @staticmethod
    def roles_permitidos() -> tuple[str, ...]:
        return ("Administrador", "Empleado", "Cliente")

    def _reconstruir_indices(self) -> None:
        self._productos_por_codigo = {
            producto.codigo: producto for producto in self.productos
        }
        self._usuarios_por_identificacion = {
            usuario.identificacion: usuario for usuario in self.usuarios
        }
        self._ventas_por_usuario = {}
        for venta in self.ventas:
            self._ventas_por_usuario.setdefault(venta.usuario_id, []).append(venta)
        self._categorias = {producto.categoria for producto in self.productos}

    def registrar_producto(self, producto: Producto) -> bool:
        if producto.codigo in self._productos_por_codigo:
            return False
        self.productos.append(producto)
        self._productos_por_codigo[producto.codigo] = producto
        self._categorias.add(producto.categoria)
        return True

    def buscar_producto_por_codigo(self, codigo: str) -> Optional[Producto]:
        return self._productos_por_codigo.get(codigo.strip())

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int | None = None,
    ) -> bool:
        producto = self._productos_por_codigo.get(codigo.strip())
        if producto is None:
            return False
        stock_actual = producto.stock if stock is None else stock
        producto_actualizado = Producto(producto.codigo, nombre, categoria, precio, stock_actual)
        self.productos[self.productos.index(producto)] = producto_actualizado
        self._productos_por_codigo[producto.codigo] = producto_actualizado
        self._categorias = {elemento.categoria for elemento in self.productos}
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self._productos_por_codigo.get(codigo.strip())
        if producto is None:
            return False
        self.productos.remove(producto)
        del self._productos_por_codigo[producto.codigo]
        self._categorias = {elemento.categoria for elemento in self.productos}
        return True

    def listar_productos(self) -> list[Producto]:
        return self.productos.copy()

    def registrar_usuario(self, usuario: Usuario) -> bool:
        if usuario.identificacion in self._usuarios_por_identificacion:
            return False
        self.usuarios.append(usuario)
        self._usuarios_por_identificacion[usuario.identificacion] = usuario
        return True

    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        return self._usuarios_por_identificacion.get(identificacion.strip())

    def actualizar_usuario(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        rol: str | None = None,
    ) -> bool:
        usuario = self._usuarios_por_identificacion.get(identificacion.strip())
        if usuario is None:
            return False
        usuario_actualizado = Usuario(
            usuario.identificacion,
            nombre,
            correo,
            (usuario.rol if rol is None else rol.strip()),
        )
        self.usuarios[self.usuarios.index(usuario)] = usuario_actualizado
        self._usuarios_por_identificacion[usuario.identificacion] = usuario_actualizado
        return True

    def eliminar_usuario(self, identificacion: str) -> bool:
        usuario = self._usuarios_por_identificacion.get(identificacion.strip())
        if usuario is None:
            return False
        self.usuarios.remove(usuario)
        del self._usuarios_por_identificacion[usuario.identificacion]
        return True

    def listar_usuarios(self) -> list[Usuario]:
        return self.usuarios.copy()

    def vender_producto(self, codigo_producto: str, identificacion_usuario: str, cantidad: int) -> bool:
        usuario = self._usuarios_por_identificacion.get(identificacion_usuario.strip())
        producto = self._productos_por_codigo.get(codigo_producto.strip())
        if usuario is None or producto is None:
            return False
        if cantidad <= 0 or producto.stock < cantidad:
            return False
        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        producto.vender(cantidad)
        self.ventas.append(venta)
        self._ventas_por_usuario.setdefault(venta.usuario_id, []).append(venta)
        return True

    def consultar_ventas_usuario(self, identificacion_usuario: str) -> list[Venta]:
        return self._ventas_por_usuario.get(identificacion_usuario.strip(), []).copy()

    def listar_ventas(self) -> list[Venta]:
        return self.ventas.copy()

    def obtener_categorias(self) -> set[str]:
        return self._categorias.copy()
