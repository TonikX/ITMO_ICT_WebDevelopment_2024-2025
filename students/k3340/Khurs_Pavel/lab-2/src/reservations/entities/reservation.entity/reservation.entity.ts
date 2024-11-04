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
export class Reservation extends BaseEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  userId: number;

  @ManyToOne(() => User, (user) => user.reservations, { eager: true })
  @JoinColumn({ name: 'userId' })
  user: User;

  @Column()
  tourId: number;

  @ManyToOne(() => Tour, (tour) => tour.reservations, { eager: true })
  @JoinColumn({ name: 'tourId' })
  tour: Tour;

  @Column({ default: 'pending' })
  status: string;

  @Column({ type: 'timestamp', default: () => 'CURRENT_TIMESTAMP' })
  createdAt: Date;
}
