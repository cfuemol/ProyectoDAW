  const form = document.getElementById("change_pass_form");
  const passInput = document.getElementById("new_password");
  const confirmInput = document.getElementById("confirm_password");
  const submitBtn = document.getElementById("submit_btn");

  function validarPassword(pass) {
    const hasUpper = /[A-Z]/.test(pass);
    const hasLower = /[a-z]/.test(pass);
    const hasNumber = /[0-9]/.test(pass);
    const hasSymbol = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(pass);
    const validLength = pass.length >= 8 && pass.length <= 12;
    return hasUpper && hasLower && hasNumber && hasSymbol && validLength;
  }

  function validateForm() {
    const pass = passInput.value;
    const confirm = confirmInput.value;

    const isPassValid = validarPassword(pass);
    const isConfirmValid = confirm === pass && pass !== "";

    //* Estilos para Password
    if (pass === "") {
      passInput.classList.remove("is-valid", "is-invalid");
    } else if (isPassValid) {
      passInput.classList.add("is-valid");
      passInput.classList.remove("is-invalid");
    } else {
      passInput.classList.add("is-invalid");
      passInput.classList.remove("is-valid");
    }

    //* Estilos para Confirm
    if (confirm === "") {
      confirmInput.classList.remove("is-valid", "is-invalid");
    } else if (isConfirmValid) {
      confirmInput.classList.add("is-valid");
      confirmInput.classList.remove("is-invalid");
    } else {
      confirmInput.classList.add("is-invalid");
      confirmInput.classList.remove("is-valid");
    }

    submitBtn.disabled = !(isPassValid && isConfirmValid);
  }

  passInput.addEventListener("input", validateForm);
  confirmInput.addEventListener("input", validateForm);
