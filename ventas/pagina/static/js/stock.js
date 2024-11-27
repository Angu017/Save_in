document.addEventListener('DOMContentLoaded', function() {
    // Función para obtener los productos desde el backend
    function obtenerProductos() {
        fetch('/api/productos_mayor_stock/')  // URL para obtener los productos
            .then(response => response.json())
            .then(data => {
                console.log(data);  // Agregar esta línea para ver la respuesta en la consola

                const tbodyStock = document.querySelector('table:nth-of-type(1) tbody');
                const tbodyVencimiento = document.querySelector('table:nth-of-type(2) tbody');
                
                // Limpiar las tablas antes de agregar los nuevos productos
                tbodyStock.innerHTML = '';
                tbodyVencimiento.innerHTML = '';

                // Agregar productos con mayor stock
                if (data.productos_mayor_stock) {
                    data.productos_mayor_stock.forEach(producto => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${producto.id}</td>
                            <td>${producto.nombre}</td>
                            <td>${producto.marca}</td>
                            <td>${producto.categoria}</td>
                            <td>${producto.stock}</td>
                        `;
                        tbodyStock.appendChild(row);
                    });
                } else {
                    console.error('No se encontraron productos con mayor stock.');
                }

                // Agregar productos con la fecha de vencimiento más cercana
                if (data.productos_fecha_vencimiento) {
                    data.productos_fecha_vencimiento.forEach(producto => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${producto.id}</td>
                            <td>${producto.nombre}</td>
                            <td>${producto.fecha_vencimiento}</td>
                            <td>${producto.stock}</td>
                        `;
                        tbodyVencimiento.appendChild(row);
                    });
                } else {
                    console.error('No se encontraron productos con fecha de vencimiento.');
                }
            })
            .catch(error => {
                console.error('Error al obtener los productos:', error);
            });
    }

    // Llamamos a la función para cargar los productos al cargar la página
    obtenerProductos();
});
