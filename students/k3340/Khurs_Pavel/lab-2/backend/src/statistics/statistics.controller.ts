import { Controller, Get } from '@nestjs/common';
import { StatisticsService } from './statistics.service';

@Controller('statistics')
export class StatisticsController {
  constructor(private readonly statisticsService: StatisticsService) {}

  @Get('sales-by-country')
  async getSalesByCountry() {
    return this.statisticsService.getSalesByCountry();
  }
}
