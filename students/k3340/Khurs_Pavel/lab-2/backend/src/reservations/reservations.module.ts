import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Reservation } from '@/src/reservations/entities/reservation.entity/reservation.entity';
import { ReservationsController } from '@/src/reservations/reservations.controller';
import { ReservationsService } from '@/src/reservations/reservations.service';
import { ToursModule } from '@/src/tours/tours.module';
import { UsersModule } from '@/src/users/users.module';

@Module({
  imports: [TypeOrmModule.forFeature([Reservation]), UsersModule, ToursModule],
  controllers: [ReservationsController],
  providers: [ReservationsService],
  exports: [ReservationsService],
})
export class ReservationsModule {}
