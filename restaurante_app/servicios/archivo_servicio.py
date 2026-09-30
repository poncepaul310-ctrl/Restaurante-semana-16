from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class ArchivoServicio:
    """Centraliza la lectura y escritura de las colecciones del sistema."""

    def __init__(self, directorio_datos: Path | None = None) -> None:
        base_dir = Path(__file__).resolve().parents[1]
        self.directorio_datos = directorio_datos or base_dir / "datos"
        self.directorio_datos.mkdir(parents=True, exist_ok=True)
        self.ruta_productos = self.directorio_datos / "productos.json"
        self.ruta_usuarios = self.directorio_datos / "usuarios.json"
        self.ruta_ventas = self.directorio_datos / "ventas.json"
        self.ruta_usuarios_anterior = base_dir / "data" / "usuarios.json"

    def _cargar_json(self, ruta: Path) -> list[dict[str, Any]]:
        try:
            with ruta.open("r", encoding="utf-8") as archivo:
                registros = json.load(archivo)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"Advertencia: {ruta.name} no contiene JSON válido. Se iniciará vacío.")
            return []
        except PermissionError:
            print(f"Advertencia: no hay permisos para leer {ruta.name}. Se iniciará vacío.")
            return []

        if isinstance(registros, dict):
            registros = list(registros.values())
        if not isinstance(registros, list):
            print(f"Advertencia: {ruta.name} debe contener una lista de registros.")
            return []
        return [registro for registro in registros if isinstance(registro, dict)]

    def _guardar_json(self, ruta: Path, registros: list[dict[str, Any]]) -> None:
        try:
            with ruta.open("w", encoding="utf-8") as archivo:
                json.dump(registros, archivo, ensure_ascii=False, indent=2)
        except PermissionError as error:
            raise PermissionError(f"No hay permisos para escribir {ruta}.") from error

    def cargar_productos(self) -> list[Producto]:
        productos: list[Producto] = []
        for indice, registro in enumerate(self._cargar_json(self.ruta_productos), start=1):
            try:
                productos.append(Producto.from_dict(registro))
            except (KeyError, TypeError, ValueError) as error:
                print(f"Advertencia: se omitió el producto {indice}: {error}")
        return productos

    def guardar_productos(self, productos: list[Producto]) -> None:
        self._guardar_json(self.ruta_productos, [producto.to_dict() for producto in productos])

    def cargar_usuarios(self) -> list[Usuario]:
        usuarios: list[Usuario] = []
        ruta = self.ruta_usuarios
        if not ruta.exists() and self.ruta_usuarios_anterior.exists():
            ruta = self.ruta_usuarios_anterior
        for indice, registro in enumerate(self._cargar_json(ruta), start=1):
            try:
                usuarios.append(Usuario.from_dict(registro))
            except (KeyError, TypeError, ValueError) as error:
                print(f"Advertencia: se omitió el usuario {indice}: {error}")
        return usuarios

    def guardar_usuarios(self, usuarios: list[Usuario]) -> None:
        self._guardar_json(self.ruta_usuarios, [usuario.to_dict() for usuario in usuarios])

    def cargar_ventas(self) -> list[Venta]:
        ventas: list[Venta] = []
        for indice, registro in enumerate(self._cargar_json(self.ruta_ventas), start=1):
            try:
                ventas.append(Venta.from_dict(registro))
            except (KeyError, TypeError, ValueError) as error:
                print(f"Advertencia: se omitió la venta {indice}: {error}")
        return ventas

    def guardar_ventas(self, ventas: list[Venta]) -> None:
        self._guardar_json(self.ruta_ventas, [venta.to_dict() for venta in ventas])
