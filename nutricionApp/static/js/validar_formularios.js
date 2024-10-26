document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('input', function () {
        // Obtenemos el valor máximo (max) del atributo del input
        const maxValue = parseFloat(this.getAttribute('max'));
        // Si existe un valor máximo definido y el valor actual es mayor al máximo
        if (!isNaN(maxValue) && this.value > maxValue) {
            this.value = maxValue;
        }
    });
});