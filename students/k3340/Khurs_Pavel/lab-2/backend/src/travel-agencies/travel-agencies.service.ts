import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { CreateTravelAgencyDto } from '@/src/travel-agencies/dto/create-travel-agency.dto';
import { UpdateTravelAgencyDto } from '@/src/travel-agencies/dto/update-travel-agency.dto';
import { TravelAgency } from '@/src/travel-agencies/entities/travel-agency.entity/travel-agency.entity';

import { Repository } from 'typeorm';

@Injectable()
export class TravelAgenciesService {
  constructor(
    @InjectRepository(TravelAgency)
    private travelAgenciesRepository: Repository<TravelAgency>,
  ) {}

  async create(
    createTravelAgencyDto: CreateTravelAgencyDto,
  ): Promise<TravelAgency> {
    const travelAgency = this.travelAgenciesRepository.create(
      createTravelAgencyDto,
    );
    return this.travelAgenciesRepository.save(travelAgency);
  }

  async findAll(): Promise<TravelAgency[]> {
    return this.travelAgenciesRepository.find();
  }

  async findOne(id: number): Promise<TravelAgency> {
    const travelAgency = await this.travelAgenciesRepository.findOne({
      where: { id },
    });
    if (!travelAgency) {
      throw new NotFoundException('Турагентство не найдено');
    }
    return travelAgency;
  }

  async update(
    id: number,
    updateTravelAgencyDto: UpdateTravelAgencyDto,
  ): Promise<TravelAgency> {
    const travelAgency = await this.findOne(id);
    Object.assign(travelAgency, updateTravelAgencyDto);
    return this.travelAgenciesRepository.save(travelAgency);
  }

  async remove(id: number): Promise<void> {
    const result = await this.travelAgenciesRepository.delete(id);
    if (result.affected === 0) {
      throw new NotFoundException('Турагентство не найдено');
    }
  }
}
