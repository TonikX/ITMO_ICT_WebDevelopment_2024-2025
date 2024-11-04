import { Tour } from '@/src/tours/entities/tour.entity/tour.entity';
import { User } from '@/src/users/entities/user.entity/user.entity';

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
  rating: number; // От 1 до 10

  @Column()
  tourDate: Date;

  @Column({ type: 'timestamp', default: () => 'CURRENT_TIMESTAMP' })
  createdAt: Date;
}
