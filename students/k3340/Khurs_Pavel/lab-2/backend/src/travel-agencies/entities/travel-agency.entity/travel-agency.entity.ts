import { Tour } from '@/src/tours/entities/tour.entity/tour.entity';
import {
  Entity,
  Column,
  PrimaryGeneratedColumn,
  OneToMany,
  BaseEntity,
} from 'typeorm';

@Entity()
export class TravelAgency extends BaseEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  @Column()
  contactInfo: string;

  @OneToMany(() => Tour, (tour) => tour.travelAgency)
  tours: Tour[];
}
