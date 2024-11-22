const express = require('express');
const axios = require('axios');
const dotenv = require('dotenv');
const cors = require('cors');  // Importa CORS

dotenv.config(); // Carga las variables de entorno
const app = express();

app.use(cors()); // Habilita CORS

// Usa las credenciales de PayPal desde las variables de entorno
const CLIENT_ID = process.env.PAYPAL_CLIENT_ID;
const CLIENT_SECRET = process.env.PAYPAL_SECRET_KEY;

// Generar un token de acceso con las credenciales
async function getAccessToken() {
    const response = await axios.post('https://api.sandbox.paypal.com/v1/oauth2/token', null, {
        headers: {
            'Authorization': `Basic ${Buffer.from(CLIENT_ID + ':' + CLIENT_SECRET).toString('base64')}`,
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        params: {
            grant_type: 'client_credentials'
        }
    });
    return response.data.access_token;
}

// Crear una orden en PayPal
app.post('/create-order', async (req, res) => {
    try {
        const accessToken = await getAccessToken();
        const response = await axios.post('https://api.sandbox.paypal.com/v2/checkout/orders', {
            intent: 'CAPTURE',
            purchase_units: [{
                amount: {
                    value: '5000'  // Monto de la compra en CLP
                }
            }]
        }, {
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
            }
        });

        res.json({ orderID: response.data.id });
    } catch (error) {
        console.error('Error al crear la orden:', error);
        res.status(500).send('Error en la creación de la orden');
    }
});

// Capturar el pago después de la aprobación del usuario
app.post('/capture-payment', async (req, res) => {
    try {
        const accessToken = await getAccessToken();
        const { orderID } = req.body;

        const response = await axios.post(`https://api.sandbox.paypal.com/v2/checkout/orders/${orderID}/capture`, {}, {
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
            }
        });

        res.json(response.data);
    } catch (error) {
        console.error('Error al capturar el pago:', error);
        res.status(500).send('Error al capturar el pago');
    }
});

app.listen(3000, () => {
    console.log('Servidor corriendo en el puerto 3000');
});
