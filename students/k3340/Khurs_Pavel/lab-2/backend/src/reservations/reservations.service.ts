import {
  Injectable,
  NotFoundException,
  ForbiddenException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { CreateReservationDto } from '@/src/reservations/dto/create-reservation.dto';
import { UpdateReservationDto } from '@/src/reservations/dto/update-reservation.dto';
import { Reservation } from '@/src/reservations/entities/reservation.entity/reservation.entity';
import { ToursService } from '@/src/tours/tours.service';
import { UsersService } from '@/src/users/users.service';
import { Repository } from 'typeorm';

@Injectable()
export class ReservationsService {
  constructor(
    @InjectRepository(Reservation)
    private reservationsRepository: Repository<Reservation>,
    private usersService: UsersService,
    private toursService: ToursService,
  ) {}

  async create(
    createReservationDto: CreateReservationDto,
    userId: number,
  ): Promise<Reservation> {
    const user = await this.usersService.findOneById(userId);
    const tour = await this.toursService.findOne(createReservationDto.tourId);

    const reservation = this.reservationsRepository.create({
      user,
      tour,
      status: 'pending',
    });

    return this.reservationsRepository.save(reservation);
  }

  async findAllByUser(userId: number): Promise<Reservation[]> {
    return this.reservationsRepository.find({
      where: { user: { id: userId } },
      relations: ['tour'],
    });
  }

  async findOneByUser(id: number, userId: number): Promise<Reservation> {
    const reservation = await this.reservationsRepository.findOne({
      where: { id, user: { id: userId } },
      relations: ['tour'],
    });

    if (!reservation) {
      throw new NotFoundException('Резервирование не найдено');
    }

    return reservation;
  }

  async update(
    id: number,
    updateReservationDto: UpdateReservationDto,
    userId: number,
  ): Promise<Reservation> {
    const reservation = await this.findOneByUser(id, userId);

    if (reservation.status === 'confirmed') {
      throw new ForbiddenException(
        'Нельзя изменять подтвержденное резервирование',
      );
    }

    Object.assign(reservation, updateReservationDto);
    return this.reservationsRepository.save(reservation);
  }

  async remove(id: number, userId: number): Promise<void> {
    const reservation = await this.findOneByUser(id, userId);

    if (reservation.status === 'confirmed') {
      throw new ForbiddenException(
        'Нельзя удалять подтвержденное резервирование',
      );
    }

    await this.reservationsRepository.delete(id);
  }

  async confirmReservation(id: number): Promise<Reservation> {
    const reservation = await this.reservationsRepository.findOne({
      where: { id },
      relations: ['user', 'tour'],
    });

    if (!reservation) {
      throw new NotFoundException('Резервирование не найдено');
    }

    reservation.status = 'confirmed';
    return this.reservationsRepository.save(reservation);
  }

  async findAll(): Promise<Reservation[]> {
    return this.reservationsRepository.find({
      relations: ['user', 'tour'],
    });
  }
}
