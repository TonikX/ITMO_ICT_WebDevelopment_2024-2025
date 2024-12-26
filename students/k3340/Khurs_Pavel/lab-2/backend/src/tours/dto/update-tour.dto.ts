import { PartialType } from '@nestjs/mapped-types';
import { CreateTourDto } from '@/src/tours/dto/create-tour.dto';

export class UpdateTourDto extends PartialType(CreateTourDto) {}
