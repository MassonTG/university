// services/notifications/server.js
const { Kafka } = require('kafkajs');

const kafka = new Kafka({ clientId: 'notifications', brokers: ['kafka:9092'] });
const consumer = kafka.consumer({ groupId: 'notifications-group' });
const producer = kafka.producer();

async function start() {
  await producer.connect();
  await consumer.connect();
  await consumer.subscribe({ topic: 'orders.events' });

  await consumer.run({
    eachMessage: async ({ message }) => {
      const key = message.key?.toString();
      if (key !== 'PaymentCaptured') return;

      const payment = JSON.parse(message.value.toString());
      const email = { orderId: payment.orderId, to: 'user@test.com', ts: Date.now() };

      // Simulated send
      console.log('Sending email', email);

      await producer.send({
        topic: 'orders.events',
        messages: [{ key: 'EmailSent', value: JSON.stringify(email) }],
      });
    },
  });
}

start().catch(err => {
  console.error('Notifications start error', err);
  process.exit(1);
});
