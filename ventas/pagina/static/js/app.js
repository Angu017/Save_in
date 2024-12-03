window.paypal
    .Buttons({
        style: {
            shape: "pill",
            layout: "vertical",
            color: "blue",
            label: "pay",
        },

        // Configuración estática para un monto fijo
        createOrder: function (data, actions) {
            return actions.order.create({
                purchase_units: [
                    {
                        amount: {
                            value: "15000", // Monto fijo
                            currency_code: "CLP", // Moneda en CLP
                        },
                    },
                ],
            });
        },

        // Manejo del pago cuando el usuario aprueba
        onApprove: function (data, actions) {
            return actions.order
                .capture()
                .then(function (details) {
                    // Muestra un mensaje de éxito
                    alert("Pago completado con éxito por " + details.payer.name.given_name);
                    console.log("Detalles del pago:", details);
                })
                .catch(function (error) {
                    // Manejo de errores en la captura
                    console.error("Error al capturar el pago:", error);
                    alert("Hubo un problema al completar el pago. Inténtalo nuevamente.");
                });
        },

        // Manejo de errores en el proceso de pago
        onError: function (err) {
            console.error("Error en PayPal:", err);
            alert("Ocurrió un error. Por favor, inténtalo más tarde.");
        },
    })
    .render("#paypal-button-container");
