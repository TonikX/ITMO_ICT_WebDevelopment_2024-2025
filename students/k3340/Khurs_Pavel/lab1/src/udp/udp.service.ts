import { Injectable, OnModuleInit } from '@nestjs/common';
import * as dgram from 'dgram';

@Injectable()
export class UdpService implements OnModuleInit {
  private server: dgram.Socket;

  onModuleInit() {
    this.server = dgram.createSocket('udp4');

    this.server.on('message', (msg, rinfo) => {
      console.log(
        `Сообщение от клиента ${rinfo.address}:${rinfo.port} - ${msg}`,
      );
      const response = Buffer.from('Hello, client');
      this.server.send(
        response,
        0,
        response.length,
        rinfo.port,
        rinfo.address,
        (err) => {
          if (err) {
            console.error('Ошибка при отправке ответа:', err);
          } else {
            console.log('Ответ отправлен клиенту');
          }
        },
      );
    });

    this.server.on('error', (err) => {
      console.error(`Ошибка сервера:\n${err.stack}`);
      this.server.close();
    });

    this.server.bind(41234, () => {
      console.log('UDP сервер запущен на порту 41234');
    });
  }
}
