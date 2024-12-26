import { Tour } from '@/src/tours/entities/tour.entity/tour.entity';
import { User } from '@/src/users/entities/user.entity/user.entity';
import { Max, Min } from 'class-validator';

import {
  Entity,
  PrimaryGeneratedColumn,
  ManyToOne,
  Column,
  BaseEntity,
  JoinColumn,
} from 'typeorm';

@Entity()
export class Review extends BaseEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  userId: number;

  @ManyToOne(() => User, (user) => user.reviews, { eager: true })
  @JoinColumn({ name: 'userId' })
  user: User;

  @Column()
  tourId: number;

  @ManyToOne(() => Tour, (tour) => tour.reviews, { eager: true })
  @JoinColumn({ name: 'tourId' })
  tour: Tour;

  @Column('text')
  comment: string;

  @Column()
  @Min(1)
  @Max(10)
  rating: number;

  @Column({ type: 'timestamp', default: () => 'CURRENT_TIMESTAMP' })
  createdAt: Date;
}
