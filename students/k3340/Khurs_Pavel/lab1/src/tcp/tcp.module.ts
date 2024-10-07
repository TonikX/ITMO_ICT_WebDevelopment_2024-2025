import { Module } from '@nestjs/common';
import { TcpController } from './tcp.controller';
import { TcpService } from './tcp.service';

@Module({
  controllers: [TcpController],
  providers: [TcpService],
})
export class TcpModule {}
