import { Injectable, UnauthorizedException } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { Strategy, StrategyOptions } from 'passport-jwt';
import { ConfigService } from '@nestjs/config';
import { UsersService } from '@/src/users/users.service';

const cookieExtractor = (req: any) => {
  let token = null;
  if (req && req.cookies) {
    token = req.cookies['authToken'];
  }
  return token;
};

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(
    private configService: ConfigService,
    private usersService: UsersService,
  ) {
    super({
      jwtFromRequest: cookieExtractor,
      ignoreExpiration: false,
      secretOrKey: configService.get<string>('JWT_SECRET'),
    } as StrategyOptions);
  }

  async validate(payload: any) {
    const user = await this.usersService.findOneById(payload.sub);

    if (!user) {
      throw new UnauthorizedException('Пользователь не найден');
    }
    if (user.isBlocked) {
      throw new UnauthorizedException('Ваш аккаунт заблокирован');
    }
    return { userId: user.id, email: user.email, role: user.role };
  }
}
