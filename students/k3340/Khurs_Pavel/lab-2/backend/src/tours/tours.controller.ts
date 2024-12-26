import {
  Controller,
  UseGuards,
  Post,
  Body,
  Patch,
  Param,
  Delete,
  Get,
} from '@nestjs/common';
import { Roles } from '@/src/auth/decorators/roles.decorator';
import { JwtAuthGuard } from '@/src/auth/guards/jwt-auth.guard';
import { CreateTourDto } from '@/src/tours/dto/create-tour.dto';
import { UpdateTourDto } from '@/src/tours/dto/update-tour.dto';
import { ToursService } from '@/src/tours/tours.service';

@Controller('tours')
export class ToursController {
  constructor(private readonly toursService: ToursService) {}

  @UseGuards(JwtAuthGuard)
  @Roles('admin')
  @Post()
  async create(@Body() createTourDto: CreateTourDto) {
    return this.toursService.create(createTourDto);
  }

  @UseGuards(JwtAuthGuard)
  @Roles('admin')
  @Patch(':id')
  async update(@Param('id') id: string, @Body() updateTourDto: UpdateTourDto) {
    return this.toursService.update(+id, updateTourDto);
  }

  @UseGuards(JwtAuthGuard)
  @Roles('admin')
  @Delete(':id')
  async remove(@Param('id') id: string) {
    return this.toursService.remove(+id);
  }

  @Get()
  async findAll() {
    return this.toursService.findAll();
  }

  @Get(':id')
  async findOne(@Param('id') id: string) {
    return this.toursService.findOne(+id);
  }
}
