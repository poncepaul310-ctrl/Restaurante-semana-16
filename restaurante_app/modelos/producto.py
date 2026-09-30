from dataclasses import dataclass


@dataclass
class Producto:
    """Representa un producto del restaurante."""

    codigo: str
    nombre: str
    categoria: str
    precio: float
    stock: int = 0

    def __post_init__(self) -> None:
        self.codigo = self.codigo.strip()
        self.nombre = self.nombre.strip()
        self.categoria = self.categoria.strip()

        if not self.codigo:
            raise ValueError("El código del producto no puede estar vacío.")
        if not self.nombre:
            raise ValueError("El nombre del producto no puede estar vacío.")
        if not self.categoria:
            raise ValueError("La categoría del producto no puede estar vacía.")
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if not isinstance(self.stock, int) or isinstance(self.stock, bool) or self.stock < 0:
            raise ValueError("El stock debe ser un entero no negativo.")

    def vender(self, cantidad: int) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        if cantidad > self.stock:
            raise ValueError("No hay stock suficiente para realizar la venta.")
        self.stock -= cantidad

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre} ({self.categoria}) - ${self.precio:.2f} - Stock: {self.stock}"

    def to_dict(self) -> dict[str, object]:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock,
        }

    @classmethod
    def from_dict(cls, datos: dict[str, object]) -> "Producto":
        return cls(
            codigo=str(datos["codigo"]),
            nombre=str(datos["nombre"]),
            categoria=str(datos["categoria"]),
            precio=float(datos["precio"]),
            stock=int(datos.get("stock", 0)),
        )
