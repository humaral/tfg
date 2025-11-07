/**
 * Autor: Hugo Martín Alonso
 * Fecha: 07/11/2025
 * Descripción: Modificación dinámica de la vista de registro de tramites.
*/

const buttonGuardar = document.getElementById('registro-tramites-guardar');
const nombre = document.getElementById('registro-tramites-nombre');

function isEmpty(){
    buttonGuardar.disabled = !(nombre.value.trim());
}

nombre.addEventListener('input', isEmpty);