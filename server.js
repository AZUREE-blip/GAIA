const express = require('express');
const app = express();
const port = 8080;
const paypal = require('@paypal/checkout-server-sdk');
require('dotenv').config(); // Load environment variables from .env file

// Middleware to parse JSON
app.use(express.json());

// Configure the PayPal environment with credentials from the .env file
let clientId = process.env.PAYPAL_CLIENT_ID;
let clientSecret = process.env.PAYPAL_SECRET;

let environment = new paypal.core.SandboxEnvironment(clientId, clientSecret);
let client = new paypal.core.PayPalHttpClient(environment);

// Default route to verify if the server is running
app.get('/', (req, res) => {
  res.send('Server is running!');
});

// Endpoint to create an order
app.post('/create-order', async (req, res) => {
  const request = new paypal.orders.OrdersCreateRequest();
  request.prefer("return=representation");
  request.requestBody({
    intent: 'CAPTURE',
    purchase_units: [{
      amount: {
        currency_code: 'USD',
        value: req.body.amount // The amount to capture from request body
      }
    }]
  });

  try {
    const order = await client.execute(request);
    res.json({ orderID: order.result.id });
  } catch (err) {
    console.error(err);
    res.status(500).send('Something went wrong while creating the order');
  }
});

// Start the server and log a message when it is running
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});

