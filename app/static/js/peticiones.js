const idFiltro = document.getElementById("filter-id");
const telefonoFiltro = document.getElementById("filter-telefono");
const estadoFiltro = document.getElementById("filter-estado");
const tramiteFiltro = document.getElementById("filter-tramite");
const empleadoFiltro = document.getElementById("filter-empleado");

const tabla_body = document.getElementById("peticiones-table").querySelector("tbody");

let ordenActual = "id";
let direccionActual = "ascendente";
const icono = document.getElementById('orden-icono');

const per_pageFiltro = document.getElementById("filter-per_page");
const lista_paginas = document.getElementById("lista-paginas");

document.querySelectorAll(".ordenable").forEach(th =>{

    th.addEventListener("click", () => {

        const orden  = th.dataset.orden;
        
        if(orden == ordenActual){
            if(direccionActual == "ascendente"){
                direccionActual = "descendente";
                icono.setAttribute("icon","tabler:arrow-down");
            }
            else{
                direccionActual = "ascendente";
                icono.setAttribute("icon","tabler:arrow-up");
            }
        }
        else{
            ordenActual = orden;
            direccionActual = "ascendente";
            icono.setAttribute("icon","tabler:arrow-up");
        }

        
        th.querySelector("div").appendChild(icono);

        actualizarTabla();

    });
});


async function actualizarTabla() {
    const params = new URLSearchParams({
        id: idFiltro.value,
        telefono: telefonoFiltro.value,
        estado: estadoFiltro.value,
        tramite: tramiteFiltro.value,
        empleado: empleadoFiltro.value,
        orden: ordenActual,
        direccion: direccionActual,
        per_page: per_pageFiltro.value
    });

    const res = await fetch(`/api/peticiones?${params}`);
    const data = await res.json();

    tabla_body.innerHTML = data.map(p =>
        `<tr>
            <td><a href="${urlSumaryPeticion.replace('0', p.id)}">${p.id}</a></td>
            <td>${p.telefono}</td>
            <td>${p.estado}</td>
            <td>${p.tramite}</td>
            <td>${p.creacion}</td>
            <td>${p.asignacion}</td>
        </tr>`
    ).join("");

}

idFiltro.addEventListener("input", actualizarTabla);
telefonoFiltro.addEventListener("input", actualizarTabla);
estadoFiltro.addEventListener("change", actualizarTabla);
tramiteFiltro.addEventListener("change", actualizarTabla);
empleadoFiltro.addEventListener("input", actualizarTabla);

per_pageFiltro.addEventListener("change", actualizarTabla);
