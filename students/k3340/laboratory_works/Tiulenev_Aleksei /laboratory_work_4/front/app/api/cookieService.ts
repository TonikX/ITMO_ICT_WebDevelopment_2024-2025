export interface CookieService {
  getToken(): string | null;
  setToken(token: string): void;
  removeToken(): void;
}
