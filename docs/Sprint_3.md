# Sprint 3 — Arquitectura Tecnológica y Refactorización

## Documentación Sprint

En este sprint nos hemos centrado en la materialización de la arquitectura técnica, aplicando patrones de diseño profesionales y estrategias de separación de conceptos para garantizar un código mantenible, escalable y robusto.

---

## Arquitectura Tecnológica y Conexión

La aplicación se ha estructurado siguiendo un modelo cliente-servidor robusto bajo el patrón de separación de responsabilidades:

- **Frontend (Interfaz)**: Las vistas están desarrolladas mediante plantillas HTML renderizadas en servidor (Jinja2). Durante este Sprint se ha aplicado una **refactorización arquitectónica profunda**, logrando una separación absoluta de responsabilidades. Todo el diseño (UI _Glassmorphism_) está ahora desacoplado en archivos CSS independientes en `/static/css/`, y toda la lógica reactiva y asíncrona se encuentra en módulos estrictos de JavaScript en `/static/scripts/`. En esta capa se asegura una mantenibilidad escalable y se evita el "código espagueti".

- **Backend (Servidor)**: Desarrollado en Python bajo un entorno web ligero (Flask), la capa Backend funciona como el orquestador principal. Procesa las rutas HTTP requeridas por el navegador, valida de forma segura y estricta las reglas de negocio (ej. validaciones de mínimo 24h de descanso entre guardias, o permisos condicionales por rol), renderiza las plantillas iniciales y sirve de puerta de enlace en tiempo real para nuestra API interna.

- **Base de Datos (BBDD)**: Se ha apoyado toda la estructura sobre un sistema NoSQL documental como **MongoDB**. Dada la variabilidad de horarios y rotaciones atípicas inherentes a los profesionales sanitarios, este modelo nos aporta un lienzo en blanco permitiendo un almacenamiento sin esquemas estrictos (_schema-less_), mejorando considerablemente el rendimiento y la facilidad de lecturas cruzadas entre colecciones sin las penalizaciones de las uniones relacionales rígidas (colecciones: `Profesionales`, `Turnos`, `Cambios` y `Salientes`).

- **Interconexión (El Flujo de Datos)**: La interconexión se traza como un flujo fluido bidireccional. El Frontend reacciona a los eventos semánticos desencadenados por el personal sanitario (guardado de lotes calendarios, selecciones de usuario...) y lanza llamadas de red (usando asincronía con `Fetch API`) solicitando acciones y validaciones al servidor. El Backend escrito en Python ataja la llamada, cruza la lógica invocando la capa del MongoDB, y le devuelve una serialización estructurada en formato JSON al navegador. Como fase final, los scripts desvinculados de JavaScript manipulan discretamente el DOM insertando los reajustes visuales (validaciones, alertas visuales de feedback...) en milisegundos _sin tener que interrumpir la usabilidad recargando toda la ventana de nuevo._

> En este sprint se ha conseguido una separación absoluta de responsabilidades, logrando una arquitectura escalable y mantenible. Además se ha mejorado la experiencia de usuario al implementar una interfaz más intuitiva y responsive. Esto permite una mejor gestión de los turnos y una mayor satisfacción de los usuarios.

> Además ha permitido la creación de lógica avanzada para la generación de usuarios, gestión de turnos y gestión de cambios, lo que permite una mayor eficiencia y productividad en el trabajo diario.
