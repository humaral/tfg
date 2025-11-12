/**
 * Autor: Hugo Martín Alonso
 * Fecha: 07-11-2025
 * Descripción: estilos dinámicos específicos de la página de tramites.
 */


const menuTramites = document.getElementById("menu-tramites")
menuTramites.setAttribute("class", "selected")

const idFiltro = document.getElementById("filter-id-tramites");
const nombreFiltro = document.getElementById("filter-nombre-tramites");
const activoFiltro = document.getElementById("filter-activo-tramites");

const tabla_tramites = document.getElementById("tramites-table").querySelector("tbody");

let ordenActual = "id";
let direccionActual = "ascendente";
const icono = document.getElementById('orden-icono-tramites');

const per_pageFiltro = document.getElementById("filter-num-tramites");
const previousPageButton = document.getElementById("prev-page-tramites");
const listPages = document.getElementById("lista-pages-tramites");
const nextPageButton = document.getElementById("next-page-tramites");

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
        valor: nombreFiltro.value,
        activo: activoFiltro.checked,
        orden: ordenActual,
        direccion: direccionActual,
        per_page: per_pageFiltro.value,
        page: pageActual
    });

    const res = await fetch(`/api/tramites?${params}`);
    const data = await res.json();

    tabla_tramites.innerHTML = data.tramites.map(t =>
        `<tr>
            <td>${t.id}</td>
            <td>${t.nombre}</td>
            <td class="icono-tramites-activo">
                <a href="${urlEditarTramite}?id=${t.id}" class="button-activo">
                ${t.activo
                    ? `<iconify-icon id="active-true-tramite" icon="charm:circle-tick"></iconify-icon>`
                    : `<iconify-icon id="active-false-tramite" icon="charm:circle-cross"></iconify-icon>`}
                </a>
            </td>
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
nombreFiltro.addEventListener("input", actualizarTabla);
activoFiltro.addEventListener("change", actualizarTabla);


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