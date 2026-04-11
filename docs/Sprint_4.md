# Sprint 4: Documentación e Internacionalización

## 📋 Resumen del Sprint
Este sprint se ha centrado en profesionalizar la documentación del proyecto, asegurar la arquitectura mediante variables de entorno y facilitar la adopción global mediante un sistema bilingüe completo (Español/Inglés).

---

## 🚀 Hitos Alcanzados

### 1. Internacionalización (i18n)
- **Documentación Bilingüe**: Se ha implementado un sistema de navegación mediante anclas en todos los archivos Markdown principales, permitiendo alternar entre Español 🇪🇸 e Inglés 🇬🇧.
- **Archivos Cubiertos**:
    - `README.md`
    - `manual_tecnico.md`
    - `manual_usuario.md`

### 2. Manual de Usuario (Ilustrado)
- **Guía por Roles**: Instrucciones específicas para Administradores, Dirección y Profesionales.
- **Material Visual**: Integración de 10+ capturas de pantalla reales que ilustran:
    - Proceso de Login (DNI/NIE).
    - Dashboard dinámico y contador de usuarios online.
    - Gestión de cuadrantes y exportación a PDF.
    - Intercambio de turnos con validaciones legales.
    - Notificaciones en tiempo real para dirección.

### 3. Manual Técnico
- **Arquitectura**: Documentación detallada del stack tecnológico (Flask, MongoDB, Nginx, Docker).
- **Diagramas Mermaid**: Inclusión de diagramas de arquitectura, flujo de autenticación y relaciones de base de datos.
- **Seguridad**: Detalle sobre la gestión de secretos y configuración del entorno.

### 4. Seguridad y Despliegue
- **Secret Management**: Migración de configuraciones sensibles a un archivo `.env` externo.
- **SECRET_KEY**: Generación de una clave criptográfica segura de 64 caracteres.
- **Docker Compose**: Sincronización de variables de entorno entre el host y el contenedor Flask.

### 5. Mejoras en la Interfaz (UI/UX)
- **Real-time Badges**: Implementación de polling para notificaciones y solicitudes de cambio sin recarga de página.
- **Nomenclatura**: Adaptación de la interfaz para soportar tanto DNI como NIE.
- **Visuales**: Refuerzo del estilo *Glassmorphism* en componentes de navegación y cards.

---

## 🛠️ Entregables Técnicos
- [x] **README.md**: Central de bienvenida y guía de inicio rápido.
- [x] **manual_tecnico.md**: Referencia para desarrolladores y administradores de sistemas.
- [x] **manual_usuario.md**: Herramienta de capacitación para el personal sanitario.
- [x] **.env**: Configuración de seguridad centralizada.

---
**Sprint Finalizado con éxito.**
*Responsable: Cristóbal Fuentes Molina*
