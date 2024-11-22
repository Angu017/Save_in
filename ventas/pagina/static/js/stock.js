document.addEventListener('DOMContentLoaded', function() {
    // Función para obtener los productos desde el backend
    function obtenerProductos() {
        fetch('/api/productos_mayor_stock/')  // URL para obtener los productos con mayor stock
            .then(response => response.json())
            .then(data => {
                const tbody = document.querySelector('table tbody');
                tbody.innerHTML = '';  // Limpiar la tabla antes de agregar los nuevos productos

                // Recorrer los productos y agregarlos a la tabla
                data.forEach(producto => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${producto.id}</td>
                        <td>${producto.nombre}</td>
                        <td>${producto.stock}</td>
                    `;
                    tbody.appendChild(row);
                });
            })
            .catch(error => {
                console.error('Error al obtener los productos:', error);
            });
    }

    // Llamamos a la función para cargar los productos al cargar la página
    obtenerProductos();
});
