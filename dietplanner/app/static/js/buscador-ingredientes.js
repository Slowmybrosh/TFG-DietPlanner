$(document).ready(function() {
    $('#buscador-ingredientes').on('input', function() {
        var query = $(this).val();
        $.ajax({
            url: '/buscar/',
            data: {'query': query},
            dataType: 'json',
            success: function(response) {
                BuscarIngrediente(response)
            }
        });
    });
});

function BuscarIngrediente(response) {
    if(ObtenerCookie("IDs") == null){
        var json = {
            seleccionados: []
        };
        crearCookie("IDs",JSON.stringify(json),1);
    }
    $('#tabla').removeAttr('hidden');
    var tabla = $('#tabla-ingredientes');
    if(response == null){
        tabla.empty();
    } else{
        var resultados = response.resultados;
        tabla.empty();
        for (var i = 0; i < resultados.length; i++) {
            var fila = $('<tr data-id="'+resultados[i].id+'" onclick="SeleccionarIngrediente(this)">');
            fila.append($('<td class="">').text(resultados[i].nombre));
            fila.append($('<td>').text(""));
            var td = $('<td class="text-center">');
            var svg = '<svg';
            if(isSeleccionado(resultados[i].id) == false){
                svg += " hidden"
            }
            svg += ' xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="40" zoomAndPan="magnify" viewBox="0 0 30 30.000001" height="40" preserveAspectRatio="xMidYMid meet" version="1.0"><defs><clipPath id="id1"><path d="M 2.328125 4.222656 L 27.734375 4.222656 L 27.734375 24.542969 L 2.328125 24.542969 Z M 2.328125 4.222656 " clip-rule="nonzero"/></clipPath></defs><g clip-path="url(#id1)"><path fill="rgb(13.729858%, 12.159729%, 12.548828%)" d="M 27.5 7.53125 L 24.464844 4.542969 C 24.15625 4.238281 23.65625 4.238281 23.347656 4.542969 L 11.035156 16.667969 L 6.824219 12.523438 C 6.527344 12.230469 6 12.230469 5.703125 12.523438 L 2.640625 15.539062 C 2.332031 15.84375 2.332031 16.335938 2.640625 16.640625 L 10.445312 24.324219 C 10.59375 24.472656 10.796875 24.554688 11.007812 24.554688 C 11.214844 24.554688 11.417969 24.472656 11.566406 24.324219 L 27.5 8.632812 C 27.648438 8.488281 27.734375 8.289062 27.734375 8.082031 C 27.734375 7.875 27.648438 7.679688 27.5 7.53125 Z M 27.5 7.53125 " fill-opacity="1" fill-rule="nonzero"/></g></svg>'
            td.append(svg);
            fila.append(td);
            tabla.append(fila);
        }
    }
}

function SeleccionarIngrediente(row){
    var svg = row.querySelector('svg');
    if(svg.hasAttribute('hidden')){
        svg.removeAttribute('hidden');
        var json = ObtenerCookie("IDs");
        if(json != null){
            var lista = JSON.parse(json);
            lista.seleccionados.push(row.getAttribute('data-id'));
            crearCookie("IDs",JSON.stringify(lista))
        }
    }
    else{
        svg.setAttribute('hidden','true');
        var json = ObtenerCookie("IDs");
        if(json != null){
            var lista = JSON.parse(json);
            lista = eliminarID(row.getAttribute('data-id'),lista);
            crearCookie("IDs",JSON.stringify(lista))
        }
    }
}


function ObtenerCookie(cookieName) {
    var cookieValue = null;
    var cookieString = document.cookie;
    var cookies = cookieString.split(';');

    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();

        if (cookie.startsWith(cookieName + '=')) {
        cookieValue = cookie.substring(cookieName.length + 1);
        break;
        }
    }

    return cookieValue;
}

function crearCookie(nombre, valor, diasExpiracion) {
    var fechaExpiracion = new Date();
    fechaExpiracion.setDate(fechaExpiracion.getDate() + diasExpiracion);
    var cookieString = nombre + '=' + valor + '; expires=' + fechaExpiracion.toUTCString() + '; path=/';
    document.cookie = cookieString;
}

function eliminarID(id, lista){
    var indice = lista.seleccionados.indexOf(String(id));
    if (indice !== -1) {
        lista.seleccionados.splice(indice, 1);
    }
    return lista
}

function isSeleccionado(id){
    var lista = JSON.parse(ObtenerCookie("IDs"));
    var indice = lista.seleccionados.indexOf(String(id))
    if(indice !== -1)
        return true
    else
        return false
}

function eliminarSeleccion(){
    if(ObtenerCookie("IDs") != null){
        var json = {
            seleccionados: []
        };
        crearCookie("IDs",JSON.stringify(json),15);
    }
    BuscarIngrediente(null);
}

function switchReceta(button){
    var json = ObtenerCookie("recetas");
    var lista = json ? JSON.parse(json) : [];
    if (button.getAttribute("saved") == "False") {
      lista.push(button.getAttribute("data-id"));
      crearCookie("recetas", JSON.stringify(lista));
      button.classList.remove("button-bg");
      button.setAttribute("saved","True");
      button.textContent = "Receta guardada"
    } else {
      lista = lista.filter((rec) => rec !== button.getAttribute("data-id"));
      crearCookie("recetas", JSON.stringify(lista));
      button.classList.add("button-bg");
      button.setAttribute("saved","False");
      button.textContent = "Guardar receta"
    }
}

function shareRecipe(){
    var base_url = window.location.href
    var share = document.getElementById("compartirReceta")

    navigator.clipboard.writeText(base_url + share.getAttribute("data-id"))

    alert("Copiada receta")
}

//Añadir listener a los botones
var btn_eliminar = document.getElementById("eliminarSeleccion");
var btn_guardar = document.getElementsByClassName("save-btn");
var btn_compartir = document.getElementsByClassName("share-btn");
if(btn_eliminar != null)
    btn_eliminar.addEventListener("click",eliminarSeleccion);
if(btn_guardar != null){
    for (const boton of btn_guardar) {
        if(boton.getAttribute("saved") == "True"){
            boton.classList.remove("button-bg");
            boton.textContent = "Receta guardada";
        }
        else{
            boton.classList.add("button-bg");
            boton.textContent = "Guardar receta";
        }
        boton.addEventListener("click", (e) => {
            switchReceta(e.target)
            if(e.target.getAttribute("origin") == "resultado")
                document.location.reload()
        });
    }
}
if(btn_compartir != null){}
for (const boton of btn_guardar) {
    boton.addEventListener("click", (e) => {
        e.target.addEventListener("click",shareRecipe)
    });
}
