import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();

    const response = await fetch("http://127.0.0.1:3001/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
      credentials: "include",
    });

    const data = await response.json();
    console.log(data, "register data");

    const cookies = response.headers.get("set-cookie");
    if (cookies) {
      const res = NextResponse.json(data);
      res.headers.set("Set-Cookie", cookies);
      return res;
    }

    return NextResponse.json(data, {
      status: response.status,
    });
  } catch (error) {
    console.error("Ошибка обработки запроса:", error);
    return NextResponse.json(
      { message: "Внутренняя ошибка сервера" },
      { status: 500 }
    );
  }
}
