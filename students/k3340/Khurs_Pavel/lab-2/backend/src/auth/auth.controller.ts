import { Controller, Request, Post, UseGuards, Body } from '@nestjs/common';
import { AuthService } from '@/src/auth/auth.service';
import { LoginDto } from '@/src/auth/dto/login.dto';
import { RegisterDto } from '@/src/auth/dto/register.dto';
import { JwtAuthGuard } from '@/src/auth/guards/jwt-auth.guard';
import { LocalAuthGuard } from '@/src/auth/guards/local-auth.guard';

@Controller('auth')
export class AuthController {
  constructor(private authService: AuthService) {}

  @Post('register')
  async register(@Body() registerDto: RegisterDto) {
    return this.authService.register(registerDto);
  }

  @UseGuards(LocalAuthGuard)
  @Post('login')
  async login(@Body() loginDto: LoginDto, @Request() req) {
    return this.authService.login(req.user);
  }
  @UseGuards(JwtAuthGuard)
  @Post('profile')
  getProfile(@Request() req) {
    return req.user;
  }
}
