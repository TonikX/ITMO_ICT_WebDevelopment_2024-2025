import {
  Injectable,
  NotFoundException,
  ForbiddenException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { CreateReviewDto } from '@/src/reviews/dto/create-review.dto';
import { UpdateReviewDto } from '@/src/reviews/dto/update-review.dto';
import { Review } from '@/src/reviews/entities/review.entity/review.entity';
import { ToursService } from '@/src/tours/tours.service';
import { UsersService } from '@/src/users/users.service';
import { Repository } from 'typeorm';

@Injectable()
export class ReviewsService {
  constructor(
    @InjectRepository(Review)
    private reviewsRepository: Repository<Review>,
    private usersService: UsersService,
    private toursService: ToursService,
  ) {}

  async create(
    createReviewDto: CreateReviewDto,
    userId: number,
  ): Promise<Review> {
    const user = await this.usersService.findOneById(userId);
    const tour = await this.toursService.findOne(createReviewDto.tourId);

    const review = this.reviewsRepository.create({
      ...createReviewDto,
      user,
      tour,
    });

    return this.reviewsRepository.save(review);
  }

  async findAll(): Promise<Review[]> {
    return this.reviewsRepository.find({ relations: ['user', 'tour'] });
  }

  async findOne(id: number): Promise<Review> {
    const review = await this.reviewsRepository.findOne({
      where: { id },
      relations: ['user', 'tour'],
    });

    if (!review) {
      throw new NotFoundException('Отзыв не найден');
    }

    return review;
  }

  async update(
    id: number,
    updateReviewDto: UpdateReviewDto,
    userId: number,
  ): Promise<Review> {
    const review = await this.findOne(id);

    if (review.user.id !== userId) {
      throw new ForbiddenException('Вы не можете редактировать этот отзыв');
    }

    Object.assign(review, updateReviewDto);
    return this.reviewsRepository.save(review);
  }

  async remove(id: number, userId: number): Promise<void> {
    const review = await this.findOne(id);

    if (review.user.id !== userId) {
      throw new ForbiddenException('Вы не можете удалять этот отзыв');
    }

    await this.reviewsRepository.delete(id);
  }
}
