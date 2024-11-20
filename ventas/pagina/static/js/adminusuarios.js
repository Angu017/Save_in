document.addEventListener("DOMContentLoaded", function() {
    var accordions = document.getElementsByClassName("accordion");

    for (var i = 0; i < accordions.length; i++) {
        accordions[i].addEventListener("click", function() {
            /* Alternar entre agregar y eliminar la clase "active" */
            this.classList.toggle("active");

            /* Alternar entre mostrar y ocultar el panel */
            var panel = this.nextElementSibling;
            if (panel.style.display === "block") {
                panel.style.display = "none";
            } else {
                panel.style.display = "block";
            }
        });
    }
});
