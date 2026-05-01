  //* Filtro de cuadrante

  function filterQuadrant(dni) {
    const container = document.getElementById("cuadrante-container");
    const rows = document.querySelectorAll(".quadrant-row");

    if (!dni) {
      container.style.display = "none";
      return;
    }

    container.style.display = "block";
    rows.forEach((row) => {
      if (row.getAttribute("data-dni") === dni) {
        row.style.display = "";
      } else {
        row.style.display = "none";
      }
    });

    container.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  //* Toggle de modificación

  function toggleMod(id) {
    const form = document.getElementById("form-mod-" + id);
    const label = document.getElementById("label-tipo-" + id);
    const btns = document.getElementById("btns-" + id);
    const isEditing = form.style.display === "flex";
    form.style.display = isEditing ? "none" : "flex";
    label.style.display = isEditing ? "inline" : "none";
    btns.style.display = isEditing ? "flex" : "none";
  }

  //* Inicialización de Flatpickr

  function initFlatpickr(element) {
    flatpickr(element, {
      locale: "es",
      dateFormat: "Y-m-d",
      altInput: true,
      altFormat: "d/m/Y",
      allowInput: true,
    });
  }

  //* Plantilla de filas

  let rowTemplate = null;
  document.addEventListener("DOMContentLoaded", () => {
    const firstRow = document.querySelector("#batch-body tr");
    if (firstRow) {
      rowTemplate = firstRow.cloneNode(true);
      // Limpiar valores en el template
      rowTemplate.querySelector("select[name='profesional_dni[]']").value = "";
      rowTemplate.querySelector("select[name='tipo[]']").value = "7h";
    }
  });

  //* Añadir fila
  document.getElementById("add-row").addEventListener("click", () => {
    const tbody = document.getElementById("batch-body");
    let row;
    
    if (tbody.lastElementChild) {
       row = tbody.lastElementChild.cloneNode(true);
    } else if (rowTemplate) {
       row = rowTemplate.cloneNode(true);
    } else {
       return;
    }
    
    const dateInput = row.querySelector(".date-picker");
    if (dateInput) {
      const container = dateInput.parentNode;
      container.innerHTML =
        '<input type="text" name="fecha[]" class="date-picker" required placeholder="Seleccionar fecha" />';
      initFlatpickr(container.querySelector(".date-picker"));
    }
    tbody.appendChild(row);
    
    //* Actualizar el cuadrante con el profesional de la nueva fila
    const select = row.querySelector("select[name='profesional_dni[]']");
    if (select) {
      filterQuadrant(select.value);
    }
  });

  //* Eliminar fila (función global para ser llamada desde el HTML)
  window.removeRow = function(btn) {
    const tr = btn.closest("tr");
    const tbody = document.getElementById("batch-body");
    tr.remove();

    const remainingRows = tbody.querySelectorAll("tr");
    if (remainingRows.length === 0) {
      filterQuadrant(""); // Oculta el cuadrante si no quedan filas
    } else {
      //* Muestra el cuadrante de la última fila restante
      const lastRow = remainingRows[remainingRows.length - 1];
      const select = lastRow.querySelector("select[name='profesional_dni[]']");
      if (select) {
        filterQuadrant(select.value);
      }
    }
  };

  //* Inicializar Flatpickr en todos los date-picker

  document.querySelectorAll(".date-picker").forEach(initFlatpickr);
