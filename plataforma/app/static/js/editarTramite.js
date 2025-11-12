/**
 * Autor: Hugo Martín Alonso
 * Fecha: 07/11/2025
 * Descripción: Modificación dinámica de la vista de editar de tramites.
*/

const buttonGuardar = document.getElementById('editar-tramites-guardar');
const nombre = document.getElementById('editar-tramites-nombre');

function isEmpty(){
    buttonGuardar.disabled = !(nombre.value.trim());
}

nombre.addEventListener('input', isEmpty);

isEmpty();