# Документация веб-приложения с NestJS и Next.js

## Введение

Добро пожаловать в документацию веб-приложения, разработанного с использованием **NestJS** и **Next.js**.

### Технологии

- **NestJS**: Фреймворк для серверной разработки на Node.js, построенный с использованием TypeScript. Обеспечивает модульную архитектуру, удобство тестирования и интеграцию с различными базами данных и сторонними сервисами.
- **Next.js**: Фреймворк для фронтенд-разработки на React, предоставляющий возможности серверного рендеринга, статической генерации и оптимизации производительности.
- **TypeScript**: Надстройка над JavaScript, обеспечивающая статическую типизацию для повышения надежности и удобства разработки.
- **PostgreSQL**: Реляционная база данных для хранения и управления данными приложения.

### Установка зависимостей

Для установки зависимостей используйте [pnpm](https://pnpm.io/):

```bash
pnpm install
```

- Эта команда будет работать как для front так и для back

### Запуск

- Для backend

```bash
pnpm run start:dev
```

- Для frontend

```bash
pnpm run dev
```

### Основные таблицы

```ts
@Entity()
export class Reservation extends BaseEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  userId: number;

  @ManyToOne(() => User, (user) => user.reservations, { eager: true })
  @JoinColumn({ name: "userId" })
  user: User;

  @Column()
  tourId: number;

  @ManyToOne(() => Tour, (tour) => tour.reservations, { eager: true })
  @JoinColumn({ name: "tourId" })
  tour: Tour;

  @Column({ default: false })
  isConfirmed: boolean;

  @Column({ default: "pending" })
  status: string;

  @Column({ type: "timestamp", default: () => "CURRENT_TIMESTAMP" })
  createdAt: Date;
}
```

```ts
@Entity()
export class Review extends BaseEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  userId: number;

  @ManyToOne(() => User, (user) => user.reviews, { eager: true })
  @JoinColumn({ name: "userId" })
  user: User;

  @Column()
  tourId: number;

  @ManyToOne(() => Tour, (tour) => tour.reviews, { eager: true })
  @JoinColumn({ name: "tourId" })
  tour: Tour;

  @Column("text")
  comment: string;

  @Column()
  @Min(1)
  @Max(10)
  rating: number;

  @Column({ type: "timestamp", default: () => "CURRENT_TIMESTAMP" })
  createdAt: Date;
}
```

```ts
@Entity()
export class Tour extends BaseEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  title: string;

  @Column("text")
  description: string;

  @Column("date")
  startDate: Date;

  @Column("date")
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
  @JoinColumn({ name: "travelAgencyId" })
  travelAgency: TravelAgency;

  @OneToMany(() => Reservation, (reservation) => reservation.tour)
  reservations: Reservation[];

  @OneToMany(() => Review, (review) => review.tour)
  reviews: Review[];
}
```

```ts
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
```

```ts
@Entity()
export class User extends BaseEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  @IsNotEmpty()
  name: string;

  @Column({ unique: true })
  @IsEmail()
  email: string;

  @Column()
  password: string;

  @Column({ default: "user" })
  role: string;

  @Column({ default: false })
  isBlocked: boolean;

  @OneToMany(() => Reservation, (reservation) => reservation.user)
  reservations: Reservation[];

  @OneToMany(() => Review, (review) => review.user)
  reviews: Review[];
}
```

### ENV

- Все что нужно для запуска есть в .env.sample
