from dataclasses import dataclass


@dataclass
class Usuario:
    """Representa a una persona registrada en el sistema."""

    identificacion: str
    nombre: str
    correo: str
    rol: str = "Cliente"

    def __post_init__(self) -> None:
        self.identificacion = self.identificacion.strip()
        self.nombre = self.nombre.strip()
        self.correo = self.correo.strip()
        self.rol = (self.rol or "Cliente").strip()

        valid_roles = {"Administrador", "Empleado", "Cliente"}
        if not self.identificacion:
            raise ValueError("La identificación del usuario no puede estar vacía.")
        if not self.nombre:
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if not self.correo:
            raise ValueError("El correo del usuario no puede estar vacío.")
        if self.rol not in valid_roles:
            raise ValueError("El rol del usuario debe ser Administrador, Empleado o Cliente.")

    def __str__(self) -> str:
        return f"{self.identificacion} - {self.nombre} - {self.correo} - {self.rol}"

    def to_dict(self) -> dict[str, str]:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "rol": self.rol,
        }

    @classmethod
    def from_dict(cls, datos: dict[str, object]) -> "Usuario":
        return cls(
            identificacion=str(datos["identificacion"]),
            nombre=str(datos["nombre"]),
            correo=str(datos["correo"]),
            rol=str(datos.get("rol", "Cliente")),
        )
