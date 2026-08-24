# Task Manager API

API REST para la gestión de tareas con autenticación de usuarios, construida con FastAPI y arquitectura por capas (Router / Service / Repository).

Aunque el dominio de ejemplo es un gestor de tareas, la arquitectura está pensada para adaptarse fácilmente a otros contextos que requieran manejo seguro de registros con autenticación — inventarios, nóminas, listas de personal, historiales de salud, o cualquier sistema donde la integridad y trazabilidad de los datos importe.

🔗 **Demo en vivo:** [https://task-manager-api-mwik.onrender.com](https://task-manager-api-mwik.onrender.com)

> Nota: el servicio corre en el plan gratuito de Render, por lo que la primera petición puede tardar unos segundos en responder (cold start).

## Características

- CRUD completo de tareas (crear, leer, actualizar, eliminar)
- Registro y autenticación de usuarios con JWT
- Contraseñas hasheadas con bcrypt (nunca se almacenan en texto plano)
- Endpoints protegidos: crear, actualizar y eliminar tareas requiere autenticación
- Manejo de errores centralizado con códigos HTTP correctos (401, 404, 409)
- Tokens JW
T con expiración
- Documentación interactiva automática (Swagger UI)
- Suite de tests automatizados con pytest

## Stack técnico

- **Framework:** FastAPI
- **Base de datos:** SQLite
- **Autenticación:** JWT (PyJWT) + OAuth2PasswordBearer
- **Validación de datos:** Pydantic
- **Testing:** pytest
- **Despliegue:** Render

## Instalación y ejecución local

```bash
# Clonar el repositorio
git clone https://github.com/mateomerchan100-lab/task_manager_api.git
cd task_manager_api

# Crear y activar entorno virtual
python -m venv venv
venv\Scripts\Activate      # Windows
source venv/bin/activate   # macOS/Linux

# Instalar dependencias
pip install -r requirements.txt
```

### Variables de entorno

Crea un archivo `.env` en la raíz del proyecto con:

DATABASE_NAME=tasks.db
SECRET_KEY=tu_clave_secreta_generada


Puedes generar una clave segura con:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Ejecutar el servidor

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`, con documentación interactiva en `http://127.0.0.1:8000/docs`.

### Ejecutar los tests

```bash
pytest
```

## Endpoints principales

| Método | Ruta | Descripción | Requiere autenticación |
|--------|------|-------------|:---:|
| POST | `/register` | Registrar un nuevo usuario | No |
| POST | `/login` | Iniciar sesión y obtener token JWT | No |
| GET | `/tasks` | Listar todas las tareas | No |
| POST | `/tasks` | Crear una nueva tarea | Sí |
| PUT | `/tasks/{task_id}` | Actualizar el estado de una tarea | Sí |
| DELETE | `/tasks/{task_id}` | Eliminar una tarea | Sí |

## Estructura del proyecto



app/
├── auth/ # Seguridad: hashing, JWT
├── config/ # Configuración y variables de entorno
├── database/ # Conexión y esquema de la base de datos
├── models/ # Esquemas de entrada/salida (Pydantic)
├── repositories/ # Acceso a datos
├── routers/ # Endpoints de la API
├── services/ # Lógica de negocio
├── tests/ # Tests automatizados
├── exception_handlers.py
└── main.py