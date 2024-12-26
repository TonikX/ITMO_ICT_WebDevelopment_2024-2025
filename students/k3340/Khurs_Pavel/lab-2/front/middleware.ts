import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  const publicPaths = ["/authentication", "/api"];

  const isPublic = publicPaths.some((path) => pathname.startsWith(path));

  if (!isPublic) {
    const token = request.cookies.get("authToken");

    if (!token) {
      const loginUrl = new URL("/authentication", request.url);
      return NextResponse.redirect(loginUrl);
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/tours/:path*",
    "/reservations/:path*",
    "/sales/:path*",
    "/profile/:path*",
  ],
};
