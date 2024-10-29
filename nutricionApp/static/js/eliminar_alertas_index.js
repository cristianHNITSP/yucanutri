function cerrarAlertas() {
    setTimeout(function () {
        var alertas = document.querySelectorAll('.alert-dismissible'); // Seleccionar todas las alertas con botón de cierre
        var contenedor = document.querySelector('.mensajes'); // Seleccionar el contenedor de las alertas

        alertas.forEach(function (alerta) {
            alerta.classList.remove('show'); // Ocultar la alerta
            setTimeout(function () {
                alerta.remove(); // Eliminar la alerta del DOM después de la animación
                if (contenedor && contenedor.querySelectorAll('.alert-dismissible').length === 0) {
                    contenedor.remove(); // Eliminar el contenedor si no quedan alertas
                }
            }, 240); // Esperar 240 ms después de la animación de desvanecimiento antes de eliminar el elemento
        });
    }, 4500); // Esperar 5.5 segundos antes de ejecutar la función
}

cerrarAlertas();
