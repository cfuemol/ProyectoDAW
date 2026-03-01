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
    print("Inicialización de la base de datos completada.");
} else {
    print("La base de datos y la colección 'usuarios' ya existen. Se omite la inicialización.");
}
