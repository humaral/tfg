/**
 * Autor: Hugo Martín Alonso
 * Fecha: 25-09-2025
 * Descripción: script para dinamizar la página de login.
 */


const button = document.getElementById('login-button');
const username = document.getElementById('login-username');
const password = document.getElementById('login-password');

//Si los inputs no tienen ningún valor se desactiva el botón de inicio de sesión.
function isEmpty(){
    button.disabled = !(username.value.trim() && password.value.trim());
}

username.addEventListener('input', isEmpty);
password.addEventListener('input', isEmpty);