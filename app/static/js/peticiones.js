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
const previousPageButton = document.getElementById("prev-page");
const listPages = document.getElementById("lista-pages");
const nextPageButton = document.getElementById("next-page");

let pageActual = 1;
let totalPages = 1;

// Filtros
document.querySelectorAll(".ordenable").forEach(th => {

    th.addEventListener("click", () => {

        const orden = th.dataset.orden;

        if (orden == ordenActual) {
            if (direccionActual == "ascendente") {
                direccionActual = "descendente";
                icono.setAttribute("icon", "tabler:arrow-down");
            }
            else {
                direccionActual = "ascendente";
                icono.setAttribute("icon", "tabler:arrow-up");
            }
        }
        else {
            ordenActual = orden;
            direccionActual = "ascendente";
            icono.setAttribute("icon", "tabler:arrow-up");
        }


        th.querySelector("div").appendChild(icono);
        pageActual=1;
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
        per_page: per_pageFiltro.value,
        page: pageActual
    });

    const res = await fetch(`/api/peticiones?${params}`);
    const data = await res.json();

    tabla_body.innerHTML = data.peticiones.map(p =>
        `<tr>
            <td><a href="${urlSumaryPeticion.replace('0', p.id)}">${p.id}</a></td>
            <td>${p.telefono}</td>
            <td>${p.estado}</td>
            <td>${p.tramite}</td>
            <td>${p.creacion}</td>
            <td>${p.asignacion}</td>
        </tr>`
    ).join("");

    pageActual = data.pageActual;
    totalPages = data.totalPages;

    cargarPaginacion();
}

// Paginacion
function cargarPaginacion() {
    const pages = [];
    const aux = 1;
    const left = Math.max(1, pageActual - aux);
    const right = Math.min(totalPages, pageActual + aux);

    previousPageButton.style.display = pageActual == 1 ? "none" : "inline-block";
    nextPageButton.style.display = pageActual == totalPages ? "none" : "inline-block";

    if (left > 2) pages.push(1, "...");
    else for (i = 1; i < left; i++) pages.push(i);

    for (i = left; i <= right; i++) pages.push(i);

    if (right < totalPages - 1) pages.push("...", totalPages);
    else for (i = right + 1; i <= totalPages; i++) pages.push(i);

    listPages.innerHTML = pages.map(p => {
        if (p == "...") return `<a>...</a>`;
        else if (p == pageActual) return `<a class=selected>${p}</a>`;
        else return `<a data-page="${p}">${p}</a>`;
    }).join("");

    listPages.querySelectorAll("a[data-page]").forEach(a => {
        a.addEventListener("click", ()=>{
            pageActual = parseInt(a.dataset.page);
            actualizarTabla();
        });
    });
}


// Eventos
idFiltro.addEventListener("input", actualizarTabla);
telefonoFiltro.addEventListener("input", actualizarTabla);
estadoFiltro.addEventListener("change", actualizarTabla);
tramiteFiltro.addEventListener("change", actualizarTabla);
empleadoFiltro.addEventListener("input", actualizarTabla);

per_pageFiltro.addEventListener("change", actualizarTabla);
previousPageButton.addEventListener("click", () => {
    pageActual--;
    actualizarTabla();
});
nextPageButton.addEventListener("click", () => {
    pageActual++;
    actualizarTabla();
});

actualizarTabla();