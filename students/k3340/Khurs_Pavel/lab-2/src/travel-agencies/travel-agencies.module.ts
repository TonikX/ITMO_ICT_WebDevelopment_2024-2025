import { Module } from '@nestjs/common';

import { TypeOrmModule } from '@nestjs/typeorm';
import { TravelAgency } from '@/src/travel-agencies/entities/travel-agency.entity/travel-agency.entity';
import { TravelAgenciesController } from '@/src/travel-agencies/travel-agencies.controller';
import { TravelAgenciesService } from '@/src/travel-agencies/travel-agencies.service';

@Module({
  imports: [TypeOrmModule.forFeature([TravelAgency])],
  controllers: [TravelAgenciesController],
  providers: [TravelAgenciesService],
  exports: [TravelAgenciesService, TypeOrmModule],
})
export class TravelAgenciesModule {}
