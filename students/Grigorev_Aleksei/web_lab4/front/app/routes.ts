import {
  type RouteConfig,
  index,
  layout,
  route,
} from "@react-router/dev/routes";

export default [
  layout("./routes/sidebar-layout.tsx", [
    index("routes/home.tsx"),
    route("employees", "routes/employees.tsx"),
    route("books", "routes/books.tsx"),
    route("authors", "routes/authors.tsx"),
    route("customers", "routes/customers.tsx"),
    route("orders", "routes/orders.tsx"),
    route("editions", "routes/editions.tsx"),
  ]),

  route("login", "routes/login.tsx"),
] satisfies RouteConfig;
