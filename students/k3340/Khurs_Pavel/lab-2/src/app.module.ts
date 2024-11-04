import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { AuthModule } from '@/src/auth/auth.module';
import { Reservation } from '@/src/reservations/entities/reservation.entity/reservation.entity';
import { ReservationsModule } from '@/src/reservations/reservations.module';
import { Review } from '@/src/reviews/entities/review.entity/review.entity';
import { ReviewsModule } from '@/src/reviews/reviews.module';
import { Tour } from '@/src/tours/entities/tour.entity/tour.entity';
import { ToursModule } from '@/src/tours/tours.module';
import { TravelAgency } from '@/src/travel-agencies/entities/travel-agency.entity/travel-agency.entity';
import { TravelAgenciesModule } from '@/src/travel-agencies/travel-agencies.module';

import { UsersModule } from '@/src/users/users.module';
import { User } from '@/src/users/entities/user.entity/user.entity';
import { DataSource } from 'typeorm';

const customBefore = (request, context) => {
  const { query = {} } = request;
  console.log(query, 'queryquery');

  const newQuery = {
    ...query,
  };

  request.query = newQuery;

  return request;
};

const customAfter = (originalResponse, request, context) => {
  console.log(originalResponse.meta);

  return originalResponse;
};

@Module({
  imports: [
    ConfigModule.forRoot(),
    TypeOrmModule.forRootAsync({
      imports: [ConfigModule],
      useFactory: async (configService: ConfigService) => ({
        type: 'postgres',
        host: configService.get<string>('DB_HOST'),
        port: configService.get<number>('DB_PORT'),
        username: configService.get<string>('DB_USERNAME'),
        password: configService.get<string>('DB_PASSWORD'),
        database: configService.get<string>('DB_DATABASE'),
        entities: [User, Tour, Reservation, Review, TravelAgency],
        synchronize: true,
      }),
      inject: [ConfigService],
    }),
    import('@adminjs/nestjs').then(({ AdminModule }) =>
      AdminModule.createAdminAsync({
        imports: [TypeOrmModule],
        inject: [DataSource],
        useFactory: async (dataSource: DataSource) => {
          const AdminJS = (await import('adminjs')).default;
          const { Database, Resource } = await import('@adminjs/typeorm');

          AdminJS.registerAdapter({ Database, Resource });

          return {
            adminJsOptions: {
              rootPath: '/admin',
              resources: [User, Tour, Reservation, Review, TravelAgency],
            },
          };
        },
      }),
    ),
    UsersModule,
    ToursModule,
    TravelAgenciesModule,
    ReservationsModule,
    ReviewsModule,
    AuthModule,
  ],
})
export class AppModule {}
