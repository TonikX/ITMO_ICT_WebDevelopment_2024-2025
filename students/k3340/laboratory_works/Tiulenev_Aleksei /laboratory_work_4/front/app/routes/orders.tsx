import type { Route } from "./+types/data";

import { redirect } from "react-router";
import OrdersPage from "@/pages/orders/orders";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "New React Router App" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}
function parseTokenFromCookies(cookieHeader: string) {
  const match = cookieHeader.match(/auth_token=([^;]+)/);
  return match ? match[1] : null;
}

export async function loader({ request }: Route.LoaderArgs) {
  const cookieHeader = request.headers.get("cookie") ?? "";
  const token = parseTokenFromCookies(cookieHeader);

  if (!token) {
    return redirect("/login");
  }
}

export default function Home() {
  return <OrdersPage />;
}
