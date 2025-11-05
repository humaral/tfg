const menuPeticiones = document.getElementById("menu-empleados")
menuPeticiones.setAttribute("class", "selected")

const usernameFiltro = document.getElementById("filter-username-empleados");
const nombreFiltro = document.getElementById("filter-nombre-empleados");
const emailFiltro = document.getElementById("filter-email-empleados");
const rolFiltro = document.getElementById("filter-rol-empleados");
const activoFiltro = document.getElementById("filter-activo-empleados");

const tabla_empleados = document.getElementById("empleados-table").querySelector("tbody");

let ordenActual = "username";
let direccionActual = "ascendente";
const icono = document.getElementById('orden-icono-empleados');

const per_pageFiltro = document.getElementById("filter-num-empleados");
const previousPageButton = document.getElementById("prev-page-empleados");
const listPages = document.getElementById("lista-pages-empleados");
const nextPageButton = document.getElementById("next-page-empleados");

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
        username: usernameFiltro.value,
        nombre: nombreFiltro.value,
        email: emailFiltro.value,
        rol: rolFiltro.value,
        activo: activoFiltro.checked,
        orden: ordenActual,
        direccion: direccionActual,
        per_page: per_pageFiltro.value,
        page: pageActual
    });

    const res = await fetch(`/api/empleados?${params}`);
    const data = await res.json();

    tabla_empleados.innerHTML = data.empleados.map(e =>
        `<tr>
            <td>${e.username}</td>
            <td>${e.nombre}</td>
            <td>${e.email}</td>
            <td>${e.rol}</td>
            <td class="icono-empleados-activo">
                ${e.activo
                    ? `<iconify-icon id="active-true" icon="charm:circle-tick"></iconify-icon>`
                    : `<td><iconify-icon id="active-false" icon="charm:circle-cross"></iconify-icon>`}
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
usernameFiltro.addEventListener("input", actualizarTabla);
nombreFiltro.addEventListener("input", actualizarTabla);
emailFiltro.addEventListener("input", actualizarTabla);
rolFiltro.addEventListener("change", actualizarTabla);
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