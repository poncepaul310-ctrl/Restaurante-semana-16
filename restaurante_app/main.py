import tkinter as tk

from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante import Restaurante
from ui.login_view import LoginView
from ui.main_view import MainView


class AplicacionRestaurante:
    """Aplicación principal con flujo de login y vista principal."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Sistema de restaurante")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

        self.archivo = ArchivoServicio()
        self.restaurante = Restaurante(
            self.archivo.cargar_productos(),
            self.archivo.cargar_usuarios(),
            self.archivo.cargar_ventas(),
        )

        if not any(usuario.rol == "Administrador" for usuario in self.restaurante.listar_usuarios()):
            admin = Usuario("admin", "Administrador", "admin@restaurante.com", "Administrador")
            self.restaurante.registrar_usuario(admin)
            self.archivo.guardar_usuarios(self.restaurante.listar_usuarios())

        self.vista_actual = None
        self.mostrar_login()

    def mostrar_login(self) -> None:
        self._limpiar_vista_actual()
        self.vista_actual = LoginView(self.root, self.restaurante, self.mostrar_main)

    def mostrar_main(self, usuario) -> None:
        self._limpiar_vista_actual()
        self.vista_actual = MainView(self.root, self.restaurante, usuario, self.archivo)

    def _limpiar_vista_actual(self) -> None:
        if self.vista_actual is not None:
            self.vista_actual.frame.destroy()
            self.vista_actual = None


if __name__ == "__main__":
    root = tk.Tk()
    AplicacionRestaurante(root)
    root.mainloop()
