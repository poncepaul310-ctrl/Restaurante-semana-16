import tkinter as tk
from tkinter import messagebox, ttk


class LoginView:
    """Vista de inicio de sesión para el sistema del restaurante."""

    def __init__(self, root: tk.Tk, restaurante, on_login) -> None:
        self.root = root
        self.restaurante = restaurante
        self.on_login = on_login
        self.frame = ttk.Frame(root, padding=24)
        self.frame.pack(fill="both", expand=True)

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        ttk.Label(self.frame, text="Sistema de restaurante", font=("Segoe UI", 18, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 20)
        )

        ttk.Label(self.frame, text="Identificación:").grid(row=1, column=0, sticky="w", pady=6)

        self.identificacion_var = tk.StringVar()
        self.identificacion_entry = ttk.Entry(self.frame, textvariable=self.identificacion_var)
        self.identificacion_entry.grid(row=1, column=1, sticky="ew", pady=6)
        self.identificacion_entry.focus()

        ttk.Button(self.frame, text="Ingresar", command=self._login).grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=(16, 0)
        )

    def _login(self) -> None:
        identificacion = self.identificacion_var.get().strip()
        if not identificacion:
            messagebox.showwarning("Ingreso", "Debe ingresar una identificación.")
            return

        usuario = self.restaurante.buscar_usuario(identificacion)
        if usuario is None:
            messagebox.showerror("Usuario no encontrado", "No existe un usuario con esa identificación.")
            return

        self.frame.destroy()
        self.on_login(usuario)
