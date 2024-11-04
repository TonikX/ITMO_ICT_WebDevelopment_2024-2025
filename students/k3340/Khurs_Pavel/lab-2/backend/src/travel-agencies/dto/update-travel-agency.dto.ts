import { PartialType } from '@nestjs/mapped-types';
import { CreateTravelAgencyDto } from '@/src/travel-agencies/dto/create-travel-agency.dto';

export class UpdateTravelAgencyDto extends PartialType(CreateTravelAgencyDto) {}
