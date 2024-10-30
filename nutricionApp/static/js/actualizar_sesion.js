const tiempoDeInactividadUrl = document.getElementById('url-container').getAttribute('data-url'); // Obtener la URL
let tiempoInactividad = 0; // Contador de tiempo de inactividad
const tiempoLimite = 3600; // 1 hora de inactividad para pruebas = 3600

function manejarInactividad() {
    tiempoInactividad++;
    console.log(`Tiempo de inactividad: ${tiempoInactividad} segundos`);

    if (tiempoInactividad >= tiempoLimite) {
        // Redirigir a la ruta de cierre de sesión
        window.location.href = tiempoDeInactividadUrl; // Usar la variable definida
    }
}

function reiniciarContador() {
    tiempoInactividad = 0; // Reiniciar el contador
}

window.onload = function() {
    document.onmousemove = reiniciarContador;
    document.onkeypress = reiniciarContador;
    document.onclick = reiniciarContador;
    document.onscroll = reiniciarContador;

    setInterval(manejarInactividad, 1000); // 1000 ms = 1 segundo
};
