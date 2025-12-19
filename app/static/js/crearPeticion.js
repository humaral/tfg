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

    const idTramite = inputTramite.value;

    if(idTramite=='0'){
        templateContainer.innerHTML = "";
        return;
    }
    
    const response = await fetch(`/cargar_plantilla/${idTramite}`);
    const html = await response.text();

    templateContainer.innerHTML = html;

    // Certificado Empadronamiento
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

    //Cita AEAT
    const inputDNIAEAT = document.getElementById("cita-aeat-dni");
    if (inputDNIAEAT){
        inputDNIAEAT.addEventListener("invalid", ()=>{
            inputDNIAEAT.setCustomValidity("Introduce un número telefónico español váldio.");
        });
        inputDNIAEAT.addEventListener("input", ()=>{
            inputDNIAEAT.setCustomValidity("");
        });
    }

    const buttonModalidad = document.getElementById("cita-aeat-modalidad");
    const inputModalidad = document.getElementById("cita-aeat-modalidad-hidden");
    const divOficina = document.getElementById("cita-aeat-oficina");
    const inputOficina = document.getElementById("cita-aeat-campo-oficina");
    const divFecha = document.getElementById("cita-aeat-fecha");
    const inputDia = document.getElementById("cita-aeat-dia");
    const inputHora = document.getElementById("cita-aeat-hora");
    const inputEmail = document.getElementById("cita-aeat-email");
    const labelOficina = document.getElementById("cita-aeat-label-oficina");
    const labelFecha = document.getElementById("cita-aeat-label-fecha");
    const labelEmail = document.getElementById("cita-aeat-label-email");

    if (buttonModalidad){
        
            const icono = buttonModalidad.querySelector("iconify-icon");
            const texto = buttonModalidad.querySelector("p");

            const actualizarPlantilla = (modalidad) => {
                
                inputModalidad.value = modalidad;

                if(modalidad=="presencial"){
                    icono.setAttribute("icon", "raphael:employee");
                    texto.textContent = "Presencial";

                    divOficina.style.display = "flex";
                    inputOficina.required = true;
                    divFecha.style.display = "flex";
                    inputDia.required = true;
                    inputHora.required = true;
                    inputEmail.style.display = "none";
                    inputEmail.required = false;
                    labelOficina.style.display = "block";
                    labelFecha.style.display = "block";
                    labelEmail.style.display = "none";
                }
                else{
                    icono.setAttribute("icon", "tabler:video");
                    texto.textContent = "Virtual";

                    divOficina.style.display = "none";
                    inputOficina.required = false;
                    divFecha.style.display = "none";
                    inputDia.required = false;
                    inputHora.required = false;
                    inputEmail.style.display = "block";
                    inputEmail.required = true;
                    labelOficina.style.display = "none";
                    labelFecha.style.display = "none";
                    labelEmail.style.display = "block";
                }
                buttonModalidad.dataset.modalidad = modalidad;
            };

            const modalidadinicial = buttonModalidad.dataset.modalidad || "virtual";
            actualizarPlantilla(modalidadinicial);

            buttonModalidad.addEventListener("click", ()=>{
                const nuevaModalidad = buttonModalidad.dataset.modalidad =="presencial" ? "virtual" : "presencial";
                actualizarPlantilla(nuevaModalidad);
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