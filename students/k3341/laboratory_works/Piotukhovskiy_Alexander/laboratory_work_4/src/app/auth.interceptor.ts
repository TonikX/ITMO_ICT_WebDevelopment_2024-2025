import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';

export const AuthInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  const token = localStorage.getItem('auth_token');

  let modifiedRequest = req;
  if (token) {
    modifiedRequest = req.clone({
      setHeaders: {
        Authorization: `Token ${token}`,
      },
    });
  }

  return next(modifiedRequest).pipe(
    catchError((error) => {
      if (error.status === 401) {
        localStorage.removeItem('auth_token');
        router.navigate(['/login']);
      }
      throw error;
    })
  );
};
