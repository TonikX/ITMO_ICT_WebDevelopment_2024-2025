import BooksPage from "@/pages/books/books";
import type { Route } from "./+types/data";

import { redirect } from "react-router";
import LoginPage from "@/pages/login/login";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "New React Router App" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export default function Home() {
  return <LoginPage />;
}
