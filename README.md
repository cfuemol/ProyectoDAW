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
- **Gestión de Usuarios**: Registro, edición y eliminación de profesionales del sistema.
- **Control de Roles**: Asignación de permisos específicos (Admin, Dirección, Profesional).

#### 📋 Perfil de Dirección
- **Gestión de Turnos**: Creación y modificación manual de turnos para toda la plantilla.
- **Cuadrante Global**: Visualización completa del personal de servicio.
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

---

### 🛠️ Cómo usarlo

#### Requisitos previos
- Docker y Docker Compose (Recomendado) **o** Python 3.9+ y MongoDB.

#### Opción A: Despliegue con Docker (Recomendado)
Esta opción es la más rápida ya que configura automáticamente la base de datos, el servidor web (Nginx) y la aplicación Flask.

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/cfuemol/ProyectoDAW.git
   cd ProyectoDAW
   ```

2. **Configurar variables de entorno**:
   Asegúrate de que el archivo `.env` en la raíz contiene las credenciales deseadas (se proporciona uno por defecto para pruebas).

3. **Lanzar los contenedores**:
   ```bash
   docker-compose up -d --build
   ```

4. **Acceder a la aplicación**:
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

---

### 🔑 Usuarios por defecto (Pruebas)
- **Admin**: Acceso con DNI registrado (Contraseña: `admin`).
- **Profesionales/Dirección**: Acceso con DNI (Contraseña por defecto: `admin123`).

### ✍️ Autor
- **Cristóbal Fuentes Molina** - [Cfuemol](https://github.com/cfuemol)

---
*Este proyecto ha sido desarrollado como parte del ciclo formativo de Grado Superior en Desarrollo de Aplicaciones Web (DAW).*

[Volver al inicio / Back to top](#top)

---

<a id="english"></a>
## 🇬🇧 ENGLISH

This project is a comprehensive web application designed for managing shifts and schedules in healthcare environments. It facilitates coordination between health center management and medical professionals, assistants, and drivers, ensuring compliance with mandatory rest periods and streamlining shift swaps.

### 🚀 Description
The application offers a collaborative work environment with a modern interface based on **Glassmorphism**, optimized for both desktop and mobile viewing. It uses a robust backend with Flask and a NoSQL database (MongoDB) to handle complex shifts and professional relationships.

### ✨ Features

#### 👤 Administrator Profile
- **User Management**: Registration, editing, and deletion of professionals in the system.
- **Role Control**: Assignment of specific permissions (Admin, Direction, Professional).

#### 📋 Direction Profile
- **Shift Management**: Manual creation and modification of shifts for the entire staff.
- **Global Schedule**: Full visualization of all on-duty personnel.
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

---

### 🛠️ How to use it

#### Prerequisites
- Docker and Docker Compose (Recommended) **or** Python 3.9+ and MongoDB.

#### Option A: Deployment with Docker (Recommended)
This option is the fastest as it automatically configures the database, web server (Nginx), and the Flask application.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/cfuemol/ProyectoDAW.git
   cd ProyectoDAW
   ```

2. **Configure environment variables**:
   Ensure that the `.env` file in the root contains the desired credentials (a default one is provided for testing).

3. **Launch containers**:
   ```bash
   docker-compose up -d --build
   ```

4. **Access the application**:
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

---

### 🔑 Default Users (Testing)
- **Admin**: Access with registered DNI (Password: `admin`).
- **Professionals/Direction**: Access with DNI (Default password: `admin123`).

### ✍️ Author
- **Cristóbal Fuentes Molina** - [Cfuemol](https://github.com/cfuemol)

---
*This project has been developed as part of the Higher Education Vocational Training for Web Application Development (DAW).*

[Volver al inicio / Back to top](#top)