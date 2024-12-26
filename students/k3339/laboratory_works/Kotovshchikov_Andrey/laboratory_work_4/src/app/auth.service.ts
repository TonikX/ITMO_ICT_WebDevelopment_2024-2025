import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ISignInRequest, ISignUpRequest } from './types';
import { tap } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly baseUrl: string = 'http://127.0.0.1:8000/auth';
  private _isAuth = false;

  constructor(private readonly http: HttpClient) {}

  signUp(data: ISignUpRequest) {
    const url = `${this.baseUrl}/users/`;
    return this.http.post<void>(url, data);
  }

  signIn(data: ISignInRequest) {
    const url = `${this.baseUrl}/token/login/`;
    return this.http
      .post<{ auth_token: string }>(url, data)
      .pipe(
        tap((response) => localStorage.setItem('token', response.auth_token))
      );
  }

  logout() {
    localStorage.removeItem('token');
    this._isAuth = false;
  }

  getAuthToken() {
    return localStorage.getItem('token');
  }

  get isAuth() {
    if (!this._isAuth) {
      const token = localStorage.getItem('token');
      this._isAuth = !!token;
    }

    return this._isAuth;
  }
}
