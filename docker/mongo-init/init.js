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
        password_hash: "scrypt:32768:8:1$0bBPS7GwA4T3zBdb$3de5478d0cb14b501bcbeacf4be972e25f4a18ee433d2df9be5f5679a1944c6dc04f5fafbd468d0f68909dad196d43b7ead1122a46e68368efb301b67b80a678"
    });

    print("Insertando profesionales de prueba...");
    guardias.usuarios.insertMany([
        // --- ALBUÑOL (23 profesionales) ---
        // Médicos (4)
        { "dni": "12345600M", "nombre": "Juan", "apellidos": "Garcia Lopez", "categoria": "Médico/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000000, "email": "juan0@ejemplo.com", "rol": "direccion", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345601A", "nombre": "Pedro", "apellidos": "Ruiz Gomez", "categoria": "Médico/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000001, "email": "pedro1@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345602S", "nombre": "Marta", "apellidos": "Sanz Lopez", "categoria": "Médico/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000002, "email": "marta2@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345603D", "nombre": "Luis", "apellidos": "Diaz Martos", "categoria": "Médico/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000003, "email": "luis3@ejemplo.com", "rol": "profesional", "es_saliente": true, "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        // DUE (4)
        { "dni": "12345608J", "nombre": "Antonio", "apellidos": "Ruiz Romero", "categoria": "DUE", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000008, "email": "antonio8@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345609F", "nombre": "Lucia", "apellidos": "Fernandez Sanz", "categoria": "DUE", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000009, "email": "lucia9@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345610G", "nombre": "Jorge", "apellidos": "Gomez Ruiz", "categoria": "DUE", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000010, "email": "jorge10@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345611H", "nombre": "Elena", "apellidos": "Hernandez Sanz", "categoria": "DUE", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000011, "email": "elena11@ejemplo.com", "rol": "profesional", "es_saliente": true, "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        // Celadores (5)
        { "dni": "12345622C", "nombre": "Francisco", "apellidos": "Castro Lopez", "categoria": "Celador/a-Conductor/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000022, "email": "fc22@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345623B", "nombre": "Beatriz", "apellidos": "Blanco Diaz", "categoria": "Celador/a-Conductor/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000023, "email": "bb23@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345624V", "nombre": "Victor", "apellidos": "Velez Martin", "categoria": "Celador/a-Conductor/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000024, "email": "vv24@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345625X", "nombre": "Xavier", "apellidos": "Ximenez Ruiz", "categoria": "Celador/a-Conductor/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000025, "email": "xx25@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345626Y", "nombre": "Yolanda", "apellidos": "Yebra Sanz", "categoria": "Celador/a-Conductor/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000026, "email": "yy26@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        // TCAE (2)
        { "dni": "12345627T", "nombre": "Tomas", "apellidos": "Torres Soler", "categoria": "TCAE", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000027, "email": "tt27@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345628U", "nombre": "Ursula", "apellidos": "Urbano Sanz", "categoria": "TCAE", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000028, "email": "uu28@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        // Auxiliar Administrativo (2)
        { "dni": "12345629A", "nombre": "Ana", "apellidos": "Alonso Rico", "categoria": "Aux Administrativo/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000029, "email": "aa29@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345630B", "nombre": "Borja", "apellidos": "Benitez Sol", "categoria": "Aux Administrativo/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000030, "email": "bb30@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        // Otras categorías (1 de cada)
        { "dni": "12345631C", "nombre": "Clara", "apellidos": "Calvo Ruiz", "categoria": "Administrativo/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000031, "email": "cc31@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345632D", "nombre": "Diego", "apellidos": "Duarte Martos", "categoria": "Técnico/a de Rayos", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000032, "email": "dd32@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345633E", "nombre": "Eva", "apellidos": "Espinosa Sanz", "categoria": "Odontólogo/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000033, "email": "ee33@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345634F", "nombre": "Felipe", "apellidos": "Franco Martos", "categoria": "Trabajador/a Social", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000034, "email": "ff34@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345635G", "nombre": "Gema", "apellidos": "Gallego Ruiz", "categoria": "Fisioterapeuta", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000035, "email": "gg35@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345636H", "nombre": "Hugo", "apellidos": "Heredia Martos", "categoria": "Matrón/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albuñol", "telefono": 600000036, "email": "hh36@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },

        // --- RESTO DE CENTROS (1 M + 1 D cada uno) ---
        // Albondón
        { "dni": "12345604Z", "nombre": "Maria", "apellidos": "Martinez Ruiz", "categoria": "Médico/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albondón", "telefono": 600000004, "email": "maria4@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345612K", "nombre": "Laura", "apellidos": "Hernandez Navarro", "categoria": "DUE", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Albondón", "telefono": 600000012, "email": "laura12@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        // Alfornón
        { "dni": "12345605X", "nombre": "Jose", "apellidos": "Fernandez Saez", "categoria": "Médico/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Alfornón", "telefono": 600000005, "email": "jose5@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345613L", "nombre": "Carlos", "apellidos": "Martin Alvarez", "categoria": "DUE", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Alfornón", "telefono": 600000013, "email": "carlos13@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        // El Pozuelo
        { "dni": "12345606B", "nombre": "Ana", "apellidos": "Sanchez Gomez", "categoria": "Médico/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "El Pozuelo", "telefono": 600000006, "email": "ana6@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345614N", "nombre": "Isabel", "apellidos": "Jimenez Moreno", "categoria": "DUE", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "El Pozuelo", "telefono": 600000014, "email": "isabel14@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        // La Rábita
        { "dni": "12345607P", "nombre": "Luis", "apellidos": "Perez Martin", "categoria": "Médico/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "La Rábita", "telefono": 600000007, "email": "luis7@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345615V", "nombre": "Victor", "apellidos": "Velez Martin", "categoria": "DUE", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "La Rábita", "telefono": 600000015, "email": "victor15@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        // Los Castillas
        { "dni": "12345616Q", "nombre": "Carmen", "apellidos": "Gomez Jimenez", "categoria": "Médico/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Los Castillas", "telefono": 600000016, "email": "carmen16@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345617W", "nombre": "Isabel", "apellidos": "Jimenez Moreno", "categoria": "DUE", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Los Castillas", "telefono": 600000017, "email": "isabel17@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        // Polopos
        { "dni": "12345618E", "nombre": "David", "apellidos": "Ruiz Romero", "categoria": "Médico/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Polopos", "telefono": 600000018, "email": "david18@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345619R", "nombre": "Sonia", "apellidos": "Hernandez Navarro", "categoria": "DUE", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Polopos", "telefono": 600000019, "email": "sonia19@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        // Sorvilán
        { "dni": "12345620T", "nombre": "Daniel", "apellidos": "Diaz Martos", "categoria": "Médico/a", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Sorvilán", "telefono": 600000020, "email": "daniel20@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" },
        { "dni": "12345621Y", "nombre": "Yolanda", "apellidos": "Yebra Sanz", "categoria": "DUE", "unidad_asignada": "ZBS Albuñol", "centro_asignado": "Sorvilán", "telefono": 600000021, "email": "yolanda21@ejemplo.com", "rol": "profesional", "password_hash": "scrypt:32768:8:1$oDUHkKZDsjsGEM8z$ddeec511af1ff18bf5cab490c5470bbb54d4c6ddabc5efd3a194fe8939bb9c3960a13eb51602dd7f183df6b5facd46598d7d56e71e5798b9ee1c18d77b35ea96" }
    ]);

    print("Inicialización de la base de datos completada.");
} else {
    print("La base de datos y la colección 'usuarios' ya existen. Se omite la inicialización.");
}
