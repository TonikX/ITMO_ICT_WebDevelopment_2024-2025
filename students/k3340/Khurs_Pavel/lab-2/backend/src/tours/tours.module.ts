import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Tour } from '@/src/tours/entities/tour.entity/tour.entity';
import { ToursController } from '@/src/tours/tours.controller';
import { ToursService } from '@/src/tours/tours.service';
import { TravelAgenciesModule } from '@/src/travel-agencies/travel-agencies.module';

@Module({
  imports: [TypeOrmModule.forFeature([Tour]), TravelAgenciesModule],
  providers: [ToursService],
  controllers: [ToursController],
  exports: [ToursService],
})
export class ToursModule {}
