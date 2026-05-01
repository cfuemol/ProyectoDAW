<a id="top"></a>

# Proyecto DAW - Gestión de Turnos y Cuadrantes Sanitarios / Healthcare Shift Management System

---

**Idiomas / Languages:**

- [Español](#español) 🇪🇸
- [English](#english) 🇬🇧

---

<a id="español"></a>

## 🇪🇸 ESPAÑOL

Este proyecto es una aplicación web integral diseñada para la gestión de turnos y cuadrantes en entornos sanitarios. Facilita la coordinación entre la dirección de los centros de salud y los profesionales médicos, auxiliares y conductores, asegurando el cumplimiento de los descansos obligatorios y agilizando el intercambio de turnos.

### 🚀 Descripción

La aplicación ofrece un entorno de trabajo colaborativo con una interfaz moderna basada en **Glassmorphism**, optimizada para visualización tanto en escritorio como en dispositivos móviles. Utiliza un backend robusto con Flask y una base de datos NoSQL (MongoDB) para manejar turnos complejos y relaciones entre profesionales.

### ✨ Funcionalidades

#### 👤 Perfil del Administrador

- **Gestión de Usuarios**: Registro, edición y eliminación de profesionales del sistema, con listados paginados.
- **Control de Roles**: Asignación de permisos específicos (Admin, Dirección, Profesional).

#### 📋 Perfil de Dirección

- **Gestión de Turnos**: Creación y modificación manual de turnos para toda la plantilla.
- **Cuadrante Global e Individual**: Visualización completa del personal de servicio diario y acceso a los cuadrantes individuales filtrados por mes de cualquier profesional.
- **Notificaciones**: Supervisión de los intercambios de turno realizados entre profesionales.
- **Reportes PDF**: Generación de listados diarios de personal de guardia.

#### 🏥 Perfil del Profesional

- **Dashboard Personal**: Resumen de turnos próximos y actividad reciente.
- **Cuadrante Interactivo**: Calendario mensual con detalles del centro de trabajo y tipo de turno.
- **Intercambio de Turnos**: Sistema de solicitudes para pedir cambios a compañeros de la misma categoría, con validación automática de descansos legales.
- **Exportación**: Descarga del cuadrante mensual personal en formato PDF.

#### 🛠️ Características Técnicas

- **Diseño Real-time**: Polling dinámico para actualizar notificaciones y usuarios conectados sin recargar la página.
- **Responsive Design**: Interfaz adaptada a móviles con navegación intuitiva.
- **Validación Automática**: Motor de reglas para asegurar descansos post-guardia y equidad en salientes.
- **Seguridad en Memoria**: Hashing criptográfico (SHA-256) de los identificadores de sesión (DNI) para proteger el registro de usuarios activos en memoria RAM.

---

### 🛠️ Cómo usarlo

#### Requisitos previos

- Docker y Docker Compose (Recomendado) **o** Python 3.9+ y MongoDB.

#### Opción A: Lanzar el proyecto (Recomendado)

Este método configura automáticamente las variables de entorno (`.env`), genera una clave de seguridad única y levanta los contenedores en un solo paso.

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/cfuemol/ProyectoDAW.git
   cd ProyectoDAW
   ```

2. **Ejecutar el script de inicio**:

   ```bash
   bash docker_start.sh
   ```

3. **Acceder a la aplicación**:
   Abre tu navegador en `http://localhost`.

#### Opción B: Instalación Local (Desarrollo)

Si prefieres ejecutarlo sin Docker:

1. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar MongoDB**:
   Asegúrate de tener MongoDB en ejecución localmente.

3. **Ejecutar la aplicación**:
   ```bash
   python app.py
   ```
   Acceso en `http://127.0.0.1:5000`.

### 🧪 Pruebas Automatizadas

El proyecto incluye una suite de pruebas exhaustiva para verificar la integridad de la lógica de negocio, el cumplimiento de descansos legales y el correcto ajuste de los turnos de saliente.

Para ejecutar todas las pruebas de forma automática:

```bash
bash run_tests.sh
```

También puedes ejecutarlas manualmente usando `pytest` dentro del entorno virtual:

```bash
./.venv/bin/pytest
```

---

### 🔑 Usuarios por defecto (Pruebas)

- **Admin**: Acceso con DNI registrado (`12345678A`) (Contraseña: `admin`).
- **Profesionales/Dirección**: Acceso con DNI (Contraseña por defecto: `admin123`).
- **Mongo_Express**: Acceso con usuario `admin` (Contraseña: `pass`).

### ✍️ Autor

- **Cristóbal Fuentes Molina** - [Cfuemol](https://github.com/cfuemol)

---

_Este proyecto ha sido desarrollado como parte del ciclo formativo de Grado Superior en Desarrollo de Aplicaciones Web (DAW)._

[Volver al inicio / Back to top](#top)

---

<a id="english"></a>

## 🇬🇧 ENGLISH

This project is a comprehensive web application designed for managing shifts and schedules in healthcare environments. It facilitates coordination between health center management and medical professionals, assistants, and drivers, ensuring compliance with mandatory rest periods and streamlining shift swaps.

### 🚀 Description

The application offers a collaborative work environment with a modern interface based on **Glassmorphism**, optimized for both desktop and mobile viewing. It uses a robust backend with Flask and a NoSQL database (MongoDB) to handle complex shifts and professional relationships.

### ✨ Features

#### 👤 Administrator Profile

- **User Management**: Registration, editing, and deletion of professionals in the system, with paginated lists.
- **Role Control**: Assignment of specific permissions (Admin, Direction, Professional).

#### 📋 Direction Profile

- **Shift Management**: Manual creation and modification of shifts for the entire staff.
- **Global & Individual Schedule**: Full visualization of all on-duty personnel and access to individual monthly schedules for any professional.
- **Notifications**: Supervision of shift swaps carried out between professionals.
- **PDF Reports**: Generation of daily lists of on-call personnel.

#### 🏥 Professional Profile

- **Personal Dashboard**: Summary of upcoming shifts and recent activity.
- **Interactive Schedule**: Monthly calendar with details of the workplace and shift type.
- **Shift Swaps**: Request system to ask for swaps from colleagues in the same category, with automatic validation of legal rest periods.
- **Export**: Download personal monthly schedule in PDF format.

#### 🛠️ Technical Specifications

- **Real-time Design**: Dynamic polling to update notifications and online users without refreshing the page.
- **Responsive Design**: Mobile-adapted interface with intuitive navigation.
- **Automatic Validation**: Rules engine to ensure post-guard rest and equity in relief assignments (salientes).
- **In-Memory Security**: Cryptographic hashing (SHA-256) of session identifiers (DNI) to protect the active users register in RAM.

---

### 🛠️ How to use it

#### Prerequisites

- Docker and Docker Compose (Recommended) **or** Python 3.9+ and MongoDB.

#### Option A: Launching the project (Recommended)

This method automatically configures the environment variables (`.env`), generates a unique security key, and spins up the containers in one simple step.

1. **Clone the repository**:

   ```bash
   git clone https://github.com/cfuemol/ProyectoDAW.git
   cd ProyectoDAW
   ```

2. **Run the startup script**:

   ```bash
   bash docker_start.sh
   ```

3. **Access the application**:
   Open your browser at `http://localhost`.

#### Option B: Local Installation (Development)

If you prefer to run it without Docker:

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure MongoDB**:
   Ensure you have MongoDB running locally.

3. **Run the application**:
   ```bash
   python app.py
   ```
   Access at `http://127.0.0.1:5000`.

### 🧪 Automated Testing

The project includes a comprehensive test suite to verify business logic integrity, compliance with legal rest periods, and the correct adjustment of relief (salientes) shifts.

To run all tests automatically:

```bash
bash run_tests.sh
```

You can also run them manually using `pytest` within the virtual environment:

```bash
./.venv/bin/pytest
```

---

### 🔑 Default Users (Testing)

- **Admin**: Access with registered DNI (`12345678A`) (Password: `admin`).
- **Professionals/Direction**: Access with DNI (Default password: `admin123`).
- **Mongo_Express**: Access with username `admin` (Password: `pass`).

### ✍️ Author

- **Cristóbal Fuentes Molina** - [Cfuemol](https://github.com/cfuemol)

---

_This project has been developed as part of the Higher Education Vocational Training for Web Application Development (DAW)._

[Volver al inicio / Back to top](#top)
