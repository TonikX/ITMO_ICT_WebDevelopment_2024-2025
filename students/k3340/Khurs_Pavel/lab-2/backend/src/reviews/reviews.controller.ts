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
import { JwtAuthGuard } from '@/src/auth/guards/jwt-auth.guard';
import { CreateReviewDto } from '@/src/reviews/dto/create-review.dto';
import { UpdateReviewDto } from '@/src/reviews/dto/update-review.dto';
import { ReviewsService } from '@/src/reviews/reviews.service';

@Controller('reviews')
export class ReviewsController {
  constructor(private readonly reviewsService: ReviewsService) {}

  @UseGuards(JwtAuthGuard)
  @Post()
  async create(@Body() createReviewDto: CreateReviewDto, @Request() req) {
    const userId = req.user.userId;
    return this.reviewsService.create(createReviewDto, userId);
  }

  @Get()
  async findAll() {
    return this.reviewsService.findAll();
  }

  @Get(':id')
  async findOne(@Param('id') id: string) {
    return this.reviewsService.findOne(+id);
  }

  @UseGuards(JwtAuthGuard)
  @Patch(':id')
  async update(
    @Param('id') id: string,
    @Body() updateReviewDto: UpdateReviewDto,
    @Request() req,
  ) {
    const userId = req.user.userId;
    return this.reviewsService.update(+id, updateReviewDto, userId);
  }

  @UseGuards(JwtAuthGuard)
  @Delete(':id')
  async remove(@Param('id') id: string, @Request() req) {
    const userId = req.user.userId;
    return this.reviewsService.remove(+id, userId);
  }
}
