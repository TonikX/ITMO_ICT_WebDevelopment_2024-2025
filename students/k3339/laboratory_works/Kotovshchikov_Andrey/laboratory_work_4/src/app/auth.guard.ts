import { inject } from '@angular/core';
import { AuthService } from './auth.service';

export const isAuthGuard = () => {
  const authService = inject(AuthService);
  return authService.isAuth;
};
