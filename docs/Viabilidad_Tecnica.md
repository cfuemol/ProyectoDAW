# Plan de Viabilidad Técnica  
Cristóbal Fuentes Molina — 2º DAW — Proyecto Intermodular

---

## Estudio de Viabilidad Técnica

### I. Resumen

Este proyecto pretende dar solución a la problemática existente en los centros de salud respecto a qué personal está trabajando y dónde, facilitando su localización en caso de urgencia o emergencia.  
El documento indica que *“permitirá el cambio de guardia entre profesionales del mismo centro, llevando un registro pormenorizado de los mismos”*.

La APP está orientada a personal sanitario y destaca la importancia de automatizar rutinas de acción.

---

## II. Descripción del Proyecto

### A. Problema que la APP va a resolver

La APP busca reducir los retrasos en la localización de profesionales sanitarios, especialmente en zonas rurales donde los avisos del 061 requieren localizar rápidamente al personal.

El documento señala que *“muchos de estos profesionales no están fijos en un centro, sino que están en varios a lo largo de la mañana”*, lo que dificulta su localización.

También permitirá notificar cambios de guardia o ausencias en especialidades como fisioterapia, odontología o radiología.

---

### B. Funcionalidades principales

La APP permitirá:

- Realizar un cambio de guardia con otro compañero del mismo centro.
- Guardar el cambio cuando ambos profesionales lo acepten.
- Notificar el cambio al personal coordinador y a los profesionales implicados.
- Evitar guardias consecutivas, exigiendo 24h de descanso.
- Generar diariamente una tabla con los profesionales que están trabajando y su ubicación.

---

## III. Análisis Técnico

### A. Plataforma

- Web App accesible desde cualquier navegador.
- Tecnologías utilizadas: **HTML, CSS, JS, Docker, Python(Django)**.

### B. Arquitectura de Software

- **Backend:** Python
- **Frontend:** HTML, CSS, JS  
- **BBDD:** MongoDB (Pymongo mediante MongoDB-Express)  
- **API:** Django  
- **Despliegue:** Docker  
- **Automatizaciones:** n8n  
- **Control de versiones:** GitHub  

### C. Infraestructura y Hosting

- Proveedor en la nube: por determinar.
- No se requieren servidores propios.

### D. Seguridad y Privacidad

- Roles de usuario para controlar permisos.
- Contraseñas encriptadas con **SHA-256**.
- Conexiones mediante **HTTPS**.
- Se estudiará el cifrado adecuado para equilibrar seguridad y rendimiento.

---

## E. UX / UI

- Diseño moderno y minimalista.
- Prototipado con **Figma**.
- Pruebas de usabilidad con acceso temprano a usuarios.

---

## F. Estrategia de Testing

- Pruebas en dispositivos reales.
- Todos los errores se registrarán como bugs y se corregirán tras cada prueba.

---

## G. Mantenimiento y Operaciones

- Actualizaciones frecuentes para corregir bugs y añadir funcionalidades.
- Escalabilidad prevista: más centros y posible integración con la sala 061.

---

## IV. Costes Técnicos Estimados

- Aproximadamente **200 horas** de desarrollo.
- Infraestructura gratuita inicialmente.
- Todas las herramientas utilizadas son de código abierto (licencia GNU).

---

## V. Evaluación de Riesgos Técnicos

### A. Identificación de Riesgos

- Falta de tiempo para implementar todas las funcionalidades.
- Falta de destreza técnica en alguna parte del desarrollo.
- Problemas inesperados en despliegue o automatizaciones.

### B. Impacto y probabilidad

El documento indica que *“el impacto puede ser grave en el caso de problemas en el despliegue”*, aunque se confía en encontrar soluciones válidas.

### C. Planes de mitigación

- Priorizar que la APP funcione correctamente en los casos de uso principales.
- Resolver problemas secundarios una vez la base esté estable.

---

## VI. Cronograma Técnico

### A. Fases

- Gestión mediante **Jira**.
- Metodología ágil con sprints definidos.
- Plazos flexibles cuando sea necesario.

### B. Hitos principales

- Varias épicas configuradas para estructurar el trabajo.
- Cada épica contiene tareas con plazos distintos.

### C. Plazos estimados

- **5 semanas** por épica.
- **7 semanas** para la implementación técnica.

---

## VII. Conclusiones y Recomendaciones

Este estudio ha permitido poner en contexto tanto la parte técnica como la parte de organización para que el proyecto llegue a buen puerto.

Como recomendación para realizar la APP es necesario tener conocimiento de la idiosincrasia del objetivo a conseguir.

**El final ideal de esta APP sería que no sólo los centros de salud utilizaran la APP, sino que también la sala de coordinación del 061 hiciera lo mismo para mejorar la respuesta ante urgencias/emergencias.**

---