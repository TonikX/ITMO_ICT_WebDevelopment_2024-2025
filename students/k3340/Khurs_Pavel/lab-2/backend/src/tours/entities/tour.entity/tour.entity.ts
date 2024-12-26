import { Reservation } from '@/src/reservations/entities/reservation.entity/reservation.entity';
import { Review } from '@/src/reviews/entities/review.entity/review.entity';
import { TravelAgency } from '@/src/travel-agencies/entities/travel-agency.entity/travel-agency.entity';
import {
  Entity,
  Column,
  PrimaryGeneratedColumn,
  ManyToOne,
  OneToMany,
  BaseEntity,
  JoinColumn,
} from 'typeorm';

@Entity()
export class Tour extends BaseEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  title: string;

  @Column('text')
  description: string;

  @Column('date')
  startDate: Date;

  @Column('date')
  endDate: Date;

  @Column()
  paymentConditions: string;

  @Column()
  country: string;

  @Column()
  travelAgencyId: number;

  @ManyToOne(() => TravelAgency, (agency) => agency.tours, {
    eager: true,
  })
  @JoinColumn({ name: 'travelAgencyId' })
  travelAgency: TravelAgency;

  @OneToMany(() => Reservation, (reservation) => reservation.tour)
  reservations: Reservation[];

  @OneToMany(() => Review, (review) => review.tour)
  reviews: Review[];
}
