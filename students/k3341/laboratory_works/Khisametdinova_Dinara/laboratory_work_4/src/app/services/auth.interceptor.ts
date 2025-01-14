import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = localStorage.getItem('auth_token'); // Получение токена из localStorage

  if (token) {
    // Добавление заголовка Authorization
    const authReq = req.clone({
      setHeaders: {
        Authorization: `Token ${token}`,
      },
    });
    return next(authReq);
  }

  return next(req);
};
