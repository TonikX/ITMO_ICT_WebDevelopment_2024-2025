// clientCookieService.ts

import type { CookieService } from "@/api/cookieService";

export class ClientCookieService implements CookieService {
  getToken(): string | null {
    const match = document.cookie.match(/(^|;\s*)auth_token=([^;]+)/);
    return match ? match[2] : null;
  }

  setToken(token: string) {
    const days = 7;
    const date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    const expires = "expires=" + date.toUTCString();
    document.cookie = `auth_token=${token};${expires};path=/`;
  }

  removeToken() {
    document.cookie = "auth_token=; Max-Age=-99999999;path=/";
  }
}
