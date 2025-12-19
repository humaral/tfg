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

//Cita AEAT
const buttonModalidad = document.getElementById("cita-aeat-modalidad");
const inputOficina = document.getElementById("cita-aeat-oficina");
const inputFecha = document.getElementById("cita-aeat-fecha");
const inputEmail = document.getElementById("cita-aeat-email");
const labelOficina = document.getElementById("cita-aeat-label-oficina");
const labelFecha = document.getElementById("cita-aeat-label-fecha");
const labelEmail = document.getElementById("cita-aeat-label-email");

if (buttonModalidad) {

    const icono = buttonModalidad.querySelector("iconify-icon");
    const texto = buttonModalidad.querySelector("p");

    const actualizarPlantilla = (modalidad) => {
        if (modalidad == "presencial") {
            icono.setAttribute("icon", "raphael:employee");
            texto.textContent = "Presencial";

            inputOficina.style.display = "flex";
            inputFecha.style.display = "flex";
            inputEmail.style.display = "none";
            labelOficina.style.display = "block";
            labelFecha.style.display = "block";
            labelEmail.style.display = "none";
        }
        else {
            icono.setAttribute("icon", "tabler:video");
            texto.textContent = "Virtual";

            inputOficina.style.display = "none";
            inputFecha.style.display = "none";
            inputEmail.style.display = "block";
            labelOficina.style.display = "none";
            labelFecha.style.display = "none";
            labelEmail.style.display = "block";
        }
        buttonModalidad.dataset.modalidad = modalidad;
    };

    const modalidadinicial = buttonModalidad.dataset.modalidad || "virtual";
    actualizarPlantilla(modalidadinicial);

    buttonModalidad.addEventListener("click", () => {
        const nuevaModalidad = buttonModalidad.dataset.modalidad == "presencial" ? "virtual" : "presencial";
        actualizarPlantilla(nuevaModalidad);
    });
}