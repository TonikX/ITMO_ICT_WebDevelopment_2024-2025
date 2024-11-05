import {
  Controller,
  Request,
  Post,
  UseGuards,
  Body,
  Res,
  Get,
  UnauthorizedException,
} from '@nestjs/common';
import { AuthService } from '@/src/auth/auth.service';

import { RegisterDto } from '@/src/auth/dto/register.dto';
import { JwtAuthGuard } from '@/src/auth/guards/jwt-auth.guard';

import { Response } from 'express';

@Controller('auth')
export class AuthController {
  constructor(private authService: AuthService) {}

  @Post('register')
  async register(
    @Body() registerDto: RegisterDto,
    @Res({ passthrough: true }) res: Response,
  ) {
    const user = await this.authService.register(registerDto);

    const token = await this.authService.login({
      email: user.email,
      id: user.id,
      role: user.role,
    });

    res.cookie('authToken', token.access_token, {
      sameSite: 'lax',
      maxAge: 3600000,
      secure: false,
      path: '/',
    });

    return { message: 'Регистрация успешна' };
  }

  @Post('login')
  async login(@Request() req, @Res({ passthrough: true }) res: Response) {
    if (!req.body) {
      throw new UnauthorizedException('Неверные учетные данные');
    }
    const token = await this.authService.login(req.body);

    res.cookie('authToken', token.access_token, {
      sameSite: 'lax',
      maxAge: 3600000, // 1 час
      secure: false,
      path: '/',
    });

    return { message: 'Успешный вход' };
  }

  @UseGuards(JwtAuthGuard)
  @Get('profile')
  getProfile(@Request() req) {
    return req.user;
  }

  @UseGuards(JwtAuthGuard)
  @Post('logout')
  async logout(@Res({ passthrough: true }) res: Response) {
    res.clearCookie('authToken', {
      httpOnly: true,
      secure: false,
      sameSite: 'none',
      path: '/',
    });
    return { message: 'Выход выполнен' };
  }
}
