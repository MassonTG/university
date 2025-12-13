// services/orders/server.js
const express = require('express');
const { Kafka } = require('kafkajs');

const app = express();
app.use(express.json());

const kafka = new Kafka({ clientId: 'orders', brokers: ['kafka:9092'] });
const producer = kafka.producer();

let orders = [];
let nextId = 1;

async function start() {
  await producer.connect();
  console.log('Orders producer connected');
}

app.post('/orders', async (req, res) => {
  const { userId, itemId, qty } = req.body || {};
  const order = { orderId: nextId++, userId, itemId, qty, ts: Date.now() };
  orders.push(order);

  await producer.send({
    topic: 'orders.events',
    messages: [{ key: 'OrderCreated', value: JSON.stringify(order) }],
  });

  res.status(201).json(order);
});

app.listen(5002, () => console.log('Orders service running on port 5002'));

start().catch(err => {
  console.error('Orders start error', err);
  process.exit(1);
});
