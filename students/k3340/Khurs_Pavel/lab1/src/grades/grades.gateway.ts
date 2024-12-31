import {
  WebSocketGateway,
  WebSocketServer,
  SubscribeMessage,
  MessageBody,
  ConnectedSocket,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { PrismaService } from '../prisma/prisma.service';

@WebSocketGateway({ namespace: '/grades' })
export class GradesGateway {
  @WebSocketServer()
  server: Server;

  constructor(private prisma: PrismaService) {}

  @SubscribeMessage('getGrades')
  async handleGetGrades(@ConnectedSocket() client: Socket) {
    const grades = await this.prisma.grade.findMany({
      orderBy: { createdAt: 'desc' },
    });

    client.emit('allGrades', grades);
  }

  @SubscribeMessage('addGrade')
  async handleAddGrade(
    @MessageBody() data: { subject: string; score: number },
    @ConnectedSocket() client: Socket,
  ) {
    const { subject, score } = data;

    if (
      !subject ||
      typeof subject !== 'string' ||
      !score ||
      typeof score !== 'number'
    ) {
      client.emit('error', { message: 'Неверные данные' });
      return;
    }

    const newGrade = await this.prisma.grade.create({
      data: {
        subject,
        score,
      },
    });

    this.server.emit('newGrade', newGrade);
  }
}
