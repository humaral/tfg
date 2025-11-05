/**
 * Autor: Hugo Martín Alonso
 * Fecha: 05/11/2025
 * Descripción: Modificación dinámica de la vista de registro de empleados.
*/

const buttonGuardar = document.getElementById('registro-empleados-guardar');
const nombre = document.getElementById('registro-empleados-nombre');
const apellido1 = document.getElementById('registro-empleados-apellido1');
const email = document.getElementById('registro-empleados-email');

function isEmpty(){
    buttonGuardar.disabled = !(nombre.value.trim() && apellido1.value.trim() && email.value.trim());
}

nombre.addEventListener('input', isEmpty);
apellido1.addEventListener('input', isEmpty);
email.addEventListener('input', isEmpty);