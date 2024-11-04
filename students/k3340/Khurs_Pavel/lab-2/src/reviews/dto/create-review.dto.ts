import {
  IsNotEmpty,
  IsNumber,
  IsString,
  Min,
  Max,
  IsDate,
} from 'class-validator';

export class CreateReviewDto {
  @IsNotEmpty()
  @IsNumber()
  tourId: number;

  @IsNotEmpty()
  @IsString()
  comment: string;

  @IsNotEmpty()
  @IsNumber()
  @Min(1)
  @Max(10)
  rating: number;

  @IsNotEmpty()
  @IsDate()
  tourDate: Date;
}
