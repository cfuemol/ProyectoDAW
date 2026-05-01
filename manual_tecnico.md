<a id="top"></a>

# Manual Técnico Profesional / Professional Technical Manual

### Sistema de Gestión de Cuadrantes Sanitarios / Healthcare Shift Management System

---

**Idiomas / Languages:**

- [Español](#español) 🇪🇸
- [English](#english) 🇬🇧

---

<a id="español"></a>

## 🇪🇸 MANUAL TÉCNICO (ESPAÑOL)

Este documento constituye la memoria técnica del proyecto, proporcionando conocimiento sobre el funcionamiento del sistema.

### 1. Introducción

#### 1.1 Contexto y Objetivos

En entornos sanitarios críticos, la gestión de turnos ("cuadrantes") presenta desafíos de alta complejidad debido a la necesidad de cubrir servicios 24/7, respetar descansos legales post-guardia y gestionar la disponibilidad del personal. Este sistema nace para automatizar estas reglas de negocio, eliminando el error humano y centralizando la comunicación de incidencias.

#### 1.2 Objetivos Estratégicos

- **Disponibilidad**: Garantizar el acceso a la información de turnos desde cualquier dispositivo.
- **Trazabilidad**: Registro inmutable de todos los intercambios de guardia entre profesionales.
- **Cumplimiento**: Validación algorítmica de normativas laborales (descansos de 24h tras guardias de 17h/24h).

---

### 2. Arquitectura del Sistema

El sistema implementa una arquitectura de servicios desacoplados bajo un modelo de **Modelo-Vista-Controlador (MVC)**, orquestado mediante contenedores Docker.

#### 2.1 Diagrama de Arquitectura de Red

```mermaid
graph TD
    User([Usuario/Navegador]) <-->|HTTP/HTTPS Port 80| Nginx[Proxy Inverso Nginx]

    subgraph "Contenedor Aplicación"
    Nginx <-->|Unix Socket / Proxy Pass| Gunicorn[Servidor WSGI Gunicorn]
    Gunicorn <-->|Python App| Flask[Backend Flask]
    end

    subgraph "Persistencia"
    Flask <-->|Motor Mongoengine| MongoDB[(Motor de Base de Datos MongoDB)]
    MongoDB <-->|Vínculo de Volumen| Storage[(Almacenamiento Persistente)]
    end
```

---

### 3. Tecnologías Utilizadas

#### 3.1 Justificación del Stack Tecnológico

- **Flask (Backend)**: Microframework elegido por su modularidad y velocidad en el desarrollo de APIs RESTful y servicios ligeros.
- **MongoDB (Base de Datos)**: Modelo NoSQL orientado a documentos que permite almacenar turnos con estructuras dinámicas (centros especiales, anotaciones) sin las rigideces de un esquema relacional.
- **Gunicorn (WSGI)**: Servidor de producción que permite el manejo de múltiples trabajadores (_pre-fork worker model_), mejorando la concurrencia.
- **Mermaid/Jinja2**: Para la renderización dinámica de datos en el cliente con mínima sobrecarga de procesamiento.

---

### 4. Instalación y Configuración Avanzada

#### 4.1 Variables de Envierno (.env)

El sistema requiere el siguiente esquema de configuración:

| Variable         | Descripción                          | Valor Ejemplo |
| :--------------- | :----------------------------------- | :------------ |
| `MONGO_USER`     | Usuario administrativo de la BD      | root          |
| `MONGO_PASSWORD` | Contraseña de acceso a la BD         | ****\*\*****  |
| `MONGO_DB`       | Nombre de la base de datos           | guardias      |
| `MONGO_HOST`     | Host del servicio (nombre en Docker) | mongodb       |
| `FLASK_PORT`     | Puerto interno de escucha de Flask   | 8000          |

#### 4.2 Despliegue con Orquestación

El despliegue se realiza mediante `Docker Compose`, el cual aísla los servicios en una red privada virtual donde solo el puerto 80 es accesible desde el exterior.

---

### 5. Estructura del Proyecto

```text
ProyectoDAW/
├── app.py                      # Controlador Principal (Flask)
├── .gitignore                  # Reglas de exclusión para Git
├── docker-compose.yml          # Orquestación de contenedores
├── docker_start.sh             # Script de inicio automatizado
├── .env.example                # Plantilla de variables de entorno
├── pytest.ini                  # Configuración de pruebas
├── requirements.txt            # Dependencias de Python
├── run_tests.sh                # Script de automatización de tests
├── manual_tecnico.md           # Memoria técnica
├── manual_usuario.md           # Guía para el usuario final
├── README.md                   # Repositorio (Español/Inglés)
├── LICENSE                     # Licencia del proyecto
├── docker/                     # Configuración de infraestructura
│   ├── Dockerfile              # Construcción de la imagen Flask
│   ├── nginx.conf              # Configuración del servidor Proxy
│   └── mongo-init/             # Inicialización de la base de datos
│       └── init.js             # Script de creación de colecciones
├── models/                     # Capa de datos (MongoEngine)
│   ├── __init__.py
│   ├── database.py             # Conexión al motor MongoDB
│   ├── usuario.py              # Gestión de Usuarios y Roles
│   ├── turno.py                # Definición de Turnos
│   ├── cambio.py               # Lógica de Intercambios
│   ├── plan_diario.py          # Organización por días
│   └── saliente.py             # Lógica de descanso post-guardia
├── static/                     # Archivos estáticos
│   ├── css/                    # Estilos Glassmorphing personalizados
│   │   ├── styles_base.css
│   │   ├── styles_login.css
│   │   ├── styles_cuadrante.css
│   │   └── (otros archivos específicos por vista...)
│   ├── images/                 # Capturas para documentación y recursos
│   │   ├── login.png
│   │   ├── cambiar_pass.png
│   │   └── (imágenes secuenciales 1-8)
│   └── scripts/                # Lógica de frontend (JavaScript)
│       ├── base.js             # Ping de actividad y notificaciones
│       ├── ver_cuadrante.js
│       ├── pedir_cambio.js
│       └── (scripts específicos por funcionalidad...)
├── templates/                  # Plantillas de Jinja2
│   ├── base.html               # Estructura principal reutilizable
│   ├── login.html              # Pantalla de acceso
│   ├── admin/                  # Panel de administrador
│   │   ├── admin_dashboard.html
│   │   ├── register.html
│   │   ├── edit_usuario.html
│   │   └── borrar_usuarios.html
│   ├── direccion/              # Gestión de dirección
│   │   ├── direccion_dashboard.html
│   │   ├── gestion_turnos.html
│   │   ├── notificaciones_cambios.html
│   │   └── ver_turnos_profesional.html
│   ├── profesional/            # Portal del profesional
│   │   ├── profesional_dashboard.html
│   │   ├── ver_cuadrante.html
│   │   ├── pedir_cambio.html
│   │   ├── solicitudes_cambio.html
│   │   ├── historico_cambios.html
│   │   └── cambiar_password.html
│   └── includes/               # Fragmentos de navegación por rol
├── tests/                      # Suite de pruebas unitarias/integración
│   ├── __init__.py
│   ├── conftest.py             # Fixtures de Pytest y Mocking de DB
│   ├── test_admin.py
│   ├── test_direccion.py
│   ├── test_profesional.py
│   └── test_saliente_adjustment.py
└── docs/                       # Documentación de Sprints y Diseño
    ├── Sprint_1-4.md
    ├── Arquitectura.md
    └── Viabilidad_Tecnica.md
```

#### 5.1 Descripción de Componentes

- **Raíz del Proyecto**: Contiene los archivos de configuración global para el despliegue Docker y la gestión de dependencias.
- **models/**: Implementa la lógica de persistencia. Se utiliza MongoEngine para mapear objetos Python a documentos de MongoDB, permitiendo consultas paginadas eficientes (ej. listados de usuarios).
- **static/**: Organizado en estilos (CSS) que siguen el patrón Glassmorphism y scripts (JS) que manejan la interactividad en tiempo real (polling).
- **templates/**: Dividido por áreas de seguridad (Admin, Dirección, Profesional) para garantizar la integridad de los permisos.
- **docker/**: Aísla la configuración de red y servidor, permitiendo un entorno de "infraestructura como código".
- **tests/**: Validaciones automatizadas de todas las reglas de negocio críticas, asegurando la robustez del sistema ante cambios.

---

### 6. Base de Datos

#### 6.1 Diagrama de Relación de Entidades (ERD)

```mermaid
classDiagram
    class Usuario {
        +String dni (PK)
        +String nombre
        +String categoria
        +String rol
        +set_password(pass)
        +check_password(pass)
    }
    class Turno {
        +ObjectId id
        +ReferenceField profesional
        +DateField fecha
        +String tipo
        +String centro_trabajo
    }
    class Cambio {
        +ReferenceField profesional1
        +ReferenceField profesional2
        +DateField fecha_original
        +String estado [Pendiente, Aceptado, Rechazado]
        +Boolean visto_por_direccion
    }

    Usuario "1" -- "*" Turno : asignado_a
    Turno "1" -- "0..1" Cambio : origen_del_cambio
    Cambio "*" -- "2" Usuario : involucra
```

---

### 7. Despliegue en Producción

El sistema utiliza un proceso de dos etapas para la entrega:

#### 7.1 Inicio Automatizado

Se recomienda el uso de `docker_start.sh` para el despliegue inicial. Este script garantiza:

1. Existencia del archivo `.env`.
2. Generación de un `SECRET_KEY` criptográficamente seguro para Flask.
3. Orquestación automática de contenedores.

#### 7.2 Arquitectura de Imágenes

1. **Build**: Generación de la imagen de Flask basada en `python:3.11-slim` para reducir el tamaño de ataque.
2. **Runtime**: Ejecución bajo Nginx con configuración de seguridad (limitación de tamaño de cuerpo de petición, ocultación de versiones de servidor).

---

### 8. Mantenimiento y Escalabilidad

#### 8.1 Estrategia de Backups

Se recomienda el uso del motor de backups nativo de MongoDB:

```bash
docker exec mongo_guardias mongodump --uri="mongodb://root:pass@localhost:27017/guardias" --archive=/data/db/backup.archive
```

#### 8.2 Escalabilidad Horizontal

Gracias al diseño _stateless_ del backend, se pueden levantar múltiples réplicas del servicio `flask` y balancear la carga mediante el proxy inverso Nginx.

---

### 9. Seguridad

#### 9.1 Protocolos Implementados

- **Protección de Datos en Memoria**: Los identificadores personales (DNI) se almacenan en la memoria RAM del servidor como hashes criptográficos (SHA-256) para el control de usuarios activos, impidiendo la filtración de datos ante hipotéticos volcados de memoria.
- **Autenticación**: Proceso de login securizado mediante el flujo de autenticación detallado:

```mermaid
sequenceDiagram
    participant U as Usuario
    participant A as app.py
    participant B as MongoDB

    U->>A: Envía DNI + Password
    A->>B: Consulta Usuario por DNI
    B-->>A: Retorna Hash de Password
    A->>A: werkzeug.check_password_hash()
    alt Credenciales Válidas
        A-->>U: Asigna Cookie de Sesión + Redirige Dashboard
    else Inválidas
        A-->>U: Retorna Error + Flash Message
    end
```

---

### 10. Pruebas y Calidad

Se implementa una suite de pruebas basada en `pytest` que cubre:

- **Unit Testing**: Validación individual de métodos de modelos.
- **Integration Testing**: Pruebas de rutas de la API simulando peticiones HTTP.
- **Mocking**: Aislamiento total de la base de datos para asegurar que los tests sean idempotentes y rápidos.

---

### 11. Problemas Frecuentes (Troubleshooting)

| Problema                        | Causa Probable                      | Solución                            |
| :------------------------------ | :---------------------------------- | :---------------------------------- |
| Error 502 Bad Gateway           | Flask/Gunicorn no está activo       | `docker logs flask_guardias`        |
| Fallo al generar PDF            | Faltan campos en el modelo de Turno | Verificar consistencia en la BD     |
| Notificaciones no se actualizan | Error en el polling JS              | Revisar consola del navegador (F12) |

---

### 12. Anexos

#### 12.1 Diagrama de Secuencia de Intercambio de Turnos

```mermaid
sequenceDiagram
    participant P1 as Profesional A
    participant P2 as Profesional B
    participant S as Servidor
    participant D as Dirección

    P1->>S: Solicita cambio (P1_Turno <--> P2_Turno)
    S->>S: Valida reglas de descanso laboral
    S-->>P2: Notifica Solicitud (Badge)
    P2->>S: Acepta Intercambio
    S->>S: Actualiza Turnos en la BD
    S-->>D: Notifica a Dirección (Badge "Nuevo")
```

---

[Volver al inicio / Back to top](#top)

---

<a id="english"></a>

## 🇬🇧 TECHNICAL MANUAL (ENGLISH)

This document constitutes the comprehensive technical report of the project, providing fundamental knowledge about the system's architecture and operation.

### 1. Introduction

#### 1.1 Context and Objectives

In critical healthcare environments, shift management ("quadrants") presents high-complexity challenges due to the need for 24/7 service coverage, compliance with legal post-guard rest periods, and personnel availability management. This system was created to automate these business rules, eliminate human error, and centralize incident communication.

#### 1.2 Strategic Objectives

- **Availability**: Ensure access to shift information from any device.
- **Traceability**: Inmutable record of all guard shift swaps between professionals.
- **Compliance**: Algorithmic validation of labor regulations (24h rest after 17h/24h guard shifts).

---

### 2. System Architecture

The system implements a decoupled services architecture under a **Model-View-Controller (MVC)** pattern, orchestrated using Docker containers.

#### 2.1 Network Architecture Diagram

```mermaid
graph TD
    User([User/Browser]) <-->|HTTP/HTTPS Port 80| Nginx[Nginx Reverse Proxy]

    subgraph "Application Container"
    Nginx <-->|Unix Socket / Proxy Pass| Gunicorn[Gunicorn WSGI Server]
    Gunicorn <-->|Python App| Flask[Flask Backend]
    end

    subgraph "Persistence"
    Flask <-->|Mongoengine Engine| MongoDB[(MongoDB Database Engine)]
    MongoDB <-->|Volume Bound| Storage[(Persistent Storage)]
    end
```

---

### 3. Technologies Used

#### 3.1 Tech Stack Justification

- **Flask (Backend)**: Microframework chosen for its modularity and speed in developing RESTful APIs and lightweight services.
- **MongoDB (Database)**: Document-oriented NoSQL model that allows storing shifts with dynamic structures (special centers, annotations) without the rigidities of a relational schema.
- **Gunicorn (WSGI)**: Production server that allows handling multiple workers (_pre-fork worker model_), improving concurrency.
- **Mermaid/Jinja2**: For dynamic data rendering on the client with minimal processing overhead.

---

### 4. Installation & Advanced Configuration

#### 4.1 Environment Variables (.env)

The system requires the following configuration schema:

| Variable         | Description                   | Example Value |
| :--------------- | :---------------------------- | :------------ |
| `MONGO_USER`     | DB administrative user        | root          |
| `MONGO_PASSWORD` | DB access password            | ****\*\*****  |
| `MONGO_DB`       | Database name                 | guardias      |
| `MONGO_HOST`     | Service host (Docker name)    | mongodb       |
| `FLASK_PORT`     | Flask internal listening port | 8000          |

#### 4.2 Orchestrated Deployment

Deployment is performed using `Docker Compose`, which isolates services in a virtual private network where only port 80 is accessible from the outside.

---

### 5. Project Structure

```text
ProyectoDAW/
├── app.py                      # Main Controller (Flask)
├── .gitignore                  # Git exclusion rules
├── docker-compose.yml          # Container orchestration
├── docker_start.sh             # Automated startup script
├── .env.example                # Environment variables template
├── pytest.ini                  # Test configuration
├── requirements.txt            # Python dependencies
├── run_tests.sh                # Test automation script
├── manual_tecnico.md           # Technical manual
├── manual_usuario.md           # End-user guide
├── README.md                   # Repository docs (Spanish/English)
├── LICENSE                     # Project license
├── docker/                     # Infrastructure configuration
│   ├── Dockerfile              # Flask image construction
│   ├── nginx.conf              # Proxy server configuration
│   └── mongo-init/             # Database initialization
│       └── init.js             # Collection creation script
├── models/                     # Data layer (MongoEngine)
│   ├── __init__.py
│   ├── database.py             # MongoDB connection setup
│   ├── usuario.py              # User and Role management
│   ├── turno.py                # Shift definitions
│   ├── cambio.py               # Swap logic
│   ├── plan_diario.py          # Daily planning
│   └── saliente.py             # Post-guard rest logic
├── static/                     # Static files
│   ├── css/                    # Custom Glassmorphism styles
│   │   ├── styles_base.css
│   │   ├── styles_login.css
│   │   ├── styles_cuadrante.css
│   │   └── (other view-specific files...)
│   ├── images/                 # Documentation screenshots and assets
│   │   ├── login.png
│   │   ├── cambiar_pass.png
│   │   └── (sequential images 1-8)
│   └── scripts/                # Frontend logic (JavaScript)
│       ├── base.js             # Activity ping and notifications
│       ├── ver_cuadrante.js
│       ├── pedir_cambio.js
│       └── (specific functionality scripts...)
├── templates/                  # Jinja2 templates
│   ├── base.html               # Main reusable structure
│   ├── login.html              # Login screen
│   ├── admin/                  # Admin panel
│   │   ├── admin_dashboard.html
│   │   ├── register.html
│   │   ├── edit_usuario.html
│   │   └── borrar_usuarios.html
│   ├── direccion/              # Management panel
│   │   ├── direccion_dashboard.html
│   │   ├── gestion_turnos.html
│   │   ├── notificaciones_cambios.html
│   │   └── ver_turnos_profesional.html
│   ├── profesional/            # Professional portal
│   │   ├── profesional_dashboard.html
│   │   ├── ver_cuadrante.html
│   │   ├── pedir_cambio.html
│   │   ├── solicitudes_cambio.html
│   │   ├── historico_cambios.html
│   │   └── cambiar_password.html
│   └── includes/               # Role-based navigation fragments
├── tests/                      # Unit/Integration test suite
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures and DB mocking
│   ├── test_admin.py
│   ├── test_direccion.py
│   ├── test_profesional.py
│   └── test_saliente_adjustment.py
└── docs/                       # Sprint and Design documentation
    ├── Sprint_1-4.md
    ├── Arquitectura.md
    └── Viabilidad_Tecnica.md
```

#### 5.1 Component Description

- **Project Root**: Contains global configuration files for Docker deployment and dependency management.
- **models/**: Implements persistence logic. MongoEngine is used to map Python objects to MongoDB documents, allowing for efficient paginated queries (e.g., user lists).
- **static/**: Organized into styles (CSS) following the Glassmorphism pattern and scripts (JS) handling real-time interactivity (polling).
- **templates/**: Divided by security areas (Admin, Management, Professional) to ensure permission integrity.
- **docker/**: Isolates network and server configuration, allowing for "infrastructure as code."
- **tests/**: Automated validations of all critical business rules, ensuring system robustness against changes.

---

### 6. Database Schema

#### 6.1 Entity-Relationship Diagram (ERD)

```mermaid
classDiagram
    class User {
        +String dni (PK)
        +String name
        +String category
        +String role
        +set_password(pass)
        +check_password(pass)
    }
    class Shift {
        +ObjectId id
        +ReferenceField professional
        +DateField date
        +String type
        +String workplace
    }
    class Swap {
        +ReferenceField professional1
        +ReferenceField professional2
        +DateField original_date
        +String status [Pending, Accepted, Rejected]
        +Boolean seen_by_direction
    }

    User "1" -- "*" Shift : assigned_to
    Shift "1" -- "0..1" Swap : swap_origin
    Swap "*" -- "2" User : involves
```

---

### 7. Production Deployment

The system uses a two-stage process for delivery:

#### 7.1 Automated Startup

The use of `docker_start.sh` is recommended for the initial deployment. This script ensures:

1. The existence of the `.env` file.
2. The generation of a cryptographically secure `SECRET_KEY` for Flask.
3. Automatic container orchestration.

#### 7.2 Image Architecture

1. **Build**: Generation of the Flask image based on `python:3.11-slim` to reduce the attack surface.
2. **Runtime**: Execution under Nginx with security configuration (request body size limitation, server version hiding).

---

### 8. Maintenance & Scalability

#### 8.1 Backup Strategy

The use of MongoDB's native backup engine is recommended:

```bash
docker exec mongo_guardias mongodump --uri="mongodb://root:pass@localhost:27017/guardias" --archive=/data/db/backup.archive
```

#### 8.2 Horizontal Scalability

Thanks to the _stateless_ design of the backend, multiple replicas of the `flask` service can be raised and load-balanced using the Nginx reverse proxy.

---

### 9. Security Protocols

#### 9.1 Implemented Protocols

- **In-Memory Data Protection**: Personal identifiers (DNI) are stored in the server's RAM as cryptographic hashes (SHA-256) within the active users tracking dictionary, preventing data leaks in case of memory dumps.
- **Authentication**: Secured login process through the detailed authentication flow:

```mermaid
sequenceDiagram
    participant U as User
    participant A as app.py
    participant B as MongoDB

    U->>A: Sends DNI + Password
    A->>B: Query User by DNI
    B-->>A: Returns Password Hash
    A->>A: werkzeug.check_password_hash()
    alt Valid Credentials
        A-->>U: Assigns Session Cookie + Redirect Dashboard
    else Invalid
        A-->>U: Returns Error + Flash Message
    end
```

---

### 10. Testing & Quality

A test suite based on `pytest` is implemented covering:

- **Unit Testing**: Individual validation of model methods.
- **Integration Testing**: Testing API routes simulating HTTP requests.
- **Mocking**: Total database isolation to ensure tests are idempotent and fast.

---

### 11. Troubleshooting

| Problem                    | Probable Cause                | Solution                     |
| :------------------------- | :---------------------------- | :--------------------------- |
| Error 502 Bad Gateway      | Flask/Gunicorn is not active  | `docker logs flask_guardias` |
| PDF generation failure     | Missing fields in Shift model | Check DB consistency         |
| Notifications not updating | JS polling error              | Check browser console (F12)  |

---

### 12. Annexes

#### 12.1 Shift Swap Sequence Diagram

```mermaid
sequenceDiagram
    participant P1 as Professional A
    participant P2 as Professional B
    participant S as Server
    participant D as HR/Direction

    P1->>S: Requests swap (P1_Shift <--> P2_Shift)
    S->>S: Validates labor rest rules
    S-->>P2: Notifies Request (Badge)
    P2->>S: Accepts Swap
    S->>S: Updates Shifts in DB
    S-->>D: Notifies Direction (Badge "New")
```

---

[Back to top / Volver al inicio](#top)
