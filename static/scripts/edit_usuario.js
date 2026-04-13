  const rolSelect = document.getElementById("rol");
  const categoriaSelect = document.getElementById("categoria");
  const unidadAsignadaSelect = document.getElementById("unidad_asignada");
  const centroAsignadoSelect = document.getElementById("centro_asignado");

  const ADMIN_CAT = "Técnico Especialista en Informática";
  const ADMIN_UNIDAD = "SAS";
  const ADMIN_CENTRO = "Distrito Sanitario Granada Sur (SAS)";

  function updateAdminFields() {
    if (rolSelect.value === "administrador") {
      //* Es administrador
      if (!Array.from(categoriaSelect.options).some(opt => opt.value === ADMIN_CAT)) {
        const opt = document.createElement("option");
        opt.value = ADMIN_CAT; opt.text = ADMIN_CAT;
        categoriaSelect.add(opt);
      }
      categoriaSelect.value = ADMIN_CAT;

      if (!Array.from(unidadAsignadaSelect.options).some(opt => opt.value === ADMIN_UNIDAD)) {
        const opt = document.createElement("option");
        opt.value = ADMIN_UNIDAD; opt.text = ADMIN_UNIDAD;
        unidadAsignadaSelect.add(opt);
      }
      unidadAsignadaSelect.value = ADMIN_UNIDAD;

      if (!Array.from(centroAsignadoSelect.options).some(opt => opt.value === ADMIN_CENTRO)) {
        const opt = document.createElement("option");
        opt.value = ADMIN_CENTRO; opt.text = ADMIN_CENTRO;
        centroAsignadoSelect.add(opt);
      }
      centroAsignadoSelect.value = ADMIN_CENTRO;

      //* Ocultar Dispositivo Apoyo Granada Sur para admin
      Array.from(centroAsignadoSelect.options).forEach(opt => {
        if (opt.value === "Dispositivo Apoyo Granada Sur") opt.style.display = "none";
      });

      categoriaSelect.setAttribute("readonly", true);
      unidadAsignadaSelect.setAttribute("readonly", true);
      centroAsignadoSelect.setAttribute("readonly", true);
    } else {
      
      //* Mostrar Dispositivo Apoyo Granada Sur para otros roles
      Array.from(centroAsignadoSelect.options).forEach(opt => {
        if (opt.value === "Dispositivo Apoyo Granada Sur") opt.style.display = "";
      });

      categoriaSelect.removeAttribute("readonly");
      unidadAsignadaSelect.removeAttribute("readonly");
      centroAsignadoSelect.removeAttribute("readonly");
    }

    //* Nueva lógica Salientes
    const salienteSection = document.getElementById("saliente_section");
    const allowedCats = ["Médico/a", "DUE"];
    if (rolSelect.value === "profesional" && allowedCats.includes(categoriaSelect.value)) {
      salienteSection.style.display = "block";
    } else {
      salienteSection.style.display = "none";
      document.getElementById("es_saliente").checked = false;
    }
  }

  rolSelect.addEventListener("change", updateAdminFields);
  categoriaSelect.addEventListener("change", updateAdminFields);
  updateAdminFields();
