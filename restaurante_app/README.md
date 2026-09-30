# restaurante_app - Semana 16

## Estudiante

Nombre completo: Gino Paul Ponce Quezada

## Descripción

Sistema de administración de un restaurante desarrollado en Python con Tkinter. La aplicación conserva la arquitectura modular de semanas anteriores y evoluciona la gestión de usuarios con manejo de eventos, roles básicos y persistencia en archivos JSON.

La Semana 16 se centra en la gestión de usuarios con Treeview y eventos de interfaz: `<<TreeviewSelect>>`, `<Return>`, `<Escape>` y `<<ComboboxSelected>>`, manteniendo la lógica de negocio en el servicio y evitando duplicar código dentro de la interfaz.

## Estructura del proyecto

```text
restaurante_app/
├── assets/
│   ├── icon.svg
│   └── logo.svg
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   ├── restaurante.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── tests/
│   └── test_restaurante.py
├── main.py
├── README.md
└── .gitignore
```

## Responsabilidades

- `Producto`: representa el código, nombre, categoría, precio y stock.
- `Usuario`: incluye identificación, nombre, correo y rol. Los roles soportados son `Administrador`, `Empleado` y `Cliente`.
- `Venta`: registra la relación entre usuario y producto con la cantidad vendida.
- `Restaurante`: administra las colecciones, validaciones y búsquedas por índices.
- `ArchivoServicio`: carga y guarda los archivos JSON.
- `MainView`: coordina el formulario, la tabla `Treeview`, la selección y los callbacks.
- `main.py`: crea la ventana principal y lanza la lógica de login y navegación.

## Roles y acceso

El modelo `Usuario` incorpora el atributo `rol` con validación específica. La gestión de usuarios solo está disponible para el usuario con rol `Administrador`.

El flujo de acceso es el siguiente:

- El administrador inicia sesión con su cuenta.
- En la vista principal, puede gestionar usuarios desde un panel con `Treeview` y formulario.
- Un `Empleado` o `Cliente` no tiene permiso para operar la administración de usuarios.

## Manejo de eventos de la Semana 16

La interfaz de usuarios utiliza varios eventos para responder a interacciones reales:

- `<<TreeviewSelect>>`: al seleccionar una fila, se carga el usuario en el formulario.
- `<Return>`: ejecuta el registro o actualización del usuario con el atajo del teclado.
- `<Escape>`: limpia el formulario y cancela la selección activa.
- `<<ComboboxSelected>>`: responde al cambio del rol elegido en el `Combobox`.
- `command=`: se usa en los botones de registrar, actualizar, eliminar y limpiar.

Toda la lógica de validación y persistencia se mantiene en `Restaurante` y `ArchivoServicio`; la vista solo coordina la interacción.

## Persistencia JSON

Los usuarios se guardan en `datos/usuarios.json` con el campo `rol` incluido. Cuando el sistema inicia, recarga la información y reconstruye los índices para que la búsqueda y actualización de usuarios funcionen correctamente.

## Ejecución

Desde la carpeta raíz:

```bash
python main.py
```

Se iniciará la aplicación en Tkinter, mostrando primero la vista de login. Si la identificación corresponde a un usuario registrado, se accede a la vista principal. Desde ahí, el administrador puede gestionar usuarios y observar la información reflejada en la tabla.

## Recursos visuales

La carpeta `assets/` incluye recursos gráficos mínimos para mantener una experiencia visual coherente:

- `assets/icon.svg`
- `assets/logo.svg`

## Pruebas realizadas

```bash
python -m pytest -q
```

Resultado verificado: `8 passed in 0.05s`.

La validación cubre la compatibilidad de la lógica previa con la nueva gestión de usuarios y el rol. También se verificó la actualización de usuarios con roles y la persistencia del campo `rol`.
