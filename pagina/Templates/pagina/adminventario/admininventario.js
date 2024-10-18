document.getElementById('back-home').addEventListener('click', function() {
    window.location.href = 'inicio.html'; // Cambia esto por la ruta correcta de tu página de inicio
});

document.getElementById('nuevo-producto').addEventListener('click', function() {
    alert("Formulario de nuevo producto será desplegado aquí.");
});

document.getElementById('sumar-stock').addEventListener('click', function() {
    alert("Ventana emergente para sumar stock.");
});

document.getElementById('restar-stock').addEventListener('click', function() {
    alert("Ventana emergente para restar stock.");
});
