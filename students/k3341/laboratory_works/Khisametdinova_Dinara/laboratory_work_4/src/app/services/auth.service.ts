import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private baseUrl = 'http://127.0.0.1:8000/auth/';

  constructor(private http: HttpClient) {}

  login(username: string, password: string): Observable<any> {
    return this.http.post(`${this.baseUrl}token/login/`, { username, password });
  }

  logout(): void {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('current_user');
  }

  setCurrentUser(user: any): void {
    localStorage.setItem('current_user', JSON.stringify(user));
  }

  getCurrentUser(): any {
    const user = localStorage.getItem('current_user');
    if (user) {
      try {
        return JSON.parse(user);
      } catch (e) {
        console.error('Error parsing user from localStorage', e);
        return null;
      }
    }
    return null;
  }
  register(user: any): Observable<any> {
    return this.http.post(`${this.baseUrl}users/`, user);
  }

  getCurrentUserDetails(): Observable<any> {
    return this.http.get('http://127.0.0.1:8000/peer/current-user/');
  }
}
