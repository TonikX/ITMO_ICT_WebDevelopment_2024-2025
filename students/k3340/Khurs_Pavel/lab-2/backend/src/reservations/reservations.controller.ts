import {
  Controller,
  Get,
  Post,
  Body,
  Param,
  Patch,
  Delete,
  UseGuards,
  Request,
} from '@nestjs/common';
import { Roles } from '@/src/auth/decorators/roles.decorator';
import { JwtAuthGuard } from '@/src/auth/guards/jwt-auth.guard';
import { RolesGuard } from '@/src/auth/guards/roles.guard';
import { CreateReservationDto } from '@/src/reservations/dto/create-reservation.dto';
import { UpdateReservationDto } from '@/src/reservations/dto/update-reservation.dto';
import { ReservationsService } from '@/src/reservations/reservations.service';

@Controller('reservations')
export class ReservationsController {
  constructor(private readonly reservationsService: ReservationsService) {}

  @UseGuards(JwtAuthGuard)
  @Post()
  async create(
    @Body() createReservationDto: CreateReservationDto,
    @Request() req,
  ) {
    const userId = req.user.userId;
    return this.reservationsService.create(createReservationDto, userId);
  }

  @UseGuards(JwtAuthGuard)
  @Get()
  async findAllByUser(@Request() req) {
    const userId = req.user.userId;
    return this.reservationsService.findAllByUser(userId);
  }

  @UseGuards(JwtAuthGuard)
  @Get(':id')
  async findOne(@Param('id') id: string, @Request() req) {
    const userId = req.user.userId;
    return this.reservationsService.findOneByUser(+id, userId);
  }

  @UseGuards(JwtAuthGuard)
  @Patch(':id')
  async update(
    @Param('id') id: string,
    @Body() updateReservationDto: UpdateReservationDto,
    @Request() req,
  ) {
    const userId = req.user.userId;
    return this.reservationsService.update(+id, updateReservationDto, userId);
  }

  @UseGuards(JwtAuthGuard)
  @Delete(':id')
  async remove(@Param('id') id: string, @Request() req) {
    const userId = req.user.userId;
    return this.reservationsService.remove(+id, userId);
  }

  // Администратор подтверждает резервирование
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @Patch('confirm/:id')
  async confirmReservation(@Param('id') id: string) {
    return this.reservationsService.confirmReservation(+id);
  }

  @UseGuards(JwtAuthGuard)
  @Roles('admin')
  @Get('all')
  async findAll() {
    return this.reservationsService.findAll();
  }
}
