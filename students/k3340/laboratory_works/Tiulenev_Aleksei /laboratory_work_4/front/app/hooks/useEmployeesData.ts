import type { Employee } from "@/types/api";
import { useState } from "react";

export function useEmployeesData() {
  const [employees, setEmployees] = useState<Employee[]>([
    {
      first_name: "John",
      last_name: "Doe",
      role: "Manager",
      email: "john@example.com",
    },
    {
      first_name: "Jane",
      last_name: "Smith",
      role: "Editor",
      email: "jane@example.com",
    },
  ]);

  return { employees, setEmployees };
}
