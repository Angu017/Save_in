document.addEventListener("DOMContentLoaded", function () {
    const productosTabla = document.querySelector("tbody");

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
                    <td colspan="4" style="text-align: center;">No hay productos disponibles.</td>
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
                    <td>
                        <button class="btn-delete" data-id="${producto.id}">
                            <i class="fas fa-trash-alt"></i> Eliminar
                        </button>
                    </td>
                `;

                productosTabla.appendChild(fila);
            });
        } catch (error) {
            productosTabla.innerHTML = `
                <tr>
                    <td colspan="4" style="text-align: center;">Error al cargar productos. Intenta de nuevo más tarde.</td>
                </tr>
            `;
            console.error(error);
        }
    }

    // Delegación de eventos para manejar clics en los botones de eliminar
    productosTabla.addEventListener("click", async function (event) {
        if (event.target.closest(".btn-delete")) {
            const button = event.target.closest(".btn-delete");
            const productoId = button.getAttribute("data-id");

            if (confirm("¿Estás seguro de que deseas eliminar este producto?")) {
                try {
                    const response = await fetch(`/eliminar_producto/${productoId}/`, {
                        method: "DELETE",
                        headers: {
                            "Content-Type": "application/json",
                        },
                    });

                    if (response.ok) {
                        alert("Producto eliminado correctamente.");
                        // Recargar la lista de productos
                        cargarProductos();
                    } else {
                        const errorData = await response.json();
                        alert(`Error al eliminar: ${errorData.message}`);
                    }
                } catch (error) {
                    console.error("Error:", error);
                    alert("Hubo un problema al eliminar el producto.");
                }
            }
        }
    });

    // Cargar productos al cargar la página
    cargarProductos();
});
