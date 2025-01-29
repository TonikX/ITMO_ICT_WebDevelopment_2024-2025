export interface Employee {
  first_name: string;
  last_name: string;
  role: "Manager" | "Editor" | "Other";
  email: string;
}
