/**
 * Autor: Hugo Martín Alonso
 * Fecha: 09/11/2025
 * Descripción: código de la vista de crear peticiones
 */

const inputTramite = document.getElementById("crear-peticion-tramite");
const templateContainer = document.getElementById("crear-peticion-template");

const inputTelefono = document.getElementById("crear-peticion-telefono");
const buttonGuardar = document.getElementById("crear-peticion-guardar");

function isEmpty(){
    buttonGuardar.disabled = !(inputTelefono.value.trim() && inputTramite.value!='0');
    console.log(!(inputTelefono.value.trim() && inputTramite.value!='0'))
}

inputTramite.addEventListener("change", async () => {

    const tramite = inputTramite.value;

    if(tramite=='0'){
        templateContainer.innerHTML = "";
        return;
    }
    
    const response = await fetch(`/cargar_plantilla/${tramite}`);
    const html = await response.text();

    templateContainer.innerHTML = html;
});

inputTelefono.addEventListener("invalid", ()=>{
    inputTelefono.setCustomValidity("Introduce un número telefónico español váldio.");
});

inputTramite.addEventListener("change", isEmpty);
inputTelefono.addEventListener("input", isEmpty);

isEmpty();