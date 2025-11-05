const menuPeticiones = document.getElementById("menu-peticiones")
menuPeticiones.setAttribute("class", "selected")

const idFiltro = document.getElementById("filter-id-peticiones");
const telefonoFiltro = document.getElementById("filter-telefono-peticiones");
const estadoFiltro = document.getElementById("filter-estado-peticiones");
const tramiteFiltro = document.getElementById("filter-tramite-peticiones");
const empleadoFiltro = document.getElementById("filter-empleado-peticiones");

const tabla_peticiones = document.getElementById("peticiones-table").querySelector("tbody");

let ordenActual = "id";
let direccionActual = "ascendente";
const icono = document.getElementById('orden-icono-peticiones');

const per_pageFiltro = document.getElementById("filter-num-peticiones");
const previousPageButton = document.getElementById("prev-page-peticiones");
const listPages = document.getElementById("lista-pages-peticiones");
const nextPageButton = document.getElementById("next-page-peticiones");

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

// Actualiza dinámicamente el contenido de la tabla
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

    tabla_peticiones.innerHTML = data.peticiones.map(p =>
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
    const left = Math.max(1, pageActual - 1);
    const right = Math.min(totalPages, pageActual + 1);

    if(pageActual==1) previousPageButton.style.display = "none";
    else previousPageButton.style.display = "inline-block";
        
    if(pageActual == totalPages) nextPageButton.style.display = "none";
    else nextPageButton.style.display = "inline-block";

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

per_pageFiltro.addEventListener("change", () =>{
    pageActual=1;
    actualizarTabla();
});
previousPageButton.addEventListener("click", () => {
    pageActual--;
    actualizarTabla();
});
nextPageButton.addEventListener("click", () => {
    pageActual++;
    actualizarTabla();
});

actualizarTabla();