import {
  Controller,
  UseGuards,
  Post,
  Body,
  Get,
  Param,
  Patch,
  Delete,
} from '@nestjs/common';
import { ApiTags, ApiBearerAuth } from '@nestjs/swagger';
import { Roles } from '@/src/auth/decorators/roles.decorator';
import { JwtAuthGuard } from '@/src/auth/guards/jwt-auth.guard';
import { RolesGuard } from '@/src/auth/guards/roles.guard';
import { CreateTravelAgencyDto } from '@/src/travel-agencies/dto/create-travel-agency.dto';
import { UpdateTravelAgencyDto } from '@/src/travel-agencies/dto/update-travel-agency.dto';
import { TravelAgenciesService } from '@/src/travel-agencies/travel-agencies.service';

@ApiTags('travel-agencies')
@ApiBearerAuth()
@Controller('travel-agencies')
export class TravelAgenciesController {
  constructor(private readonly travelAgenciesService: TravelAgenciesService) {}

  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @Post()
  async create(@Body() createTravelAgencyDto: CreateTravelAgencyDto) {
    return this.travelAgenciesService.create(createTravelAgencyDto);
  }

  @Get()
  async findAll() {
    return this.travelAgenciesService.findAll();
  }

  @Get(':id')
  async findOne(@Param('id') id: string) {
    return this.travelAgenciesService.findOne(+id);
  }

  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @Patch(':id')
  async update(
    @Param('id') id: string,
    @Body() updateTravelAgencyDto: UpdateTravelAgencyDto,
  ) {
    return this.travelAgenciesService.update(+id, updateTravelAgencyDto);
  }

  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @Delete(':id')
  async remove(@Param('id') id: string) {
    return this.travelAgenciesService.remove(+id);
  }
}
