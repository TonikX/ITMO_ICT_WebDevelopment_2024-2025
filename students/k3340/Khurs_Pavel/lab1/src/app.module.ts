import { Module } from '@nestjs/common';
import { UdpModule } from './udp/udp.module';
import { TcpModule } from './tcp/tcp.module';
import { HttpController } from './http/http.controller';
import { HttpModule } from './http/http.module';
import { ChatModule } from './chat/chat.module';
import { PrismaModule } from './prisma/prisma.module';
import { GradesModule } from './grades/grades.module';

@Module({
  imports: [
    UdpModule,
    TcpModule,
    HttpModule,
    ChatModule,
    PrismaModule,
    GradesModule,
  ],
  controllers: [HttpController],
})
export class AppModule {}
