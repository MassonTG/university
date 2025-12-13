// services/billing/server.js
const { Kafka } = require('kafkajs');

const kafka = new Kafka({ clientId: 'billing', brokers: ['kafka:9092'] });
const consumer = kafka.consumer({ groupId: 'billing-group' });
const producer = kafka.producer();

// In-memory idempotency store (by orderId)
const processedOrderIds = new Set();

async function start() {
  await producer.connect();
  await consumer.connect();
  await consumer.subscribe({ topic: 'orders.events' });

  await consumer.run({
    eachMessage: async ({ message }) => {
      const key = message.key?.toString();
      if (key !== 'OrderCreated') return;

      const order = JSON.parse(message.value.toString());
      const { orderId } = order;

      if (processedOrderIds.has(orderId)) {
        console.log('Billing skipped duplicate OrderCreated for orderId', orderId);
        return;
      }

      processedOrderIds.add(orderId);

      const payment = { orderId, amount: 100, ts: Date.now() };
      await producer.send({
        topic: 'orders.events',
        messages: [{ key: 'PaymentCaptured', value: JSON.stringify(payment) }],
      });

      console.log('Billing processed', payment);
    },
  });
}

start().catch(err => {
  console.error('Billing start error', err);
  process.exit(1);
});
