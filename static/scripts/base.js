const toggleBtn = document.getElementById("theme-toggle");
if (toggleBtn) {
  const themeIcon = toggleBtn.querySelector("i");
  const rootElement = document.documentElement;

  // Comprobar si hay un tema guardado, sino usar oscuro por defecto
  const savedTheme = localStorage.getItem("theme") || "dark";
  rootElement.setAttribute("data-theme", savedTheme);
  updateIcon(savedTheme, themeIcon);

  toggleBtn.addEventListener("click", () => {
    const currentTheme = rootElement.getAttribute("data-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";

    rootElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
    updateIcon(newTheme, themeIcon);
  });
}

function updateIcon(theme, themeIcon) {
  if (!themeIcon) return;
  if (theme === "dark") {
    themeIcon.className = "fas fa-moon";
  } else {
    themeIcon.className = "fas fa-sun";
  }
}

// Función para desaparecer alertas automáticamente a los 10 segundos
window.autoDismissAlert = function (alertElement) {
  setTimeout(() => {
    alertElement.style.transition = "opacity 0.5s ease";
    alertElement.style.opacity = "0";
    setTimeout(() => alertElement.remove(), 500);
  }, 10000); // 10 segundos
};

// Aplicar auto-dismiss a las alertas que vienen renderizadas por el servidor
document.querySelectorAll(".alert").forEach((alert) => window.autoDismissAlert(alert));

document.addEventListener("DOMContentLoaded", function () {
  const pdfBtns = document.querySelectorAll(".btn-pdf-global");
  if (pdfBtns.length > 0) {
    pdfBtns.forEach((btn) => {
      // Instanciamos el datepicker, pero lo vinculamos AL BOTÓN para que solo muestre el calendario
      const fp = flatpickr(btn, {
        allowInput: true,
        locale: "es",
        onChange: function (selectedDates, dateStr, instance) {
          if (dateStr) {
            // Mostrar indicación visual de carga
            const originalText = btn.innerText;
            btn.innerText = "↻ Generando...";
            btn.style.pointerEvents = "none";

            // Hacer la petición fetch
            fetch(`/descargar_pdf_dia?fecha=${dateStr}`)
              .then(async (response) => {
                if (!response.ok) {
                  try {
                    const errData = await response.json();
                    throw new Error(errData.error || "Error al generar PDF o no hay turnos.");
                  } catch (e) {
                    throw new Error(e.message || "Error de red o de servidor.");
                  }
                }
                return response.blob();
              })
              .then((blob) => {
                // Crear el link invisible para forzar la descarga
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.style.display = "none";
                a.href = url;

                const rawDate = dateStr.replace(/-/g, "");
                a.download = `turnos_${rawDate}.pdf`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);

                // Inyectar el mensaje de éxito usando el mismo formato de flash-messages
                let flashContainer = document.querySelector(".flash-messages");
                if (!flashContainer) {
                  flashContainer = document.createElement("div");
                  flashContainer.className = "flash-messages";
                  // Inyectar justo después del nav o body
                  const main = document.querySelector("main");
                  main.parentNode.insertBefore(flashContainer, main);
                }

                // Ajustar fecha al formato español para el mensaje
                const partes = dateStr.split("-");
                const fechaFormat = `${partes[2]}/${partes[1]}/${partes[0]}`;

                // Añadir alerta verde
                const alertHTML = `<div class="alert alert-success">PDF del ${fechaFormat} generado correctamente.</div>`;
                flashContainer.innerHTML = alertHTML + flashContainer.innerHTML;

                // Auto-dismiss de la nueva alerta
                window.autoDismissAlert(flashContainer.firstElementChild);
              })
              .catch((error) => {
                console.error("Error:", error);

                // Preparar el contenedor flash para pintar el error en rojo
                let flashContainer = document.querySelector(".flash-messages");
                if (!flashContainer) {
                  flashContainer = document.createElement("div");
                  flashContainer.className = "flash-messages";
                  const main = document.querySelector("main");
                  main.parentNode.insertBefore(flashContainer, main);
                }

                // Inyectar la alerta de error recogida
                const alertHTML = `<div class="alert alert-error">${error.message}</div>`;
                flashContainer.innerHTML = alertHTML + flashContainer.innerHTML;

                // Auto-dismiss
                window.autoDismissAlert(flashContainer.firstElementChild);
              })
              .finally(() => {
                btn.innerText = originalText;
                btn.style.pointerEvents = "auto";
                setTimeout(() => instance.clear(), 500);
              });
          }
        },
      });

      btn.addEventListener("click", function (e) {
        e.preventDefault();
        fp.open();
      });
    });
  }
    // Manejo responsivo - Toggler tipo Bootstrap para móvil
  const navbarToggler = document.getElementById("navbarToggler");
  const navbarNav = document.getElementById("navbarNav");
  if (navbarToggler && navbarNav) {
    navbarToggler.addEventListener("click", function () {
      navbarNav.classList.toggle("show");
      const icon = navbarToggler.querySelector("i");
      if (navbarNav.classList.contains("show")) {
        icon.classList.remove("fa-bars");
        icon.classList.add("fa-times");
      } else {
        icon.classList.remove("fa-times");
        icon.classList.add("fa-bars");
      }
    });
  }

  // ---- Usuarios Online: polling cada 30 segundos ----
  function actualizarUsuariosOnline() {
    const contador = document.getElementById("online-count");
    if (!contador) return; // Solo si el elemento existe (usuario logado)

    fetch("/api/usuarios_online")
      .then((res) => {
        if (!res.ok) {
          // Si recibimos un 403 o error, el usuario probablemente ya no está logado
          if (contador.textContent !== "–") contador.textContent = "–";
          return;
        }
        return res.json();
      })
      .then((data) => {
        if (data && typeof data.count === "number") {
          // Pequeña animación al cambiar el número
          if (contador.textContent !== String(data.count)) {
            contador.style.transform = "scale(1.3)";
            contador.style.opacity = "0.5";
            setTimeout(() => {
              contador.textContent = data.count;
              contador.style.transform = "scale(1)";
              contador.style.opacity = "1";
            }, 200);
          }
        }
      })
      .catch(() => {}); // Silencioso en caso de error de red
  }

  // Ejecutar inmediatamente y luego cada 5 segundos
  actualizarUsuariosOnline();
  setInterval(actualizarUsuariosOnline, 5000);

  // ---- Polling de Notificaciones y Solicitudes: cada 10 segundos ----
  function actualizarNotificaciones() {
    const badgeNotificaciones = document.getElementById("notificaciones-badge");
    const badgeSolicitudes = document.getElementById("solicitudes-badge");

    if (!badgeNotificaciones && !badgeSolicitudes) return;

    fetch("/api/notificaciones")
      .then((res) => {
        if (!res.ok) return;
        return res.json();
      })
      .then((data) => {
        if (!data) return;

        // Actualizar Notificaciones (Dirección)
        if (badgeNotificaciones) {
          if (data.notificaciones > 0) {
            badgeNotificaciones.textContent = data.notificaciones;
            badgeNotificaciones.style.display = "flex";
          } else {
            badgeNotificaciones.style.display = "none";
          }
        }

        // Actualizar Solicitudes (Profesional)
        if (badgeSolicitudes) {
          if (data.solicitudes > 0) {
            badgeSolicitudes.textContent = data.solicitudes;
            badgeSolicitudes.style.display = "flex";
          } else {
            badgeSolicitudes.style.display = "none";
          }
        }
      })
      .catch((err) => console.error("Error al actualizar notificaciones:", err));
  }

  // Ejecutar inmediatamente y luego cada 10 segundos
  actualizarNotificaciones();
  setInterval(actualizarNotificaciones, 10000);
});
