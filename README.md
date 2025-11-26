# link de la api 

https://plataforma-de-gesti-n-de-fincas-y.onrender.com/api/docs/


# Plataforma de Gestión de Fincas y Operaciones Agrícolas

Sistema modular desarrollado con Django REST Framework para la administración integral de operaciones agrícolas, incluyendo gestión de fincas, tareas, trabajadores e insumos.

## Equipo de Desarrollo

- **Líder:** [Sarah Castro] - Fincas/Lotes
- **Dev 2:** [Mariana Valderrama] - Tareas Agrícolas  
- **Dev 3:** [Saira Aragon] - Trabajadores
- **Dev 4:** [Sara Martinez] - Insumos

## Descripción del Proyecto

Plataforma backend que permite administrar todas las operaciones de una explotación agrícola moderna, desde la gestión de terrenos hasta el control de insumos y la trazabilidad completa de los cultivos.

## Requerimientos Técnicos

* Python 3.13
* DBeaver (Base de datos)
* Laragon (Activación de MySQL)
* Django REST Framework

## Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/Sarah-con-h/Plataforma-de-Gesti-n-de-Fincas-y-Operaciones-Agr-colas.git
```
### 2. Crear y activar entorno virtual

```bash
# Windows
python -m venv .venv
venv\Scripts\activate
```
### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copiar el archivo `.env.example` a `.env` y configurar las variables:

```bash
cp .env.example .env
```

### 5. Creación de base de datos
### Para este proyecto se utilizó Laragon como metodo para activar MySQL

**Paso 1: Iniciar Laragon**
1. Abrir Laragon
2. Click en "MySQL" (Verificar que quede activado)

**Paso 2: Crear base de datos con DBeaver**
1. Abrir DBeaver
2. Conectar a MySQL:
   - Click derecho en "Connections" → "Create" → "New Database Connection"
   - Seleccionar "MySQL"
   - Configurar conexión:
     ```
     Host: localhost
     Port: 3306
     Database: (dejar vacío por ahora)
     Username: root
     Password: (dejar vacío o la que configuraste en Laragon)
     ```
   - Click en "Test Connection" para verificar
   - Click en "Finish"
3. Crear la base de datos:
   - Click derecho a "crear nuevo Database"
   - En Data name: "gestion_finca"
   - Click en aceptar
4. Verificar que la base de datos fue creada:
   - Refrescar la conexión (F5)
   - Debe aparecer "gestion_finca" en la lista de bases de datos

**Paso 3: Configurar .env para MySQL con Laragon**

```Archivo .env

SECRET_KEY=your_secret_key_here
DEBUG=True
DB_NAME='gestion_finca'
DB_USER='root'
DB_PASSWORD=''
DB_HOST=localhost
DB_PORT=3306
```

### 6. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```
### 9. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

La aplicación estará disponible en: `http://127.0.0.1:8000/api/docs/`

## Estructura del Proyecto

```
gestion_fincas_agricolas/
│
├── config/                          # Proyecto principal
│   ├── __init__.py
│   ├── settings.py               # Configuración general
│   ├── urls.py                   # URLs principales
│   ├── wsgi.py
│   └── asgi.py
│
├── fincas/                        # App: Gestión de fincas y lotes
│   ├── models.py                 # Finca, Lote
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── filters.py
│   └── tests.py
│
├── tareas/                        # App: Tareas agrícolas
│   ├── models.py                 # TipoTarea, Tarea
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── filters.py
│   └── tests.py
│
├── trabajadores/                  # App: Gestión de trabajadores
│   ├── models.py                 # Trabajador, Asignacion
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── filters.py
│   └── tests.py
│
├── insumos/                       # App: Control de insumos
│   ├── models.py                 # Insumo, Movimiento, Consumo
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── filters.py
│   └── tests.py
│
├── .env                          # Variables de entorno (no subir a Git)
├── .env.example                  # Ejemplo de variables de entorno
├── .gitignore
├── requirements.txt
├── manage.py
└── README.md
```

## Diagrama de Base de Datos

### Modelo General

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Finca     │         │    Lote     │         │    Tarea    │
├─────────────┤         ├─────────────┤         ├─────────────┤
│ id (PK)     │────1:N──│ id (PK)     │────1:N──│ id (PK)     │
│ nombre      │         │ finca (FK)  │         │ lote (FK)   │
│ ubicacion   │         │ area        │         │ tipo        │
│ area_total  │         │ cultivo     │         │ fecha       │
└─────────────┘         └─────────────┘         │ estado      │
                                                 └─────────────┘
                                                        │
                                                        │N:M
                        ┌─────────────┐                │
                        │ Trabajador  │         ┌──────▼──────┐
                        ├─────────────┤         │ Asignacion  │
                        │ id (PK)     │────1:N──│ trabajador  │
                        │ nombre      │         │ tarea       │
                        │ rol         │         │ horas       │
                        │ salario     │         └─────────────┘
                        └─────────────┘
                                                 ┌─────────────┐
                        ┌─────────────┐         │   Consumo   │
                        │   Insumo    │────1:N──│ insumo (FK) │
                        ├─────────────┤         │ tarea (FK)  │
                        │ id (PK)     │         │ cantidad    │
                        │ nombre      │         └─────────────┘
                        │ stock       │
                        │ unidad      │
                        └─────────────┘
```

## .gitignore

Se creó un archivo .gitignore para excluir archivos y carpetas que no deben subirse al repositorio, siguiendo buenas prácticas de control de versiones.
Esto evita exponer información sensible (como variables de entorno) y reduce archivos innecesarios, como los generados por el entorno virtual o por Python.

Archivos y directorios ignorados:
```
.venv/
env/
.env
__pycache__/
*.pyc

```

## Uso de Variables de Entorno

El proyecto utiliza `python-decouple` para gestionar variables sensibles. 

**Archivo `.env.example`:**
```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=fincas_db
DATABASE_USER=postgres
DATABASE_PASSWORD=password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

## Documentación Swagger/OpenAPI

La documentación interactiva de la API está disponible en:

- **Swagger UI:** `http://localhost:8000/swagger/`
- **ReDoc:** `http://localhost:8000/redoc/`
- **JSON Schema:** `http://localhost:8000/swagger.json`

## Endpoints por Aplicación

### Fincas/Lotes (`/api/fincas/`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/fincas/` | Listar todas las fincas |
| POST | `/fincas/` | Crear nueva finca |
| GET | `/fincas/{id}/` | Detalle de finca |
| PUT/PATCH | `/fincas/{id}/` | Actualizar finca |
| DELETE | `/fincas/{id}/` | Eliminar finca |
| GET | `/fincas/?area_min=X&area_max=Y` | Filtrar por área |
| GET | `/lotes/` | Listar lotes |
| GET | `/lotes/?cultivo=maiz` | Filtrar por cultivo |
| GET | `/lotes/{id}/planificacion-semanal/` | 📊 Planificación semanal del lote |

### Tareas Agrícolas (`/api/tareas/`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/tareas/` | Listar tareas |
| POST | `/tareas/` | Crear nueva tarea |
| GET | `/tareas/{id}/` | Detalle de tarea |
| PUT/PATCH | `/tareas/{id}/` | Actualizar tarea |
| DELETE | `/tareas/{id}/` | Eliminar tarea |
| GET | `/tareas/?fecha_inicio=&fecha_fin=` | Filtrar por fechas |
| GET | `/tareas/?estado=pendiente` | Filtrar por estado |
| GET | `/tareas/estadisticas-periodo/` | 📊 Estadísticas de tareas |

### Trabajadores (`/api/trabajadores/`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/trabajadores/` | Listar trabajadores |
| POST | `/trabajadores/` | Crear trabajador |
| GET | `/trabajadores/{id}/` | Detalle de trabajador |
| PUT/PATCH | `/trabajadores/{id}/` | Actualizar trabajador |
| DELETE | `/trabajadores/{id}/` | Eliminar trabajador |
| GET | `/trabajadores/?rol=operario` | Filtrar por rol |
| GET | `/trabajadores/{id}/horas-mes/` | 📊 Horas trabajadas en el mes |
| GET | `/asignaciones/?trabajador=X` | Filtrar asignaciones |

### Insumos (`/api/insumos/`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/insumos/` | Listar insumos |
| POST | `/insumos/` | Crear insumo |
| GET | `/insumos/{id}/` | Detalle de insumo |
| PUT/PATCH | `/insumos/{id}/` | Actualizar insumo |
| DELETE | `/insumos/{id}/` | Eliminar insumo |
| GET | `/insumos/?stock_min=X` | Filtrar por stock bajo |
| GET | `/insumos/?categoria=fertilizante` | Filtrar por categoría |
| GET | `/insumos/{id}/historial-consumo/` | 📊 Historial de consumo |
| GET | `/trazabilidad/{lote_id}/` | 🔍 Trazabilidad completa |

## Flujo de Trabajo con Git

### Configuración inicial (Líder)

```bash
git init
git add .
git commit -m "Initial commit: Django project structure"
git branch -M main
git remote add origin https://github.com/usuario/gestion-fincas-agricolas.git
git push -u origin main
```

### Desarrollo por miembro del equipo

```bash
# 1. Clonar y crear rama
git clone https://github.com/usuario/gestion-fincas-agricolas.git
git checkout -b feature-fincas-juan

# 2. Desarrollar la aplicación
# ... código ...

# 3. Commit y push
git add .
git commit -m "feat: Implementa app fincas con CRUD y filtros"
git push origin feature-fincas-juan

# 4. Crear Pull Request en GitHub
# 5. Esperar revisión del líder
```

### Integración (Líder)

```bash
# Revisar PR en GitHub
# Aprobar y hacer merge
# Actualizar rama local
git checkout main
git pull origin main
```

## Roles del Equipo

| Miembro | Rol | Aplicación | Responsabilidad |
|---------|-----|------------|-----------------|
| **Sarah** | Líder / Dev | Fincas/Lotes | Config inicial + App Fincas |
| **Mariana** | Desarrollador | Tareas Agrícolas | CRUD Tareas + Planificación |
| **Saira** | Desarrollador | Trabajadores | Gestión personal + Asignaciones |
| **Sara** | Desarrollador | Insumos | Control inventario + Trazabilidad |

## Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Add: nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

## Conclusión

Este proyecto integra buenas prácticas de desarrollo , control de versiones y organización
del entorno de trabajo. A través de la implementación del archivo .gitignore, el manejo 
adecuado del repositorio y la estructura del proyecto, se garqantiza un flujo de trabajo más 
limpio, ordenado y eficiente. Estos elementos permiten mantener el código actualizado, facilitar
la colaboración y asegurar que el proyecto pueda escalar y mantenerse de manera adecuada a lo 
largo del tiempo.
