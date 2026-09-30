from dataclasses import dataclass


@dataclass
class Venta:
    """Representa una venta entre un usuario y un producto."""

    usuario_id: str
    producto_codigo: str
    cantidad: int

    def __post_init__(self) -> None:
        self.usuario_id = self.usuario_id.strip()
        self.producto_codigo = self.producto_codigo.strip()
        if not self.usuario_id:
            raise ValueError("La identificación del usuario no puede estar vacía.")
        if not self.producto_codigo:
            raise ValueError("El código del producto no puede estar vacío.")
        if not isinstance(self.cantidad, int) or isinstance(self.cantidad, bool) or self.cantidad <= 0:
            raise ValueError("La cantidad vendida debe ser un entero mayor que cero.")

    def to_dict(self) -> dict[str, object]:
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad,
        }

    @classmethod
    def from_dict(cls, datos: dict[str, object]) -> "Venta":
        return cls(
            usuario_id=str(datos["usuario_id"]),
            producto_codigo=str(datos["producto_codigo"]),
            cantidad=int(datos["cantidad"]),
        )

    def __str__(self) -> str:
        return f"Usuario {self.usuario_id} - Producto {self.producto_codigo} - Cantidad: {self.cantidad}"