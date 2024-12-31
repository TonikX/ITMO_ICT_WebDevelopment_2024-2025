import {
  ClientProxyFactory,
  Transport,
  ClientProxy,
} from '@nestjs/microservices';
import * as readline from 'readline';

const client: ClientProxy = ClientProxyFactory.create({
  transport: Transport.TCP,
  options: { port: 3001 },
});

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

console.log('Выберите операцию:');
console.log('1 - Теорема Пифагора');
console.log('2 - Решение квадратного уравнения');
console.log('3 - Площадь трапеции');
console.log('4 - Площадь параллелограмма');

rl.question('Введите номер операции: ', (answer) => {
  let operation: any;
  let params = {};

  switch (answer) {
    case '1':
      operation = 'pythagoras';
      rl.question('Введите сторону a: ', (a) => {
        rl.question('Введите сторону b: ', (b) => {
          params = { a: Number(a), b: Number(b) };
          sendRequest();
        });
      });
      break;
    case '2':
      operation = 'quadratic';
      rl.question('Введите коэффициент a: ', (a) => {
        rl.question('Введите коэффициент b: ', (b) => {
          rl.question('Введите коэффициент c: ', (c) => {
            params = { a: Number(a), b: Number(b), c: Number(c) };
            sendRequest();
          });
        });
      });
      break;
    case '3':
      operation = 'trapezoid_area';
      rl.question('Введите основание a: ', (a) => {
        rl.question('Введите основание b: ', (b) => {
          rl.question('Введите высоту h: ', (h) => {
            params = { a: Number(a), b: Number(b), h: Number(h) };
            sendRequest();
          });
        });
      });
      break;
    case '4':
      operation = 'parallelogram_area';
      rl.question('Введите основание: ', (base) => {
        rl.question('Введите высоту: ', (height) => {
          params = { base: Number(base), height: Number(height) };
          sendRequest();
        });
      });
      break;
    default:
      console.log('Неверный выбор операции');
      rl.close();
      process.exit(0);
  }

  function sendRequest() {
    client.send('calculate', { operation, params }).subscribe((result) => {
      console.log('Результат:', result);
      rl.close();
      process.exit(0);
    });
  }
});
