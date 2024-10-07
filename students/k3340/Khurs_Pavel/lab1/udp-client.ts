import * as dgram from 'dgram';

const client = dgram.createSocket('udp4');
const message = Buffer.from('Hello, server');

client.send(message, 41234, 'localhost', (err) => {
  if (err) {
    console.error('Ошибка при отправке сообщения:', err);
    client.close();
  } else {
    console.log('Сообщение отправлено серверу');
  }
});

client.on('message', (msg) => {
  console.log(`Ответ от сервера: ${msg}`);
  client.close();
});

client.on('error', (err) => {
  console.error(`Ошибка клиента:\n${err.stack}`);
  client.close();
});
