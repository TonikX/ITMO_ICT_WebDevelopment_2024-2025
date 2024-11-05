import { Module } from '@nestjs/common';
import { StatisticsController } from './statistics.controller';
import { StatisticsService } from './statistics.service';
import { Reservation } from '@/src/reservations/entities/reservation.entity/reservation.entity';
import { Tour } from '@/src/tours/entities/tour.entity/tour.entity';
import { TypeOrmModule } from '@nestjs/typeorm';

@Module({
  imports: [TypeOrmModule.forFeature([Reservation, Tour])],
  controllers: [StatisticsController],
  providers: [StatisticsService],
})
export class StatisticsModule {}
