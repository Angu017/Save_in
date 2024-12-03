onApprove: function (data, actions) {
    return actions.order.capture().then(function (details) {
        window.location.href = "/thank_you.html"; // Redirige a tu página de agradecimiento
    });
},
