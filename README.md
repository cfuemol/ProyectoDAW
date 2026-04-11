# Proyecto DAW - Gestión de Turnos y Cuadrantes Sanitarios

Este proyecto es una aplicación web integral diseñada para la gestión de turnos y cuadrantes en entornos sanitarios. Facilita la coordinación entre la dirección de los centros de salud y los profesionales médicos, auxiliares y conductores, asegurando el cumplimiento de los descansos obligatorios y agilizando el intercambio de turnos.

## 🚀 Descripción

La aplicación ofrece un entorno de trabajo colaborativo con una interfaz moderna basada en **Glassmorphism**, optimizada para visualización tanto en escritorio como en dispositivos móviles. Utiliza un backend robusto con Flask y una base de datos NoSQL (MongoDB) para manejar turnos complejos y relaciones entre profesionales.

## ✨ Funcionalidades

### 👤 Perfil del Administrador
- **Gestión de Usuarios**: Registro, edición y eliminación de profesionales del sistema.
- **Control de Roles**: Asignación de permisos específicos (Admin, Dirección, Profesional).

### 📋 Perfil de Dirección
- **Gestión de Turnos**: Creación y modificación manual de turnos para toda la plantilla.
- **Cuadrante Global**: Visualización completa del personal de servicio.
- **Notificaciones**: Supervisión de los intercambios de turno realizados entre profesionales.
- **Reportes PDF**: Generación de listados diarios de personal de guardia.

### 🏥 Perfil del Profesional
- **Dashboard Personal**: Resumen de turnos próximos y actividad reciente.
- **Cuadrante Interactivo**: Calendario mensual con detalles del centro de trabajo y tipo de turno.
- **Intercambio de Turnos**: Sistema de solicitudes para pedir cambios a compañeros de la misma categoría, con validación automática de descansos legales.
- **Exportación**: Descarga del cuadrante mensual personal en formato PDF.

### 🛠️ Características Técnicas
- **Diseño Real-time**: Polling dinámico para actualizar notificaciones y usuarios conectados sin recargar la página.
- **Responsive Design**: Interfaz adaptada a móviles con navegación intuitiva.
- **Validación Automática**: Motor de reglas para asegurar descansos post-guardia y equidad en salientes.

## 🛠️ Cómo usarlo

### Requisitos previos
- Docker y Docker Compose (Recomendado) **o** Python 3.9+ y MongoDB.

### Opción A: Despliegue con Docker (Recomendado)
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

### Opción B: Instalación Local (Desarrollo)
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

### Usuarios por defecto (Pruebas)
- **Admin**: Acceso con DNI registrado (Contraseña: `admin`).
- **Profesionales/Dirección**: Acceso con DNI (Contraseña por defecto: `admin123`).

## ✍️ Autor

- **Cristóbal Fuentes Molina** - [Cfuemol](https://github.com/cfuemol)

---
*Este proyecto ha sido desarrollado como parte del ciclo formativo de Grado Superior en Desarrollo de Aplicaciones Web (DAW).*