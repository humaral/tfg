/**
 * Autor: Hugo Martín Alonso
 * Fecha: 25-09-2025
 * Descripción: Script para dinamizar la página de login.
 */


const button = document.getElementById('login-button');
const username = document.getElementById('login-username');
const password = document.getElementById('login-password');
const buttonPassword = document.getElementById('button-password')

//Si los inputs no tienen ningún valor se desactiva el botón de inicio de sesión.
function isEmpty(){
    button.disabled = !(username.value.trim() && password.value.trim());
}

username.addEventListener('input', isEmpty);
password.addEventListener('input', isEmpty);

buttonPassword.addEventListener("click", () => {
    
    if (password.type == "password") {
        password.type = "text";
        buttonPassword.querySelector("iconify-icon").setAttribute("icon", "famicons:eye-outline");
    }
    else{
        password.type = "password";
        buttonPassword.querySelector("iconify-icon").setAttribute("icon", "famicons:eye-off-outline");
    }
});

isEmpty();