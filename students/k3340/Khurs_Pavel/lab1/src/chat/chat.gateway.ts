import {
  WebSocketGateway,
  WebSocketServer,
  SubscribeMessage,
  MessageBody,
  ConnectedSocket,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { PrismaService } from 'src/prisma/prisma.service';

@WebSocketGateway()
export class ChatGateway {
  @WebSocketServer()
  server: Server;

  constructor(private prisma: PrismaService) {}

  @SubscribeMessage('message')
  async handleMessage(@MessageBody() data: string) {
    await this.prisma.message.create({
      data: {
        content: data,
      },
    });

    this.server.emit('message', data);
  }

  @SubscribeMessage('getMessages')
  async handleGetMessages(@ConnectedSocket() client: Socket) {
    const messages = await this.prisma.message.findMany({
      orderBy: { createdAt: 'asc' },
      take: 50,
    });

    client.emit('allMessages', messages);
  }
}
