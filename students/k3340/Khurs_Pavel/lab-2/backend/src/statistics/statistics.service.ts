import { Reservation } from '@/src/reservations/entities/reservation.entity/reservation.entity';
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';

import { Repository } from 'typeorm';

@Injectable()
export class StatisticsService {
  constructor(
    @InjectRepository(Reservation)
    private readonly reservationRepository: Repository<Reservation>,
  ) {}

  async getSalesByCountry() {
    const data = await this.reservationRepository
      .createQueryBuilder('reservation')
      .leftJoin('reservation.tour', 'tour')
      .select('tour.country', 'country')
      .addSelect('COUNT(reservation.id)', 'sales')
      .where('reservation.isConfirmed = :isConfirmed', { isConfirmed: true })
      .groupBy('tour.country')
      .getRawMany();

    return data;
  }
}
