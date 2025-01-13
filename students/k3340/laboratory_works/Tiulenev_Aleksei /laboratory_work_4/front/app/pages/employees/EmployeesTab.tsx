"use client";

import React, { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useEmployeesData } from "@/hooks/useEmployeesData";
import type { Employee } from "@/types/api";
import {
  TableHeader,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
  Table,
} from "@/components/ui/table";

import { api } from "@/api/api";

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
}

function SearchBar({ value, onChange }: SearchBarProps) {
  return (
    <div className="my-4">
      <Input
        placeholder="Поиск..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}

export const EmployeesTab: React.FC = () => {
  const [employees, setEmployees] = useState<Employee[] | []>([]);
  const [search, setSearch] = useState<string>("");
  const [open, setOpen] = useState<boolean>(false);
  const [newEmployee, setNewEmployee] = useState<Employee>({
    first_name: "",
    last_name: "",
    role: "Other",
    email: "",
  });

  useEffect(() => {
    const fetchUsers = async () => {
      const res = await api.get("api/employees");

      if (res.data) {
        setEmployees(res.data);
      }
      return res.data;
    };
    fetchUsers();
  }, []);

  const filtered = employees.filter(
    (e) =>
      e.first_name.toLowerCase().includes(search.toLowerCase()) ||
      e.last_name.toLowerCase().includes(search.toLowerCase()) ||
      e.role.toLowerCase().includes(search.toLowerCase()) ||
      e.email.toLowerCase().includes(search.toLowerCase())
  );

  function addEmployee() {
    setEmployees([...employees, newEmployee]);
    setNewEmployee({ first_name: "", last_name: "", role: "Other", email: "" });
    setOpen(false);
  }

  return (
    <div>
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold">Сотрудники</h2>
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger asChild>
            <Button>Добавить сотрудника</Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Новый сотрудник</DialogTitle>
            </DialogHeader>
            <div className="space-y-4">
              <div>
                <Label className="mb-1">First Name</Label>
                <Input
                  value={newEmployee.first_name}
                  onChange={(e) =>
                    setNewEmployee({
                      ...newEmployee,
                      first_name: e.target.value,
                    })
                  }
                />
              </div>
              <div>
                <Label className="mb-1">Last Name</Label>
                <Input
                  value={newEmployee.last_name}
                  onChange={(e) =>
                    setNewEmployee({
                      ...newEmployee,
                      last_name: e.target.value,
                    })
                  }
                />
              </div>
              <div>
                <Label className="mb-1">Role</Label>
                <Input
                  value={newEmployee.role}
                  onChange={(e) =>
                    setNewEmployee({
                      ...newEmployee,
                      role: e.target.value as Employee["role"],
                    })
                  }
                />
              </div>
              <div>
                <Label className="mb-1">Email</Label>
                <Input
                  type="email"
                  value={newEmployee.email}
                  onChange={(e) =>
                    setNewEmployee({ ...newEmployee, email: e.target.value })
                  }
                />
              </div>
            </div>
            <DialogFooter className="space-x-2">
              <Button variant="secondary" onClick={() => setOpen(false)}>
                Отмена
              </Button>
              <Button onClick={addEmployee}>Сохранить</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      <SearchBar value={search} onChange={setSearch} />

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Имя</TableHead>
            <TableHead>Фамилия</TableHead>
            <TableHead>Роль</TableHead>
            <TableHead>email</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {filtered.map((emp, idx) => (
            <TableRow key={idx}>
              <TableCell className="font-medium">{emp.first_name}</TableCell>
              <TableCell>{emp.last_name}</TableCell>
              <TableCell>{emp.role}</TableCell>
              <TableCell>{emp.email}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};
