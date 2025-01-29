import type { Route } from "./+types/data";
import DataPage from "@/pages/employees/employees";

import { redirect } from "react-router";

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
  const token = '7c7805134f5912f723fe82d17da63254ee8ea313';

  if (!token) {
    return redirect("/login");
  }
}

export default function Home() {
  return <>Домашняя страница</>;
}
