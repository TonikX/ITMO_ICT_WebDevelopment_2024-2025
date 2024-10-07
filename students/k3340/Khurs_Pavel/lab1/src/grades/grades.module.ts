import { Module } from '@nestjs/common';
import { GradesGateway } from './grades.gateway';

@Module({
  providers: [GradesGateway]
})
export class GradesModule {}
