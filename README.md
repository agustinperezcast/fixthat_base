# Gestor básico de contactos

Aplicación web local para practicar operaciones CRUD con formularios y SQLite: crear, consultar, editar y eliminar registros.

## Requisitos

- Python 3.9 o posterior
- `pip` (incluido normalmente con Python)

SQLite viene incluido con Python; no hace falta instalar ni configurar un servidor de base de datos.

## Instalación y ejecución

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
python -m venv .venv
```

Activa el entorno virtual:

- **Windows (PowerShell):** `.venv\\Scripts\\Activate.ps1`
- **Windows (CMD):** `.venv\\Scripts\\activate.bat`
- **macOS/Linux:** `source .venv/bin/activate`

Instala Flask y ejecuta la aplicación:

```bash
python -m pip install -r requirements.txt
python app.py
```

Abre <http://127.0.0.1:5000> en el navegador. La base de datos se crea automáticamente en `instance/contacts.sqlite3`.

## Qué incluye

- Listado de contactos.
- Formulario para crear y editar registros.
- Eliminación con confirmación.
- Validación del nombre obligatorio.
- Consultas SQLite parametrizadas.
- Protección CSRF básica en formularios de escritura.

> Esta aplicación está pensada para ejecutarse localmente. No la publiques en Internet tal cual. Si la adaptas para un entorno real, configura una clave secreta fuerte en la variable de entorno `SECRET_KEY` y añade las medidas de seguridad y despliegue apropiadas.
