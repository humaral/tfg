/**
 * Autor: Hugo Martín Alonso
 * Fecha: 09/11/2025
 * Descripción: código de la vista de crear peticiones
 */

const inputTramite = document.getElementById("crear-peticion-tramite");
const templateContainer = document.getElementById("crear-peticion-template");

const inputTelefonoLlamada = document.getElementById("crear-peticion-telefono");
const buttonGuardar = document.getElementById("crear-peticion-guardar");


function isEmpty(){
    buttonGuardar.disabled = !(inputTelefonoLlamada.value.trim() && inputTramite.value!='0');
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

    const inputTelefono = document.getElementById("certificado-empadronamiento-telefono");
    const inputDNI = document.getElementById("certificado-empadronamiento-dni");
    if (inputTelefono){
        inputTelefono.addEventListener("invalid", ()=>{
            inputTelefono.setCustomValidity("Introduce un número telefónico español váldio.");
        });
        inputTelefono.addEventListener("input", ()=>{
            inputTelefono.setCustomValidity("");
        });
    }
    
    if (inputDNI){
        inputDNI.addEventListener("invalid", ()=>{
            inputDNI.setCustomValidity("Introduce un DNI váldio.");
        });
        inputDNI.addEventListener("input", ()=>{
            inputDNI.setCustomValidity("");
        });
    }
});

inputTelefonoLlamada.addEventListener("invalid", ()=>{
    inputTelefonoLlamada.setCustomValidity("Introduce un número telefónico español váldio.");
});
inputTelefonoLlamada.addEventListener("input", ()=>{
    inputTelefonoLlamada.setCustomValidity("");
});

inputTramite.addEventListener("change", isEmpty);
inputTelefonoLlamada.addEventListener("input", isEmpty);

isEmpty();