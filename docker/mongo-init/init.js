// ==========================================
//  AUTENTICACIÓN COMO ROOT
// ==========================================
db = db.getSiblingDB("admin");
db.auth(
    process.env.MONGO_INITDB_ROOT_USERNAME,
    process.env.MONGO_INITDB_ROOT_PASSWORD
);

// ==========================================
//  SELECCIONAR BASE DE DATOS GUARDIAS
// ==========================================
const guardias = db.getSiblingDB("guardias");

// ==========================================
//  COMPROBAR EXISTENCIA E INICIALIZAR
// ==========================================
const collections = guardias.getCollectionNames();

if (!collections.includes("usuarios")) {
    print("La colección 'usuarios' no existe. Creándola...");
    guardias.createCollection("usuarios");

    print("Insertando usuario administrador por defecto...");
    guardias.usuarios.insertOne({
        dni: "12345678Z",
        nombre: "Admin",
        apellidos: "Sistema",
        categoria: "Técnico Especialista en Informática",
        unidad_asignada: "SAS",
        centro_asignado: "Distrito Sanitario Granada Sur (SAS)",
        telefono: 600000000,
        email: "admin@correo.com",
        rol: "administrador",
        password_hash: "scrypt:32768:8:1$tKbt20hESy7HmJ0R$ebffa8324e053f125dca4a6ddcdc6f36c7c396f37f799c3b8e68d01769da00b5d84437ba6c38ce54646070bdd780d3d427992aa36b45b5dc7309af8860cb0dd4"
    });

    print("Insertando profesionales de prueba...");
    guardias.usuarios.insertMany([
        {
                "dni": "12345600M",
                "nombre": "Juan",
                "apellidos": "Garcia Lopez",
                "categoria": "Médico/a",
                "unidad_asignada": "ZBS Albuñol",
                "centro_asignado": "Albuñol",
                "telefono": 600000000,
                "email": "juan0@ejemplo.com",
                "rol": "direccion",
                "password_hash": "scrypt:32768:8:1$JmqKxZ4I7EjtnUCk$966d3415f1a098998a084375da8dab545d602b26eadcbb765df84ac6c7d98add1855b69215a67dd11a8bcd90c9c1b5065b1a0999045bae59f4cd2a741895366f"
        },
        {
                "dni": "12345601Y",
                "nombre": "Maria",
                "apellidos": "Martinez Ruiz",
                "categoria": "Médico/a",
                "unidad_asignada": "ZBS Albuñol",
                "centro_asignado": "Albondón",
                "telefono": 600000001,
                "email": "maria1@ejemplo.com",
                "rol": "profesional",
                "es_saliente": true,
                "password_hash": "scrypt:32768:8:1$JmqKxZ4I7EjtnUCk$966d3415f1a098998a084375da8dab545d602b26eadcbb765df84ac6c7d98add1855b69215a67dd11a8bcd90c9c1b5065b1a0999045bae59f4cd2a741895366f"
        },
        {
                "dni": "12345602F",
                "nombre": "Jose",
                "apellidos": "Fernandez Saez",
                "categoria": "Médico/a",
                "unidad_asignada": "ZBS Albuñol",
                "centro_asignado": "Alfornón",
                "telefono": 600000002,
                "email": "jose2@ejemplo.com",
                "rol": "profesional",
                "password_hash": "scrypt:32768:8:1$JmqKxZ4I7EjtnUCk$966d3415f1a098998a084375da8dab545d602b26eadcbb765df84ac6c7d98add1855b69215a67dd11a8bcd90c9c1b5065b1a0999045bae59f4cd2a741895366f"
        },
        {
                "dni": "12345603P",
                "nombre": "Ana",
                "apellidos": "Sanchez Gomez",
                "categoria": "Médico/a",
                "unidad_asignada": "ZBS Albuñol",
                "centro_asignado": "El Pozuelo",
                "telefono": 600000003,
                "email": "ana3@ejemplo.com",
                "rol": "profesional",
                "password_hash": "scrypt:32768:8:1$JmqKxZ4I7EjtnUCk$966d3415f1a098998a084375da8dab545d602b26eadcbb765df84ac6c7d98add1855b69215a67dd11a8bcd90c9c1b5065b1a0999045bae59f4cd2a741895366f"
        },
        {
                "dni": "12345604D",
                "nombre": "Luis",
                "apellidos": "Perez Martin",
                "categoria": "Médico/a",
                "unidad_asignada": "ZBS Albuñol",
                "centro_asignado": "La Rábita",
                "telefono": 600000004,
                "email": "luis4@ejemplo.com",
                "rol": "profesional",
                "password_hash": "scrypt:32768:8:1$JmqKxZ4I7EjtnUCk$966d3415f1a098998a084375da8dab545d602b26eadcbb765df84ac6c7d98add1855b69215a67dd11a8bcd90c9c1b5065b1a0999045bae59f4cd2a741895366f"
        },
        {
                "dni": "12345605X",
                "nombre": "Carmen",
                "apellidos": "Gomez Jimenez",
                "categoria": "DUE",
                "unidad_asignada": "ZBS Albuñol",
                "centro_asignado": "Los Castillas",
                "telefono": 600000005,
                "email": "carmen5@ejemplo.com",
                "rol": "profesional",
                "password_hash": "scrypt:32768:8:1$JmqKxZ4I7EjtnUCk$966d3415f1a098998a084375da8dab545d602b26eadcbb765df84ac6c7d98add1855b69215a67dd11a8bcd90c9c1b5065b1a0999045bae59f4cd2a741895366f"
        },
        {
                "dni": "12345606B",
                "nombre": "Carlos",
                "apellidos": "Martin Alvarez",
                "categoria": "DUE",
                "unidad_asignada": "ZBS Albuñol",
                "centro_asignado": "Polopos",
                "telefono": 600000006,
                "email": "carlos6@ejemplo.com",
                "rol": "profesional",
                "password_hash": "scrypt:32768:8:1$JmqKxZ4I7EjtnUCk$966d3415f1a098998a084375da8dab545d602b26eadcbb765df84ac6c7d98add1855b69215a67dd11a8bcd90c9c1b5065b1a0999045bae59f4cd2a741895366f"
        },
        {
                "dni": "12345607N",
                "nombre": "Isabel",
                "apellidos": "Jimenez Moreno",
                "categoria": "DUE",
                "unidad_asignada": "ZBS Albuñol",
                "centro_asignado": "Sorvilán",
                "telefono": 600000007,
                "email": "isabel7@ejemplo.com",
                "rol": "profesional",
                "es_saliente": true,
                "password_hash": "scrypt:32768:8:1$JmqKxZ4I7EjtnUCk$966d3415f1a098998a084375da8dab545d602b26eadcbb765df84ac6c7d98add1855b69215a67dd11a8bcd90c9c1b5065b1a0999045bae59f4cd2a741895366f"
        },
        {
                "dni": "12345608J",
                "nombre": "Antonio",
                "apellidos": "Ruiz Romero",
                "categoria": "DUE",
                "unidad_asignada": "ZBS Albuñol",
                "centro_asignado": "Albuñol",
                "telefono": 600000008,
                "email": "antonio8@ejemplo.com",
                "rol": "profesional",
                "password_hash": "scrypt:32768:8:1$JmqKxZ4I7EjtnUCk$966d3415f1a098998a084375da8dab545d602b26eadcbb765df84ac6c7d98add1855b69215a67dd11a8bcd90c9c1b5065b1a0999045bae59f4cd2a741895366f"
        },
        {
                "dni": "12345609Z",
                "nombre": "Laura",
                "apellidos": "Hernandez Navarro",
                "categoria": "DUE",
                "unidad_asignada": "ZBS Albuñol",
                "centro_asignado": "Albondón",
                "telefono": 600000009,
                "email": "laura9@ejemplo.com",
                "rol": "profesional",
                "password_hash": "scrypt:32768:8:1$JmqKxZ4I7EjtnUCk$966d3415f1a098998a084375da8dab545d602b26eadcbb765df84ac6c7d98add1855b69215a67dd11a8bcd90c9c1b5065b1a0999045bae59f4cd2a741895366f"
        },
        {
                "dni": "12345610S",
                "nombre": "Francisco",
                "apellidos": "Garcia Lopez",
                "categoria": "Celador/a-Conductor/a",
                "unidad_asignada": "ZBS Albuñol",
                "centro_asignado": "Alfornón",
                "telefono": 600000010,
                "email": "francisco10@ejemplo.com",
                "rol": "profesional",
                "password_hash": "scrypt:32768:8:1$JmqKxZ4I7EjtnUCk$966d3415f1a098998a084375da8dab545d602b26eadcbb765df84ac6c7d98add1855b69215a67dd11a8bcd90c9c1b5065b1a0999045bae59f4cd2a741895366f"
        },
        {
                "dni": "12345611Q",
                "nombre": "Elena",
                "apellidos": "Martinez Ruiz",
                "categoria": "Celador/a-Conductor/a",
                "unidad_asignada": "ZBS Albuñol",
                "centro_asignado": "El Pozuelo",
                "telefono": 600000011,
                "email": "elena11@ejemplo.com",
                "rol": "profesional",
                "password_hash": "scrypt:32768:8:1$JmqKxZ4I7EjtnUCk$966d3415f1a098998a084375da8dab545d602b26eadcbb765df84ac6c7d98add1855b69215a67dd11a8bcd90c9c1b5065b1a0999045bae59f4cd2a741895366f"
        },
        {
                "dni": "12345612V",
                "nombre": "Manuel",
                "apellidos": "Fernandez Saez",
                "categoria": "TCAE",
                "unidad_asignada": "ZBS Albuñol",
                "centro_asignado": "Albuñol",
                "telefono": 600000012,
                "email": "manuel12@ejemplo.com",
                "rol": "profesional",
                "password_hash": "scrypt:32768:8:1$JmqKxZ4I7EjtnUCk$966d3415f1a098998a084375da8dab545d602b26eadcbb765df84ac6c7d98add1855b69215a67dd11a8bcd90c9c1b5065b1a0999045bae59f4cd2a741895366f"
        },
        {
                "dni": "12345613H",
                "nombre": "Cristina",
                "apellidos": "Sanchez Gomez",
                "categoria": "Aux Administrativo/a",
                "unidad_asignada": "ZBS Albuñol",
                "centro_asignado": "Albuñol",
                "telefono": 600000013,
                "email": "cristina13@ejemplo.com",
                "rol": "profesional",
                "password_hash": "scrypt:32768:8:1$JmqKxZ4I7EjtnUCk$966d3415f1a098998a084375da8dab545d602b26eadcbb765df84ac6c7d98add1855b69215a67dd11a8bcd90c9c1b5065b1a0999045bae59f4cd2a741895366f"
        },
        {
                "dni": "12345614L",
                "nombre": "Miguel",
                "apellidos": "Perez Martin",
                "categoria": "Administrativo/a",
                "unidad_asignada": "ZBS Albuñol",
                "centro_asignado": "Albuñol",
                "telefono": 600000014,
                "email": "miguel14@ejemplo.com",
                "rol": "profesional",
                "password_hash": "scrypt:32768:8:1$JmqKxZ4I7EjtnUCk$966d3415f1a098998a084375da8dab545d602b26eadcbb765df84ac6c7d98add1855b69215a67dd11a8bcd90c9c1b5065b1a0999045bae59f4cd2a741895366f"
        },
        {
                "dni": "12345615C",
                "nombre": "Lucia",
                "apellidos": "Gomez Jimenez",
                "categoria": "Técnico/a de Rayos",
                "unidad_asignada": "ZBS Albuñol",
                "centro_asignado": "Albuñol",
                "telefono": 600000015,
                "email": "lucia15@ejemplo.com",
                "rol": "profesional",
                "password_hash": "scrypt:32768:8:1$JmqKxZ4I7EjtnUCk$966d3415f1a098998a084375da8dab545d602b26eadcbb765df84ac6c7d98add1855b69215a67dd11a8bcd90c9c1b5065b1a0999045bae59f4cd2a741895366f"
        },
        {
                "dni": "12345616K",
                "nombre": "Javier",
                "apellidos": "Martin Alvarez",
                "categoria": "Odontólogo/a",
                "unidad_asignada": "ZBS Albuñol",
                "centro_asignado": "Albuñol",
                "telefono": 600000016,
                "email": "javier16@ejemplo.com",
                "rol": "profesional",
                "password_hash": "scrypt:32768:8:1$JmqKxZ4I7EjtnUCk$966d3415f1a098998a084375da8dab545d602b26eadcbb765df84ac6c7d98add1855b69215a67dd11a8bcd90c9c1b5065b1a0999045bae59f4cd2a741895366f"
        },
        {
                "dni": "12345617E",
                "nombre": "Marta",
                "apellidos": "Jimenez Moreno",
                "categoria": "Trabajador/a Social",
                "unidad_asignada": "ZBS Albuñol",
                "centro_asignado": "Albuñol",
                "telefono": 600000017,
                "email": "marta17@ejemplo.com",
                "rol": "profesional",
                "password_hash": "scrypt:32768:8:1$JmqKxZ4I7EjtnUCk$966d3415f1a098998a084375da8dab545d602b26eadcbb765df84ac6c7d98add1855b69215a67dd11a8bcd90c9c1b5065b1a0999045bae59f4cd2a741895366f"
        },
        {
                "dni": "12345618T",
                "nombre": "David",
                "apellidos": "Ruiz Romero",
                "categoria": "Fisioterapeuta",
                "unidad_asignada": "ZBS Albuñol",
                "centro_asignado": "Albuñol",
                "telefono": 600000018,
                "email": "david18@ejemplo.com",
                "rol": "profesional",
                "password_hash": "scrypt:32768:8:1$JmqKxZ4I7EjtnUCk$966d3415f1a098998a084375da8dab545d602b26eadcbb765df84ac6c7d98add1855b69215a67dd11a8bcd90c9c1b5065b1a0999045bae59f4cd2a741895366f"
        },
        {
                "dni": "12345619R",
                "nombre": "Sonia",
                "apellidos": "Hernandez Navarro",
                "categoria": "Matrón/a",
                "unidad_asignada": "ZBS Albuñol",
                "centro_asignado": "Albuñol",
                "telefono": 600000019,
                "email": "sonia19@ejemplo.com",
                "rol": "profesional",
                "password_hash": "scrypt:32768:8:1$JmqKxZ4I7EjtnUCk$966d3415f1a098998a084375da8dab545d602b26eadcbb765df84ac6c7d98add1855b69215a67dd11a8bcd90c9c1b5065b1a0999045bae59f4cd2a741895366f"
        }
]);
    print("Inicialización de la base de datos completada.");
} else {
    print("La base de datos y la colección 'usuarios' ya existen. Se omite la inicialización.");
}
