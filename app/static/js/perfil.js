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

currentPass.addEventListener('input', isEmpty);
newPass.addEventListener('input', isEmpty);
confirmPass.addEventListener('input', isEmpty);




buttonCambiarPass.addEventListener("click", ()=>{

    formCambiarPass.classList.toggle("hidden");
});