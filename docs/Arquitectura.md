# Sistema de Gestión de Guardias y Cuadrantes  
## Documento de Arquitectura

Autor: **Cristóbal Fuentes Molina**  
Ciclo: **2º DAW**  
Proyecto: **Proyecto Intermodular**

---

## 1. Introducción

### 1.1. Propósito del sistema

El **Sistema de Gestión de Guardias y Cuadrantes** tiene como objetivo gestionar de forma centralizada:

- Los **cuadrantes de guardias y turnos** de profesionales sanitarios.
- Los **cambios de turno y guardia** entre profesionales.
- La **asignación automática de salientes** cuando el titular no está disponible.
- La **generación de informes diarios** en formato PDF.
- La **consulta de históricos** de cambios y cuadrantes.

El sistema está orientado a centros sanitarios donde participan **celadores**, **médicos/DUE**, **administración** y **dirección**.

---

### 1.2. Alcance

El sistema cubre:

- Gestión de cuadrantes diarios de profesionales.
- Gestión de turnos y guardias.
- Petición y aceptación de cambios de turno/guardia.
- Asignación automática de salientes según una lista ordenada.
- Consultas de profesionales por pueblos y centros.
- Generación de informes diarios en PDF.
- Consultas de históricos de cambios por rol.

No cubre:

- Gestión de nóminas.
- Gestión de vacaciones.
- Integración con otros sistemas externos (se asume standalone).

---

## 2. Actores del sistema

| Actor            | Descripción |
|------------------|-------------|
| **Celador**      | Gestiona turnos y cambios de turno. Consulta cuadrantes e históricos. |
| **Médico/DUE**   | Gestiona guardias y cambios de guardia. Consulta cuadrantes e históricos. |
| **Administración** | Consulta cuadrantes y profesionales de los pueblos. |
| **Dirección**    | Gestiona cuadrantes de profesionales, históricos y automatismos. |
| **Sistema**      | Ejecuta procesos automáticos (informes, asignación de salientes). |

---

## 3. Casos de uso

### 3.1. Listado de casos de uso

#### Casos comunes

| Código | Caso de uso                               |
|--------|--------------------------------------------|
| **UC1** | Consultar cuadrante                        |
| **UC2** | Consultar profesionales de los pueblos     |
| **UC3** | Consultar histórico de cambios             |

#### Celadores

| Código | Caso de uso                 | Notas |
|--------|------------------------------|-------|
| **UC4** | Pedir cambio de turno        | Deben pasar al menos **24h** entre guardias |
| **UC5** | Aceptar cambio de turno      | — |

#### Médicos / DUE

| Código | Caso de uso                  |
|--------|-------------------------------|
| **UC6** | Pedir cambio de guardia       |
| **UC7** | Aceptar cambio de guardia     |

#### Dirección

| Código | Caso de uso                                   |
|--------|------------------------------------------------|
| **UC8**  | Consultar cuadrante profesionales              |
| **UC9**  | Insertar cuadrante profesionales               |
| **UC10** | Modificar cuadrante profesionales              |
| **UC11** | Consultar histórico cambios celadores          |
| **UC12** | Consultar histórico cambios Médico/DUE         |

#### Sistema

| Código | Caso de uso                                  | Notas |
|--------|-----------------------------------------------|-------|
| **UC13** | Generar informe diario PDF profesionales       | Incluye UC1 |
| **UC14** | Asignar salientes automáticamente              | L–V no festivos; reparto equitativo (el que sale pasa al final) |

---

### 3.2. Relaciones entre actores y casos de uso

#### Celador

| Actor   | Caso de uso |
|---------|-------------|
| Celador | UC1 – Consultar cuadrante |
| Celador | UC2 – Consultar profesionales de los pueblos |
| Celador | UC3 – Consultar histórico cambios |
| Celador | UC4 – Pedir cambio de turno |
| Celador | UC5 – Aceptar cambio de turno |

#### Médico/DUE

| Actor   | Caso de uso |
|---------|-------------|
| Médico/DUE | UC1 – Consultar cuadrante |
| Médico/DUE | UC2 – Consultar profesionales de los pueblos |
| Médico/DUE | UC3 – Consultar histórico cambios |
| Médico/DUE | UC6 – Pedir cambio de guardia |
| Médico/DUE | UC7 – Aceptar cambio de guardia |

#### Administración

| Actor          | Caso de uso |
|----------------|-------------|
| Administración | UC1 – Consultar cuadrante |
| Administración | UC2 – Consultar profesionales de los pueblos |

#### Dirección

| Actor     | Caso de uso |
|-----------|-------------|
| Dirección | UC2 – Consultar profesionales de los pueblos |
| Dirección | UC8 – Consultar cuadrante profesionales |
| Dirección | UC9 – Insertar cuadrante profesionales |
| Dirección | UC10 – Modificar cuadrante profesionales |
| Dirección | UC11 – Consultar histórico cambios celadores |
| Dirección | UC12 – Consultar histórico cambios Médico/DUE |

---

### 3.3. Relaciones «include»

| Caso principal | Incluye | Motivo |
|----------------|---------|--------|
| **UC4** – Pedir cambio de turno | **UC5** – Aceptar cambio de turno | Validación del cambio |
| **UC6** – Pedir cambio de guardia | **UC7** – Aceptar cambio de guardia | Validación del cambio |
| **UC13** – Generar informe diario PDF profesionales | **UC1** – Consultar cuadrante | Necesita datos del cuadrante |
| **UC14** – Asignar salientes automáticamente | **UC1** – Consultar cuadrante | Necesita datos del cuadrante |

---

## 4. Modelo de datos

### 4.1. Entidades principales (MongoDB)

#### Profesional

- `_id: ObjectId`
- `dni: string` *(único)*
- `nombre: string`
- `apellidos: string`
- `categoria: string`
- `centro_asignado: string`
- `telefono: number`

#### Plan_Diario

- `_id: ObjectId`
- `nombre: string`
- `apellidos: string`
- `categoria: string`
- `centro: string`
- `telefono: number`

Relaciones:

- Un **Profesional** tiene varios **Plan_Diario**.
- Un **Plan_Diario** participa en uno o varios **Profesional**.

#### Turnos

- `_id: ObjectId`
- `profesional_id: ObjectId` *(ref Profesional)*
- `fecha: date`
- `tipo: string`

Reglas de negocio asociadas a `tipo`:

- `7h` → Consulta  
- `17h` → Solo guardia  
- `24h` → Festivo o Consulta+Guardia  

#### Cambios

- `_id: ObjectId`
- `profesional1_id: ObjectId` *(ref Profesional)*
- `profesional2_id: ObjectId` *(ref Profesional)*
- `fecha_original: date`
- `fecha_final: date`

Restricción:

- Los cambios solo se permiten entre **profesionales de la misma categoría**.

#### Salientes

- `_id: ObjectId`
- `profesional_id: ObjectId` *(ref Profesional)*
- `nombre: string`

Regla:

- Si el profesional titular no está disponible, se usa la **lista de salientes**.

---

### 4.2. Resumen de relaciones

- **Profesional 1..* Plan_Diario**
- **Profesional 1..* Turnos**
- **Profesional 1..* Cambios** (como profesional1 o profesional2)
- **Profesional 1..* Salientes**

---

## 5. Clases del sistema

### 5.1. Acceso a datos

#### MongoDBConnection

- `uri: string`
- `databaseName: string`
- `connect(): void`
- `getCollection(nombre: string)`
- `close(): void`

Responsabilidad: encapsular la conexión a la base de datos y la obtención de colecciones.

---

### 5.2. Clases de dominio

#### Profesional

- `DNI: string (PK)`
- `Nombre: string`
- `Apellidos: string`
- `Categoria: string`
- `CentroAsignado: string`
- `Telefono: string`

#### Plan_Diario

- `Nombre: string`
- `Apellidos: string`
- `Categoria: string`
- `Centro: string`
- `Telefono: string`

#### Cambios

- `DNI_Profesional1: string`
- `DNI_Profesional2: string`
- `Fecha_original: date`
- `Fecha_final: date`

#### Turnos

- `DNI_Profesional: string`
- `Fecha: date`
- `Tipo: string`

#### Salientes

- `DNI_Profesional: string`
- `Nombre: string`
- `Apellidos: string`
- `Telefono: string`

---

## 6. Reglas de negocio

1. **RB1 – Restricción de 24h entre guardias**  
   - Para que un celador, médico o DUE pueda **pedir cambio de turno/guardia**, deben haber pasado al menos **24 horas** entre guardias.

2. **RB2 – Cambios solo entre misma categoría**  
   - Los cambios de turno/guardia solo se permiten entre profesionales de la **misma categoría**.

3. **RB3 – Uso de lista de salientes**  
   - Si el profesional titular no está disponible, se recurre a la **lista de salientes**.

4. **RB4 – Lista de salientes ordenada**  
   - La lista de salientes es **ordenada**:  
     - El profesional que sale pasa al **final de la lista**.

5. **RB5 – Asignación automática de salientes**  
   - La asignación automática se realiza **solo de lunes a viernes no festivos**.
   - Se garantiza un **reparto equitativo** usando la lista ordenada.

6. **RB6 – Generación de informe diario**  
   - El sistema genera un **informe diario en PDF** con los profesionales y sus cuadrantes.
   - Este proceso incluye la consulta del cuadrante (UC1).

---

## 7. Arquitectura lógica

### 7.1. Capas

- **Capa de presentación**  
  - Interfaces para Celador, Médico/DUE, Administración y Dirección.
  - Formularios para petición/aceptación de cambios.
  - Vistas de cuadrantes, históricos y listados.

- **Capa de lógica de negocio**  
  - Validación de reglas de negocio (24h, misma categoría, lista de salientes).
  - Gestión de cambios de turno/guardia.
  - Generación de informes.
  - Asignación automática de salientes.

- **Capa de acceso a datos**  
  - Gestión de conexión a MongoDB.
  - CRUD sobre colecciones: Profesionales, Turnos, Cambios, Salientes, Plan_Diario.

---

## 8. Procesos clave

### 8.1. Proceso: Pedir cambio de turno (UC4)

1. El **Celador** consulta su cuadrante.
2. Selecciona el turno a cambiar.
3. El sistema verifica:
   - Que se cumplen las **24h entre guardias**.
   - Que el profesional con el que se intercambia es de la **misma categoría**.
4. Se registra la petición de cambio.
5. Se incluye el caso de uso **UC5 – Aceptar cambio de turno**.

---

### 8.2. Proceso: Asignar salientes automáticamente (UC14)

1. El sistema consulta el **cuadrante** (UC1).
2. Detecta profesionales no disponibles.
3. Consulta la **lista de salientes**.
4. Asigna el siguiente profesional de la lista.
5. Mueve al profesional asignado al **final de la lista**.
6. Solo se ejecuta **L–V no festivos**.

---

### 8.3. Proceso: Generar informe diario PDF (UC13)

1. El sistema consulta el **cuadrante** (UC1).
2. Genera un documento con:
   - Profesionales.
   - Turnos/guardias.
   - Centros asignados.
3. Exporta el resultado a **PDF**.
4. Deja el informe disponible para Dirección/Administración.

---

## 9. Conclusión

Este documento define la **arquitectura funcional y de datos** del Sistema de Gestión de Guardias y Cuadrantes:

- Se han descrito los **actores**, **casos de uso**, **reglas de negocio**, **modelo de datos** y **clases**.
- Se han detallado los **procesos clave**: cambios de turno, asignación de salientes e informes diarios.
- La arquitectura propuesta es adecuada para una implementación basada en **MongoDB** y una aplicación web modular.