document.addEventListener("DOMContentLoaded", function() {
  const rolSelect = document.getElementById("rol");
  const categoriaSelect = document.getElementById("categoria");
  const unidadAsignadaSelect = document.getElementById("unidad_asignada");
  const centroAsignadoSelect = document.getElementById("centro_asignado");

  //* Leer variable dinámica inyectada desde Jinja
  const form = document.querySelector("form");
  const sessionRol = form.getAttribute("data-session-rol");

  const ADMIN_CAT = "Técnico Especialista en Informática";
  const ADMIN_UNIDAD = "SAS";
  const ADMIN_CENTRO = "Distrito Sanitario Granada Sur (SAS)";

  function updateAdminFields() {
    const isDireccion = sessionRol === "direccion";

    //* Limpiar opciones previas si no es admin
    if (rolSelect.value !== "administrador") {
      Array.from(categoriaSelect.options).forEach((opt) => {
        if (opt.value === ADMIN_CAT) opt.remove();
      });

      //* Si no es admin y el rol actual es Dirección, también quitamos SAS y Distrito
      Array.from(unidadAsignadaSelect.options).forEach((opt) => {
        if (opt.value === ADMIN_UNIDAD) opt.remove();
      });
      Array.from(centroAsignadoSelect.options).forEach((opt) => {
        if (opt.value === ADMIN_CENTRO) opt.remove();
      });

      categoriaSelect.removeAttribute("readonly");
      unidadAsignadaSelect.removeAttribute("readonly");
      centroAsignadoSelect.removeAttribute("readonly");

      //* Mostrar Dispositivo Apoyo Granada Sur para otros roles
      Array.from(centroAsignadoSelect.options).forEach((opt) => {
        if (opt.value === "Dispositivo Apoyo Granada Sur")
          opt.style.display = "";
      });
    } else {

      //* Categoría

      if (
        !Array.from(categoriaSelect.options).some(
          (opt) => opt.value === ADMIN_CAT
        )
      ) {
        const opt = document.createElement("option");
        opt.value = ADMIN_CAT;
        opt.text = ADMIN_CAT;
        categoriaSelect.add(opt);
      }
      categoriaSelect.value = ADMIN_CAT;

      //* Unidad asignada

      if (
        !Array.from(unidadAsignadaSelect.options).some(
          (opt) => opt.value === ADMIN_UNIDAD
        )
      ) {
        const opt = document.createElement("option");
        opt.value = ADMIN_UNIDAD;
        opt.text = ADMIN_UNIDAD;
        unidadAsignadaSelect.add(opt);
      }
      unidadAsignadaSelect.value = ADMIN_UNIDAD;

      //* Centro asignado

      if (
        !Array.from(centroAsignadoSelect.options).some(
          (opt) => opt.value === ADMIN_CENTRO
        )
      ) {
        const opt = document.createElement("option");
        opt.value = ADMIN_CENTRO;
        opt.text = ADMIN_CENTRO;
        centroAsignadoSelect.add(opt);
      }
      centroAsignadoSelect.value = ADMIN_CENTRO;

      //* Ocultar Dispositivo Apoyo Granada Sur para admin
      Array.from(centroAsignadoSelect.options).forEach((opt) => {
        if (opt.value === "Dispositivo Apoyo Granada Sur")
          opt.style.display = "none";
      });

      categoriaSelect.setAttribute("readonly", true);
      unidadAsignadaSelect.setAttribute("readonly", true);
      centroAsignadoSelect.setAttribute("readonly", true);
    }

    //* Nueva lógica Salientes
    const salienteSection = document.getElementById("saliente_section");
    const allowedCats = ["Médico/a", "DUE"];
    if (
      rolSelect.value === "profesional" &&
      allowedCats.includes(categoriaSelect.value)
    ) {
      salienteSection.style.display = "block";
    } else {
      salienteSection.style.display = "none";
      document.getElementById("es_saliente").checked = false;
    }

    handleCategoriaChange(); //* Validar categoría tras cambio de rol
  }

  //* Categorías especiales

  const SPECIAL_CATEGORIES = [
    "TCAE",
    "Aux Administrativo/a",
    "Administrativo/a",
    "Técnico/a de Rayos",
    "Odontólogo/a",
    "Trabajador/a Social",
    "Fisioterapeuta",
    "Matrón/a",
  ];

  //* Manejo de categorías especiales

  function handleCategoriaChange() {
    const categoria = categoriaSelect.value;
    const isSpecial = SPECIAL_CATEGORIES.includes(categoria);

    if (isSpecial) {
      centroAsignadoSelect.value = "Albuñol";
      centroAsignadoSelect.setAttribute("disabled", true);

      //* Asegurar que el valor se envíe aunque esté disabled

      if (!document.getElementById("centro_hidden_special")) {
        const hiddenCent = document.createElement("input");
        hiddenCent.type = "hidden";
        hiddenCent.name = "centro_asignado";
        hiddenCent.value = "Albuñol";
        hiddenCent.id = "centro_hidden_special";
        form.appendChild(hiddenCent);
      }
    } else {

      //* Solo rehabilitar si no es el caso de Dispositivo Apoyo Granada Sur

      if (
        unidadAsignadaSelect.value !== "Dispositivo Apoyo Granada Sur" &&
        rolSelect.value !== "administrador"
      ) {
        centroAsignadoSelect.removeAttribute("disabled");
      }
      if (document.getElementById("centro_hidden_special")) {
        document.getElementById("centro_hidden_special").remove();
      }
    }
  }

  //* Evento de cambio de categoría

  categoriaSelect.addEventListener("change", handleCategoriaChange);

  //* Manejo de dispositivo de apoyo

  function handleDispositivoConstraint() {
    if (unidadAsignadaSelect.value === "Dispositivo Apoyo Granada Sur") {
      centroAsignadoSelect.value = "Dispositivo Apoyo Granada Sur";
      centroAsignadoSelect.setAttribute("disabled", true);

      //* Metemos un input oculto para que el valor se envíe

      if (!document.getElementById("centro_hidden")) {
        const hiddenCent = document.createElement("input");
        hiddenCent.type = "hidden";
        hiddenCent.name = "centro_asignado";
        hiddenCent.value = "Dispositivo Apoyo Granada Sur";
        hiddenCent.id = "centro_hidden";
        form.appendChild(hiddenCent);
      }
    } else {
      centroAsignadoSelect.removeAttribute("disabled");
      if (document.getElementById("centro_hidden")) {
        document.getElementById("centro_hidden").remove();
      }
    }
  }

  //* Evento de cambio de unidad asignada

  unidadAsignadaSelect.addEventListener("change", handleDispositivoConstraint);

  const submitBtn = document.getElementById("submit_btn");
  const dniInput = document.getElementById("dni");
  const emailInput = document.getElementById("email");
  const telefonoInput = document.getElementById("telefono");
  const inputs = form.querySelectorAll("input[required], select[required]");

  //* Validación de DNI o NIE

  function validarDNI(value) {
    const validChars = "TRWAGMYFPDXBNJZSQVHLCKE";
    const nifRegex = /^[0-9]{8}[TRWAGMYFPDXBNJZSQVHLCKE]$/i;
    const nieRegex = /^[XYZ][0-9]{7}[TRWAGMYFPDXBNJZSQVHLCKE]$/i;

    if (!nifRegex.test(value) && !nieRegex.test(value)) return false;

    let nieValue = value
      .replace(/^[X]/i, "0")
      .replace(/^[Y]/i, "1")
      .replace(/^[Z]/i, "2");

    const number = parseInt(nieValue.slice(0, 8), 10);
    const letter = value.slice(-1).toUpperCase();

    return validChars[number % 23] === letter;
  }

  function validarEmail(email) {
    const emailRegex = /^[a-zA-Z][^\s@]*@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  function validarTelefono(telefono) {
    const telRegex = /^[6789]\d{8}$/;
    return telRegex.test(telefono);
  }

  function updateValidationStyles(input, isValid) {
    if (input.value.trim() === "") {
      input.classList.remove("is-valid", "is-invalid");
    } else if (isValid) {
      input.classList.add("is-valid");
      input.classList.remove("is-invalid");
    } else {
      input.classList.add("is-invalid");
      input.classList.remove("is-valid");
    }
  }

  //* Validación de formulario

  function validateForm() {
    let allValid = true;

    const isDniValid = validarDNI(dniInput.value);
    const isEmailValid = validarEmail(emailInput.value);
    const isTelefonoValid = validarTelefono(telefonoInput.value);

    updateValidationStyles(dniInput, isDniValid);
    updateValidationStyles(emailInput, isEmailValid);
    updateValidationStyles(telefonoInput, isTelefonoValid);

    inputs.forEach((input) => {
      const value = input.value.trim();
      if (input === dniInput) {
        if (!isDniValid) allValid = false;
      } else if (input === emailInput) {
        if (!isEmailValid) allValid = false;
      } else if (input === telefonoInput) {
        if (!isTelefonoValid) allValid = false;
      } else if (input.id === "nombre" || input.id === "apellidos") {
        const nameRegex = /^[a-zA-ZÁéíóúÁÉÍÓÚñÑ][a-zA-ZÁéíóúÁÉÍÓÚñÑ\s]{4,}[a-zA-ZÁéíóúÁÉÍÓÚñÑ]$/;
        const isValid = nameRegex.test(value);
        updateValidationStyles(input, isValid);
        if (!isValid) allValid = false;
      } else {
        const isValid = value.length > 0;
        updateValidationStyles(input, isValid);
        if (!isValid) allValid = false;
      }
    });

    submitBtn.disabled = !allValid;
  }

  inputs.forEach((input) => {
    input.addEventListener("input", validateForm);
    input.addEventListener("change", validateForm);
  });

  rolSelect.addEventListener("change", () => {
    updateAdminFields();
    validateForm();
  });

  updateAdminFields(); //* Inicializar
  validateForm(); //* Inicializar estado del botón
});
