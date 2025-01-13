// serverCookieService.ts

import type { CookieService } from "@/api/cookieService";
import { IncomingMessage, ServerResponse } from "http";

export class ServerCookieService implements CookieService {
  private req: IncomingMessage;
  private res: ServerResponse;

  constructor(req: IncomingMessage, res: ServerResponse) {
    this.req = req;
    this.res = res;
  }

  getToken(): string | null {
    const cookies = this.req.headers.cookie || "";
    const match = cookies.match(/(^|;\s*)auth_token=([^;]+)/);
    return match ? match[2] : null;
  }

  setToken(token: string) {
    const days = 7;
    const maxAge = days * 24 * 60 * 60;
    // Добавляем Set-Cookie заголовок
    this.res.setHeader(
      "Set-Cookie",
      `auth_token=${token}; Max-Age=${maxAge}; Path=/; HttpOnly`
    );
  }

  removeToken() {
    // Удаляем cookie, устанавливая его с отрицательным Max-Age
    this.res.setHeader(
      "Set-Cookie",
      `auth_token=; Max-Age=0; Path=/; HttpOnly`
    );
  }
}
