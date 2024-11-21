document.addEventListener("DOMContentLoaded", function () {
    const productosTabla = document.getElementById("productos-tabla").querySelector("tbody");

    // Función para cargar productos desde la API
    async function cargarProductos() {
        try {
            const response = await fetch('/api/productos/');
            if (!response.ok) {
                throw new Error("Error al cargar productos");
            }
            const productos = await response.json();

            // Vaciar la tabla antes de llenarla
            productosTabla.innerHTML = "";

            if (productos.length === 0) {
                // Mostrar un mensaje si no hay productos
                const fila = document.createElement("tr");
                fila.innerHTML = `
                    <td colspan="3" style="text-align: center;">No hay productos disponibles.</td>
                `;
                productosTabla.appendChild(fila);
                return;
            }

            // Crear filas para cada producto
            productos.forEach(producto => {
                const fila = document.createElement("tr");

                fila.innerHTML = `
                    <td>${producto.nombre}</td>
                    <td>${producto.stock}</td>
                    <td>$${producto.precio}</td>
                `;

                productosTabla.appendChild(fila);
            });
        } catch (error) {
            productosTabla.innerHTML = `
                <tr>
                    <td colspan="3" style="text-align: center;">Error al cargar productos. Intenta de nuevo más tarde.</td>
                </tr>
            `;
            console.error(error);
        }
    }

    // Cargar productos al cargar la página
    cargarProductos();
});
