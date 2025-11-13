/**
 * Autor: Hugo Martín Alonso
 * Fecha: 05/11/2025
 * Descripción: Modificación dinámica de la vista de editar de empleados.
*/

const buttonGuardar = document.getElementById('editar-empleados-guardar');
const nombre = document.getElementById('editar-empleados-nombre');
const apellido1 = document.getElementById('editar-empleados-apellido1');
const email = document.getElementById('editar-empleados-email');

function isEmpty(){
    buttonGuardar.disabled = !(nombre.value.trim() && apellido1.value.trim() && email.value.trim());
}

nombre.addEventListener('input', isEmpty);
apellido1.addEventListener('input', isEmpty);
email.addEventListener('input', isEmpty);

isEmpty();