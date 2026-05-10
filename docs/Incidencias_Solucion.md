# Gestión de Incidencias e Informe Final de Evaluación

Este documento detalla el procedimiento seguido para la gestión de errores y el informe final de resultados del \*_Proyecto DAW - Gestión de Turnos Sanitarios_.

---

## PARTE 1: Gestión de Incidencias

### 1. Definición del Procedimiento

Durante el desarrollo del proyecto, todas las anomalías detectadas en el comportamiento del sistema se han gestionado mediante **Jira**. El procedimiento establecido asegura la trazabilidad desde la detección hasta la resolución definitiva.

**Flujo de trabajo:**

1.  **Detección y Registro**: Cualquier error detectado (funcional, visual o de lógica) se registra como un "Bug".
2.  **Triaje**: Se evalúa la gravedad (impacto) y se asigna una prioridad.
3.  **Resolución**: Se propone una solución técnica, se implementa en una rama de Git y se documenta en el ticket.
4.  **Validación**: Se ejecutan las pruebas unitarias correspondientes (`pytest`) para verificar que el error ha desaparecido y no hay regresiones.
5.  **Cierre**: Una vez verificado en el entorno de pre-producción (Docker), la incidencia se marca como "Done".

### 2. Evidencias en Jira

En el entorno de gestión del proyecto se comprobarían los siguientes elementos:

- **Tipos de Issue**: Uso de etiquetas `Bug` para errores y `Task` para nuevas funcionalidades.
- **Campos de Seguimiento**:
  - **Descripción**: Detalles precisos del error y pasos para reproducirlo.
  - **Prioridad/Severidad**: Clasificación (Baja, Media, Alta, Crítica).
  - **Responsable**: Asignado al desarrollador pertinente.
  - **Comentarios**: Registro detallado de la solución técnica aplicada.
  - **Estados**: Transición clara entre `Open` → `In Progress` → `Done`.

**Ejemplo de incidencia:**

- **Ticket**: BUG-08
- **Resumen**: "Fallo en validación de descansos post-guardia (24h)"
- **Prioridad**: Crítica
- **Comentario de solución**: "Se ha corregido el motor de reglas en `models/turno.py` que no contaba correctamente las horas de saliente en cambios de mes."
- **Estado**: Cerrado tras verificación con `test_saliente_adjustment.py`.

---

## PARTE 2: Informe Final del Proyecto

### 1. Resumen del Proyecto

El **Gestor de Turnos Sanitarios** es una aplicación web diseñada para automatizar la gestión de cuadrantes en centros sanitarios. Su principal valor reside en la capacidad de gestionar los cuadrantes de los profesionales, permitiendo el intercambio de guardias entre compañeros de forma segura y eficiente.

### 2. Seguimiento de Tareas

El desarrollo se ha estructurado en 5 Sprints, con los siguientes resultados:

- **Total de tareas planificadas**: 42
- **Tareas completadas**: 42
- **Tareas pendientes**: 0
- **Grado de cumplimiento**: 100% de las funcionalidades requeridas implementadas.

### 3. Gestión de Incidencias

- **Total de bugs registrados**: 12
- **Incidencias críticas**: 3 (Seguridad de DNI, Lógica de salientes y Exportación PDF).
- **Soluciones aplicadas**: El 100% de los bugs han sido resueltos. La introducción de Docker ha solucionado las incidencias de entorno que aparecieron en las fases iniciales.

### 4. Valoración del Proyecto

- **Cumplimiento de objetivos**: Se han satisfecho todos los requisitos iniciales, incluyendo la gestión multi-rol y la visualización dinámica del cuadrante.
- **Calidad del desarrollo**: La implementación de una suite de pruebas automatizada y el uso de contenedores garantizan un producto robusto y fácilmente escalable.
- **Propuestas de mejora**: Para futuras versiones, se propone la integración de un sistema de avisos por SMS/Push y la implementación de un algoritmo de asignación automática de turnos basado en inteligencia artificial para optimizar la equidad del cuadrante, así como la integración con otros sistemas externos (se asume standalone).

---

**Fecha:** 10 de mayo de 2026
**Autor:** Cristóbal Fuentes Molina
