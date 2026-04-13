# Guion de Exposición: Proyecto DAW - Gestión de Turnos Sanitarios

Este guion está diseñado para una presentación de aproximadamente 10-15 minutos. Cubre desde la problemática inicial hasta la solución técnica implementada.

---

## 1. Introducción y Contexto (2 min)
*   **Apertura**: "Buenos días. Mi nombre es Cristóbal Fuentes Molina y hoy voy a presentar mi proyecto final de DAW: una solución integral para la gestión de cuadrantes y turnos en entornos sanitarios."
*   **El Problema**: "En muchos centros de salud, la gestión de turnos se sigue haciendo de forma manual, en hojas de cálculo complejas o papel. Esto provoca:
    *   Errores en el cumplimiento de descansos legales (post-guardias).
    *   Dificultad para gestionar intercambios entre compañeros.
    *   Falta de información en tiempo real para el profesional."
*   **La Solución**: "He desarrollado una aplicación web que no solo digitaliza estos cuadrantes, sino que automatiza las reglas de descanso y ofrece una experiencia de usuario moderna y fluida."

## 2. Demostración Visual: La Interfaz (2 min)
*   **Diseño Glassmorphism**: "Lo primero que destaca es el diseño. He aplicado una estética **Glassmorphism** (efecto cristal). El objetivo no es solo que sea bonito, sino que la interfaz sea 'limpia', reduzca la fatiga visual de los usuarios y se sienta como una aplicación premium moderna."
*   **Responsive**: "La aplicación es totalmente responsive. Un médico puede consultar su próximo turno desde su móvil en el hospital con la misma facilidad que el director gestiona la plantilla desde su ordenador."

## 3. Funcionalidades por Roles (4 min)
*   **Administrador**: "El sistema se basa en tres niveles de acceso. El Admin se encarga de la configuración inicial, gestión de altas, bajas y control de permisos."
*   **Dirección (El Corazón del Control)**:
    *   "El director tiene una visión global del cuadrante."
    *   "Puede asignar turnos de forma masiva y modificar incidencias."
    *   "Genera listados diarios en PDF para saber exactamente quién está de guardia en cada centro."
*   **Profesional (Autonomía)**:
    *   "Cada profesional tiene su propio dashboard."
    *   "Puede solicitar intercambios de turno con otros compañeros de su misma categoría."
    *   "**Validación Automática**: El sistema no permite aceptar un cambio si alguno de los dos profesionales incumple el descanso obligatorio de 24 horas tras una guardia. El sistema 'piensa' por el usuario para evitar errores legales."

## 4. Características Técnicas Destacadas (3 min)
*   **Automatización de 'Salientes'**: "Cuando se asigna una guardia de 17h o 24h, el sistema detecta automáticamente que el profesional necesita un 'Saliente' al día siguiente (turno de 7h) y busca entre el personal disponible para cubrir ese hueco de forma equitativa."
*   **Real-Time**: "Mediante técnicas de *polling* dinámico, las notificaciones de cambios y el contador de usuarios online se actualizan sin necesidad de refrescar la página, mejorando la interactividad."
*   **Exportación**: "Los cuadrantes y listados de guardias se exportan a PDF de forma dinámica, facilitando la impresión y distribución física si fuera necesario."

## 5. El Stack Tecnológico y Calidad (2 min)
*   **Backend**: "He utilizado **Flask** por su flexibilidad y **MongoDB** como base de datos NoSQL, lo que permite manejar la flexibilidad de los turnos de forma mucho más natural que una base de datos relacional tradicional."
*   **Contenerización**: "El proyecto está totalmente montado sobre **Docker**. Con un solo comando, levantamos el servidor web (Gunicorn), la base de datos, el servidor proxy (Nginx) y la interfaz de gestión."
*   **Testing**: "Para garantizar que las reglas de descanso no fallen nunca, he desarrollado una suite de pruebas con **Pytest** que verifica automáticamente cada escenario crítico antes de cada despliegue."

## 6. Conclusión y Cierre (1 min)
*   **Resumen**: "En definitiva, Proyecto DAW es una herramienta que transforma un proceso administrativo caótico en un flujo de trabajo automatizado, seguro y estéticamente superior."
*   **Cierre**: "Muchas gracias por su atención. Quedo a su disposición para cualquier pregunta o para realizar una demostración en vivo de alguna funcionalidad específica."

---

### Consejos para la presentación:
1.  **Demo en vivo**: Ten abierto el navegador con tres pestañas (una por cada rol) para mostrar la fluidez entre ellos.
2.  **Muestra el PDF**: Genera un PDF en vivo, siempre impresiona ver cómo la web crea un documento formal en segundos.
3.  **Hitos**: Menciona que el sistema 'valida descansos' como tu mayor reto técnico resuelto.
