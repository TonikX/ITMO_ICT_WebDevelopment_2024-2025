import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Review } from '@/src/reviews/entities/review.entity/review.entity';
import { ReviewsController } from '@/src/reviews/reviews.controller';
import { ReviewsService } from '@/src/reviews/reviews.service';
import { ToursModule } from '@/src/tours/tours.module';
import { UsersModule } from '@/src/users/users.module';

@Module({
  imports: [TypeOrmModule.forFeature([Review]), UsersModule, ToursModule],
  controllers: [ReviewsController],
  providers: [ReviewsService],
  exports: [ReviewsService],
})
export class ReviewsModule {}
