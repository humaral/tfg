/**
 * Autor: Hugo Martín Alonso
 * Fecha: 20-11-2025
 * Descripción: estilos dinámicos específicos de la página resumen de una petición.
 */


const inputTelefono = document.getElementById("certificado-empadronamiento-telefono");
const inputDNI = document.getElementById("certificado-empadronamiento-dni");


if (inputTelefono) {
    inputTelefono.addEventListener("invalid", () => {
        inputTelefono.setCustomValidity("Introduce un número telefónico español váldio.");
    });
    inputTelefono.addEventListener("input", () => {
        inputTelefono.setCustomValidity("");
    });
}

if (inputDNI) {
    inputDNI.addEventListener("invalid", () => {
        inputDNI.setCustomValidity("Introduce un DNI váldio.");
    });
    inputDNI.addEventListener("input", () => {
        inputDNI.setCustomValidity("");
    });
}