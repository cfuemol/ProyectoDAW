# Sprint 5: Pruebas y Contenerización

Este documento resume los avances realizados durante el Sprint 5, centrándose en la calidad del software mediante pruebas unitarias y la facilidad de despliegue mediante la contenerización con Docker.

## 1. Pruebas Unitarias

Se ha implementado una robusta suite de pruebas utilizando **Pytest** para asegurar la integridad de las funciones críticas del sistema. Las pruebas están organizadas en diferentes archivos para cubrir las funcionalidades específicas de cada rol y la lógica de negocio compleja.

### Cobertura de Pruebas
- **`test_admin.py`**: Verifica las capacidades de gestión de usuarios por parte del administrador, incluyendo el registro, edición y borrado, asegurando que las restricciones de rol se cumplan.
- **`test_direccion.py`**: Centrado en la gestión de turnos y visualización de cuadrantes, validando que el personal de dirección pueda asignar turnos respetando las reglas de la unidad.
- **`test_profesional.py`**: Prueba las funcionalidades para el personal sanitario, como la visualización de sus propios turnos, el cambio de contraseña y la solicitud de intercambio de turnos con compañeros.
- **`test_saliente_adjustment.py`**: Valida la lógica automática de asignación de salientes (descansos post-guardia), asegurando que se cumplan los periodos de descanso obligatorios tras una guardia de 17h o 24h.

### Automatización
Se ha incluido el script `run_tests.sh`, que automatiza la configuración del entorno necesario y la ejecución de todas las pruebas, proporcionando una salida clara sobre el estado del sistema.

---

## 2. Contenerización con Docker

El proyecto ha sido completamente contenerizado para garantizar un entorno de ejecución consistente y facilitar su despliegue en cualquier sistema sin conflictos de dependencias.

### Arquitectura de Microservicios
Se ha utilizado **Docker Compose** para orquestar los siguientes servicios:
- **`flask`**: El núcleo de la aplicación web, ejecutándose sobre Gunicorn para un rendimiento de producción.
- **`mongodb`**: Base de datos NoSQL que almacena toda la información de usuarios, turnos y cambios.
- **`nginx`**: Servidor proxy inverso que gestiona las peticiones externas y sirve de puerta de enlace segura hacia la aplicación Flask.
- **`mongo-express`**: Interfaz web para la administración visual de la base de datos MongoDB durante el desarrollo.

### Gestión de Configuración
- Se utiliza un archivo `.env` para centralizar todas las variables críticas (credenciales de BD, llaves secretas, puertos), permitiendo una configuración flexible sin modificar el código.
- Los archivos de configuración de Docker y Nginx se encuentran organizados en el directorio `/docker`.

### Despliegue Rápido
El script `docker_start.sh` permite levantar todo el ecosistema con un solo comando, encargándose de construir las imágenes e iniciar los contenedores necesarios.
