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

  function toggleMod(id) {
    const form = document.getElementById("form-mod-" + id);
    const label = document.getElementById("label-tipo-" + id);
    const btns = document.getElementById("btns-" + id);
    const isEditing = form.style.display === "flex";
    form.style.display = isEditing ? "none" : "flex";
    label.style.display = isEditing ? "inline" : "none";
    btns.style.display = isEditing ? "flex" : "none";
  }

  function initFlatpickr(element) {
    flatpickr(element, {
      locale: "es",
      dateFormat: "Y-m-d",
      altInput: true,
      altFormat: "d/m/Y",
      allowInput: true,
      theme: "dark",
    });
  }

  document.getElementById("add-row").addEventListener("click", () => {
    const tbody = document.getElementById("batch-body");
    const row = tbody.querySelector("tr").cloneNode(true);
    const dateInput = row.querySelector(".date-picker");
    if (dateInput) {
      const container = dateInput.parentNode;
      container.innerHTML =
        '<input type="text" name="fecha[]" class="date-picker" required placeholder="Seleccionar fecha" />';
      initFlatpickr(container.querySelector(".date-picker"));
    }
    tbody.appendChild(row);
  });

  document.querySelectorAll(".date-picker").forEach(initFlatpickr);
