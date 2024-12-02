document.addEventListener('DOMContentLoaded', function () {
    fetch('/editarad/')  // Cambiado la URL para que apunte a editarad
        .then(response => response.json())
        .then(data => {
            const profileData = data.profile_data;
            document.getElementById('id_username').value = profileData.username;
            document.getElementById('id_email').value = profileData.email;
            document.getElementById('id_role').value = profileData.role;
            document.getElementById('id_phone').value = profileData.phone;
            document.getElementById('id_address').value = profileData.address;
            document.getElementById('id_first_name').value = profileData.first_name;
            document.getElementById('id_last_name').value = profileData.last_name;
        });
});

document.getElementById('profileFormAd').addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = {
        username: document.getElementById('id_username').value,
        email: document.getElementById('id_email').value,
        role: document.getElementById('id_role').value,
        phone: document.getElementById('id_phone').value,
        address: document.getElementById('id_address').value,
        first_name: document.getElementById('id_first_name').value,
        last_name: document.getElementById('id_last_name').value,
    };

    fetch('/editarad/', {  // Cambiado la URL para que apunte a editarad
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,  // Asegúrate de que `csrfToken` esté definido en tu HTML
        },
        body: JSON.stringify(formData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Perfil de administrador actualizado con éxito.');
        } else {
            alert('Error al actualizar el perfil.');
        }
    });
});
