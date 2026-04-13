  const miTurnoSel = document.getElementById('mi_turno_id');
  const compTurnoSel = document.getElementById('companero_turno_id');
  const submitBtn = document.getElementById('submit-btn');
  const errorDiv = document.getElementById('validacion-error');

  miTurnoSel.addEventListener('change', validarTodo);
  compTurnoSel.addEventListener('change', validarTodo);

  //* Validación de turnos

  function validarTodo() {
    errorDiv.style.display = 'none';
    submitBtn.disabled = true;
    const originalText = "Enviar Solicitud";
    submitBtn.innerText = originalText;

    if (miTurnoSel.value && compTurnoSel.value) {
      submitBtn.innerText = "⏳ Validando descanso...";
      
      //* Llamar al API de validación
      fetch(`/api/validar_cambio?mi_turno_id=${miTurnoSel.value}&companero_turno_id=${compTurnoSel.value}`)
        .then(res => res.json())
        .then(data => {
          submitBtn.innerText = originalText;
          if (data.valido) {
            submitBtn.disabled = false;
          } else {
            submitBtn.disabled = true; //* Asegurar que sigue bloqueado
            if (data.mensaje) {
              errorDiv.innerText = data.mensaje;
              errorDiv.style.display = 'block';
            }
          }
        })
        .catch(err => {
          console.error("Error validando:", err);
          submitBtn.innerText = originalText;
          submitBtn.disabled = true;
        });
    }
  }

  //* Carga de turnos

  function cargarTurnosCompanero() {
    const dni = document.getElementById('companero_dni').value;
    const selectTurno = document.getElementById('companero_turno_id');
    
    selectTurno.innerHTML = '<option value="">Cargando turnos...</option>';
    selectTurno.disabled = true;
    validarTodo();

    if (!dni) {
      selectTurno.innerHTML = '<option value="">-- Primero selecciona un compañero --</option>';
      return;
    }

    fetch(`/api/turnos_companero/${dni}`)
      .then(response => response.json())
      .then(data => {
        selectTurno.innerHTML = '<option value="">-- Selecciona un turno del compañero --</option>';
        if (data.turnos.length === 0) {
          selectTurno.innerHTML = '<option value="">El compañero no tiene turnos disponibles de 17h/24h</option>';
        } else {
          data.turnos.forEach(turno => {
            selectTurno.innerHTML += `<option value="${turno.id}">${turno.fecha} (${turno.tipo})</option>`;
          });
          selectTurno.disabled = false;
        }
      })
      .catch(error => {
        console.error('Error fetching turnos:', error);
        selectTurno.innerHTML = '<option value="">Error al cargar turnos</option>';
      });
  }

  //* Hacer estrictamente global para onclick en línea
  window.cargarTurnosCompanero = cargarTurnosCompanero;
