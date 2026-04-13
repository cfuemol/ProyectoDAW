  document.addEventListener("DOMContentLoaded", function () {
    const pickerInput = document.getElementById("month-picker");
    const defaultDateVal = pickerInput.getAttribute("data-default-date");
    
    //* Inicializa el selector de mes

    const monthPicker = flatpickr("#month-picker", {
      locale: "es",
      plugins: [
        new monthSelectPlugin({
          shorthand: true,
          dateFormat: "m/Y",
          altFormat: "F Y",
        }),
      ],
      defaultDate: defaultDateVal,
      onChange: function (selectedDates, dateStr, instance) {
        if (selectedDates.length > 0) {
          const date = selectedDates[0];
          const mes = date.getMonth() + 1;
          const anio = date.getFullYear();

          //* Recargar con los nuevos parámetros

          window.location.href = `/profesional/ver_cuadrante?mes=${mes}&anio=${anio}`;
        }
      },
    });
  });
