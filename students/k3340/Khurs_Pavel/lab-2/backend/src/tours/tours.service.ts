import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { CreateTourDto } from '@/src/tours/dto/create-tour.dto';
import { UpdateTourDto } from '@/src/tours/dto/update-tour.dto';
import { Tour } from '@/src/tours/entities/tour.entity/tour.entity';
import { TravelAgency } from '@/src/travel-agencies/entities/travel-agency.entity/travel-agency.entity';
import { Repository } from 'typeorm';

@Injectable()
export class ToursService {
  constructor(
    @InjectRepository(Tour)
    private toursRepository: Repository<Tour>,
    @InjectRepository(TravelAgency)
    private travelAgenciesRepository: Repository<TravelAgency>,
  ) {}

  async create(createTourDto: CreateTourDto): Promise<Tour> {
    const { travelAgencyId, ...tourData } = createTourDto;
    const travelAgency = await this.travelAgenciesRepository.findOne({
      where: { id: travelAgencyId },
    });

    if (!travelAgency) {
      throw new NotFoundException('Турагентство не найдено');
    }

    const tour = this.toursRepository.create({
      ...tourData,
      travelAgency,
    });
    return this.toursRepository.save(tour);
  }

  async findAll(): Promise<Tour[]> {
    return this.toursRepository.find({ relations: ['travelAgency'] });
  }

  async findOne(id: number): Promise<Tour> {
    const tour = await this.toursRepository.findOne({
      where: { id: id },
      relations: ['travelAgency'],
    });
    if (!tour) {
      throw new NotFoundException('Тур не найден');
    }
    return tour;
  }

  async update(id: number, updateTourDto: UpdateTourDto): Promise<Tour> {
    const tour = await this.findOne(id);
    const updatedTour = Object.assign(tour, updateTourDto);
    return this.toursRepository.save(updatedTour);
  }

  async remove(id: number): Promise<void> {
    const result = await this.toursRepository.delete(id);
    if (result.affected === 0) {
      throw new NotFoundException('Тур не найден');
    }
  }
}
