let currentPage = 1;  // Página inicial
const usersPerPage = 5;  // Mostrar 5 usuarios por página

// Mostrar los usuarios en la tabla
function displayUsers(data) {
    const tableBody = document.getElementById('userTableBody');
    tableBody.innerHTML = '';  // Limpiar la tabla antes de agregar nuevos usuarios

    data.usuarios.forEach(user => {
        const row = document.createElement('tr');
        
        // Mostrar los roles desde la base de datos (modificado)
        const roles = user.roles.map(role => {
            return `
                <p><input type="radio" name="role-${user.username}" value="${role}" ${user.role === role ? 'checked' : ''} onclick="changeRole('${user.username}', '${role}')"> ${role}</p>
            `;
        }).join('');  // Crear una lista de radios para seleccionar el rol

        row.innerHTML = `
            <td>${user.username}</td>
            <td>
                <button class="accordion">Seleccionar Rol</button>
                <div class="panel">
                    ${roles}
                </div>
            </td>
            <td>
                <button class="btn eliminar" onclick="deleteUser('${user.username}')">
                    <span class="material-icons">delete</span> Eliminar
                </button>
            </td>
        `;
        tableBody.appendChild(row);
    });

    // Actualizar la paginación
    updatePagination(data.total_pages, data.current_page);
    setAccordionEventListeners();  // Configurar los eventos del acordeón
}

// Configurar el acordeón para abrir y cerrar
function setAccordionEventListeners() {
    const accordions = document.getElementsByClassName('accordion');
    Array.from(accordions).forEach(accordion => {
        accordion.addEventListener('click', function() {
            this.classList.toggle('active');
            const panel = this.nextElementSibling;
            if (panel.style.display === 'block') {
                panel.style.display = 'none';
            } else {
                panel.style.display = 'block';
            }
        });
    });
}

// Manejar la paginación
function updatePagination(totalPages, currentPage) {
    const paginationDiv = document.getElementById('pagination');
    paginationDiv.innerHTML = ''; // Limpiar la paginación

    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement('button');
        button.innerText = i;
        button.onclick = () => {
            currentPage = i;  // Actualizar la página actual
            fetchUsers();  // Obtener usuarios de la página seleccionada
        };
        paginationDiv.appendChild(button);
    }
}

// Obtener los usuarios de la API con filtros
function fetchUsers() {
    const role = document.getElementById('roleFilter').value;  // Obtener el filtro de rol
    const searchQuery = document.getElementById('searchInput').value.trim();  // Obtener el valor de la búsqueda

    // Construir la URL para obtener los usuarios con los filtros
    let url = `/api/usuarios/?page=${currentPage}`;

    if (role) {
        url += `&role=${role}`;
    }

    if (searchQuery) {
        url += `&search=${searchQuery}`;  // Añadir filtro de búsqueda
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            displayUsers(data);  // Mostrar los usuarios en la tabla
        })
        .catch(error => console.error('Error fetching users:', error));
}

// Función para eliminar un usuario
function deleteUser(username) {
    fetch(`/api/usuarios/${username}/eliminar/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Usuario eliminado correctamente');
            fetchUsers();  // Recargar los usuarios después de eliminar uno
        } else {
            alert('Error al eliminar el usuario');
        }
    })
    .catch(error => console.error('Error deleting user:', error));
}

// Función para cambiar el rol de un usuario
function changeRole(username, role) {
    fetch(`/api/usuarios/${username}/cambiar_rol/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: `role=${role}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Rol actualizado correctamente');
        } else {
            alert('Error al actualizar el rol');
        }
    })
    .catch(error => console.error('Error changing role:', error));
}

// Obtener el valor de la cookie CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Función para la barra de búsqueda
function searchUser() {
    currentPage = 1;  // Reiniciar a la primera página al hacer búsqueda
    fetchUsers();  // Llamar a fetchUsers para obtener los usuarios con el filtro de búsqueda
}

// Función para aplicar el filtro de roles
function applyFilter() {
    currentPage = 1;  // Reiniciar a la primera página al aplicar el filtro de rol
    fetchUsers();  // Llamar a fetchUsers para obtener los usuarios con el filtro de rol
}

// Inicializar la página con los usuarios de la primera página
fetchUsers();

// Event listener para la búsqueda
document.getElementById('searchInput').addEventListener('input', searchUser);

// Event listener para el filtro de roles
document.getElementById('roleFilter').addEventListener('change', applyFilter);
