import tkinter as tk
from tkinter import messagebox, ttk

from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio


class MainView:
    """Vista principal con información del restaurante y gestión de usuarios."""

    def __init__(self, root: tk.Tk, restaurante, usuario, archivo: ArchivoServicio | None = None) -> None:
        self.root = root
        self.restaurante = restaurante
        self.usuario = usuario
        self.archivo = archivo or ArchivoServicio()
        self.usuario_seleccionado = None

        self.frame = ttk.Frame(root, padding=16)
        self.frame.pack(fill="both", expand=True)

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)

        ttk.Label(self.frame, text=f"Bienvenido, {usuario.nombre}", font=("Segoe UI", 16, "bold")).grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 12)
        )
        ttk.Label(self.frame, text=f"Usuario: {usuario.identificacion} | Rol: {usuario.rol}").grid(
            row=1, column=0, columnspan=3, sticky="w", pady=(0, 8)
        )

        ttk.Label(self.frame, text="Productos", font=("Segoe UI", 11, "bold")).grid(row=2, column=0, sticky="w")
        ttk.Label(self.frame, text="Usuarios", font=("Segoe UI", 11, "bold")).grid(row=2, column=1, sticky="w")
        ttk.Label(self.frame, text="Categorías", font=("Segoe UI", 11, "bold")).grid(row=2, column=2, sticky="w")

        self.productos_listbox = tk.Listbox(self.frame, width=34, height=12)
        self.productos_listbox.grid(row=3, column=0, padx=(0, 12), sticky="nsew")

        self.usuarios_listbox = tk.Listbox(self.frame, width=34, height=12)
        self.usuarios_listbox.grid(row=3, column=1, padx=(0, 12), sticky="nsew")

        self.categorias_listbox = tk.Listbox(self.frame, width=24, height=12)
        self.categorias_listbox.grid(row=3, column=2, sticky="nsew")

        self.panel_usuarios = ttk.LabelFrame(self.frame, text="Gestión de usuarios")
        self.panel_usuarios.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=(16, 0))
        self.panel_usuarios.columnconfigure(0, weight=2)
        self.panel_usuarios.columnconfigure(1, weight=1)

        self.tree_usuarios = ttk.Treeview(
            self.panel_usuarios,
            columns=("identificacion", "nombre", "correo", "rol"),
            show="headings",
            height=6,
        )
        self.tree_usuarios.heading("identificacion", text="Identificación")
        self.tree_usuarios.heading("nombre", text="Nombre")
        self.tree_usuarios.heading("correo", text="Correo")
        self.tree_usuarios.heading("rol", text="Rol")
        self.tree_usuarios.column("identificacion", width=120, anchor="center")
        self.tree_usuarios.column("nombre", width=180)
        self.tree_usuarios.column("correo", width=220)
        self.tree_usuarios.column("rol", width=120, anchor="center")
        self.tree_usuarios.grid(row=0, column=0, sticky="nsew", padx=(10, 8), pady=10)
        self.tree_usuarios.bind("<<TreeviewSelect>>", self._seleccionar_usuario)

        self.formulario = ttk.Frame(self.panel_usuarios)
        self.formulario.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
        self.identificacion_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.correo_var = tk.StringVar()
        self.rol_var = tk.StringVar(value="Cliente")
        self.estado_var = tk.StringVar(value="Listo")

        self._agregar_campo("Identificación", self.identificacion_var, self.formulario, 0)
        self._agregar_campo("Nombre", self.nombre_var, self.formulario, 1)
        self._agregar_campo("Correo", self.correo_var, self.formulario, 2)

        ttk.Label(self.formulario, text="Rol:").grid(row=3, column=0, sticky="w", pady=(8, 4))
        self.rol_combo = ttk.Combobox(
            self.formulario,
            textvariable=self.rol_var,
            values=["Administrador", "Empleado", "Cliente"],
            state="readonly",
        )
        self.rol_combo.grid(row=3, column=1, sticky="ew", pady=(8, 4))
        self.rol_combo.bind("<<ComboboxSelected>>", self._evento_rol)

        self._crear_botones()
        ttk.Label(self.formulario, textvariable=self.estado_var, foreground="#1b5e20").grid(
            row=5, column=0, columnspan=2, sticky="w", pady=(10, 0)
        )

        self.identificacion_var.set("")
        self.nombre_var.set("")
        self.correo_var.set("")

        self.root.bind("<Escape>", self._limpiar_formulario)
        self.root.bind("<Return>", self._guardar_usuario)

        self._cargar_productos()
        self._cargar_usuarios()
        self._cargar_categorias()
        self._cargar_treeview_usuarios()
        self._actualizar_acceso_usuarios()

    def _agregar_campo(self, texto: str, variable: tk.StringVar, contenedor: ttk.Frame, fila: int) -> None:
        ttk.Label(contenedor, text=f"{texto}:").grid(row=fila, column=0, sticky="w", pady=(8, 4))
        entrada = ttk.Entry(contenedor, textvariable=variable, width=28)
        entrada.grid(row=fila, column=1, sticky="ew", pady=(8, 4))

    def _crear_botones(self) -> None:
        botones = ttk.Frame(self.formulario)
        botones.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        botones.columnconfigure((0, 1, 2, 3), weight=1)

        ttk.Button(botones, text="Registrar", command=self._guardar_usuario).grid(row=0, column=0, sticky="ew", padx=(0, 4))
        ttk.Button(botones, text="Actualizar", command=self._actualizar_usuario).grid(row=0, column=1, sticky="ew", padx=4)
        ttk.Button(botones, text="Eliminar", command=self._eliminar_usuario).grid(row=0, column=2, sticky="ew", padx=4)
        ttk.Button(botones, text="Limpiar", command=self._limpiar_formulario).grid(row=0, column=3, sticky="ew", padx=(4, 0))

    def _actualizar_acceso_usuarios(self) -> None:
        if self.usuario.rol != "Administrador":
            self.estado_var.set("Solo el administrador puede gestionar usuarios.")
            for widget in (self.tree_usuarios, self.rol_combo, self.formulario.winfo_children()):
                try:
                    widget.configure(state="disabled")
                except Exception:
                    pass
            return

        self.estado_var.set("Administrador activo: puede gestionar usuarios.")
        for child in self.formulario.winfo_children():
            if isinstance(child, ttk.Button):
                child.configure(state="normal")
            if isinstance(child, ttk.Entry):
                child.configure(state="normal")
        self.rol_combo.configure(state="readonly")
        self.tree_usuarios.configure(selectmode="browse")

    def _guardar_usuario(self, event=None) -> None:
        if self.usuario.rol != "Administrador":
            messagebox.showwarning("Acceso", "Solo el administrador puede registrar usuarios.")
            return

        identificacion = self.identificacion_var.get().strip()
        nombre = self.nombre_var.get().strip()
        correo = self.correo_var.get().strip()
        rol = self.rol_var.get().strip()

        if not identificacion or not nombre or not correo:
            messagebox.showwarning("Validación", "Debe completar identificación, nombre y correo.")
            return

        if self.restaurante.buscar_usuario(identificacion) is not None and self.usuario_seleccionado != identificacion:
            messagebox.showwarning("Duplicado", "Ya existe un usuario con esa identificación.")
            return

        usuario = Usuario(identificacion, nombre, correo, rol)
        if self.usuario_seleccionado == identificacion:
            self.restaurante.actualizar_usuario(identificacion, nombre, correo, rol)
            self.estado_var.set(f"Usuario actualizado: {identificacion}")
        else:
            self.restaurante.registrar_usuario(usuario)
            self.estado_var.set(f"Usuario registrado: {identificacion}")

        self.archivo.guardar_usuarios(self.restaurante.listar_usuarios())
        self._cargar_treeview_usuarios()
        self._limpiar_formulario()

    def _actualizar_usuario(self) -> None:
        if self.usuario.rol != "Administrador":
            messagebox.showwarning("Acceso", "Solo el administrador puede actualizar usuarios.")
            return

        identificacion = self.identificacion_var.get().strip()
        if not identificacion:
            messagebox.showwarning("Selección", "Seleccione un usuario para actualizar.")
            return

        usuario = self.restaurante.buscar_usuario(identificacion)
        if usuario is None:
            messagebox.showwarning("No encontrado", "El usuario seleccionado no existe.")
            return

        self._guardar_usuario()

    def _eliminar_usuario(self) -> None:
        if self.usuario.rol != "Administrador":
            messagebox.showwarning("Acceso", "Solo el administrador puede eliminar usuarios.")
            return

        identificacion = self.identificacion_var.get().strip()
        if not identificacion:
            messagebox.showwarning("Selección", "Seleccione un usuario para eliminar.")
            return

        if identificacion == self.usuario.identificacion:
            messagebox.showwarning("Protección", "No puedes eliminar tu propia cuenta administrativa.")
            return

        if messagebox.askyesno("Confirmar eliminación", f"¿Desea eliminar al usuario {identificacion}?"):
            if self.restaurante.eliminar_usuario(identificacion):
                self.archivo.guardar_usuarios(self.restaurante.listar_usuarios())
                self._cargar_treeview_usuarios()
                self.estado_var.set(f"Usuario eliminado: {identificacion}")
                self._limpiar_formulario()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario.")

    def _seleccionar_usuario(self, event=None) -> None:
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            return
        item = self.tree_usuarios.item(seleccion[0], "values")
        if not item:
            return
        identificacion, nombre, correo, rol = item
        self.usuario_seleccionado = identificacion
        self.identificacion_var.set(identificacion)
        self.nombre_var.set(nombre)
        self.correo_var.set(correo)
        self.rol_var.set(rol)
        self.estado_var.set(f"Usuario seleccionado: {identificacion}")

    def _evento_rol(self, event=None) -> None:
        self.estado_var.set(f"Rol seleccionado: {self.rol_var.get()}")

    def _limpiar_formulario(self, event=None) -> None:
        self.usuario_seleccionado = None
        self.identificacion_var.set("")
        self.nombre_var.set("")
        self.correo_var.set("")
        self.rol_var.set("Cliente")
        self.estado_var.set("Formulario limpio.")
        if self.tree_usuarios.selection():
            self.tree_usuarios.selection_remove(self.tree_usuarios.selection()[0])

    def _cargar_productos(self) -> None:
        self.productos_listbox.delete(0, tk.END)
        for producto in self.restaurante.listar_productos():
            self.productos_listbox.insert(tk.END, f"{producto.codigo} - {producto.nombre} - Stock: {producto.stock}")

    def _cargar_usuarios(self) -> None:
        self.usuarios_listbox.delete(0, tk.END)
        for usuario in self.restaurante.listar_usuarios():
            self.usuarios_listbox.insert(tk.END, f"{usuario.identificacion} - {usuario.nombre} - {usuario.rol}")

    def _cargar_categorias(self) -> None:
        self.categorias_listbox.delete(0, tk.END)
        for categoria in sorted(self.restaurante.obtener_categorias()):
            self.categorias_listbox.insert(tk.END, categoria)

    def _cargar_treeview_usuarios(self) -> None:
        self.tree_usuarios.delete(*self.tree_usuarios.get_children())
        for usuario in self.restaurante.listar_usuarios():
            self.tree_usuarios.insert(
                "",
                tk.END,
                values=(usuario.identificacion, usuario.nombre, usuario.correo, usuario.rol),
            )
