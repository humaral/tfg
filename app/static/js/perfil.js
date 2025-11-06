/**
 * Autor: Hugo Martín Alonso
 * Fecha: 06/11/2025
 * Descripción: estilos dinámicos de la vista del perfil de empleado.
 */

const buttonCambiarPass = document.getElementById("button-cambiar-pass");
const formCambiarPass = document.getElementById("form-cambiar-pass");

const currentPass = document.getElementById('currentPass');
const newPass = document.getElementById('newPass');
const confirmPass = document.getElementById('confirmPass');
const buttonConfirmar = document.getElementById("button-confirmar-cambio-pass")

const buttonCurrentPass = document.getElementById('button-currentPass');
const buttonNewPass = document.getElementById('button-newPass');
const buttonConfirmPass = document.getElementById('button-confirmPass');

//TODO acabar
// document.getElementById("foto-perfil").addEventListener("click", async (e) =>{

//     const file = e.target.files[0];
//     console.log(file);
//     if (!file) return;

//     const formData = new FormData();
//     formData.append("foto_perfil", file);

//     const response = await fetch("/uploads/perfil", {method:"POST", body: formData});
//     const result = await response.json();
//     console.log(response, result);
// });

function isEmpty(){
    buttonConfirmar.disabled = !(currentPass.value.trim() && newPass.value.trim() && confirmPass.value.trim());
}

function mostrarPassword(input, button){
    
    if (input.type == "password") {
        input.type = "text";
        button.querySelector("iconify-icon").setAttribute("icon", "famicons:eye-outline");
    }
    else{
        input.type = "password";
        button.querySelector("iconify-icon").setAttribute("icon", "famicons:eye-off-outline");
    }
}



currentPass.addEventListener('input', isEmpty);
newPass.addEventListener('input', isEmpty);
confirmPass.addEventListener('input', isEmpty);

buttonCurrentPass.addEventListener('click', () => mostrarPassword(currentPass, buttonCurrentPass));
buttonNewPass.addEventListener('click', () => mostrarPassword(newPass, buttonNewPass));
buttonConfirmPass.addEventListener('click', () => mostrarPassword(confirmPass, buttonConfirmPass));

buttonCambiarPass.addEventListener("click", ()=>{
    formCambiarPass.classList.toggle("hidden");
});