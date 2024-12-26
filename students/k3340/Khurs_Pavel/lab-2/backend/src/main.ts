import { NestFactory } from '@nestjs/core';

import { ValidationPipe } from '@nestjs/common';
import { AppModule } from '@/src/app.module';
import cookieParser from 'cookie-parser';

async function bootstrap() {
  const app = await NestFactory.create(AppModule, {
    snapshot: true,
  });
  app.use(cookieParser());
  app.enableCors({
    origin: 'http://localhost:3000',
    credentials: true,
  });
  app.useGlobalPipes(new ValidationPipe());
  await app.listen(3001);
}
bootstrap();
