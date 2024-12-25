"use client";

import React, { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  TableHeader,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
  Table,
} from "@/components/ui/table";
import { api } from "@/api/api";
import { TrashIcon, EditIcon } from "lucide-react";

export interface Customer {
  id: number;
  name: string;
  email: string;
  phone_number?: string;
  address?: string;
}

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
}

function SearchBar({ value, onChange }: SearchBarProps) {
  return (
    <div className="my-4">
      <Input
        placeholder="Поиск по имени, email или телефону..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}

export const CustomersTab: React.FC = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [search, setSearch] = useState<string>("");
  const [open, setOpen] = useState<boolean>(false);
  const [isEditMode, setIsEditMode] = useState<boolean>(false);
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(
    null
  );

  const [formData, setFormData] = useState<{
    name: string;
    email: string;
    phone_number?: string;
    address?: string;
  }>({
    name: "",
    email: "",
    phone_number: "",
    address: "",
  });

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const res = await api.get("api/customers/");
        if (res.data) {
          setCustomers(res.data);
        }
      } catch (error) {
        console.error("Ошибка при загрузке клиентов:", error);
      }
    };
    fetchCustomers();
  }, []);

  const filtered = customers.filter((customer) => {
    const searchLower = search.toLowerCase();
    return (
      customer.name.toLowerCase().includes(searchLower) ||
      customer.email.toLowerCase().includes(searchLower) ||
      (customer.phone_number &&
        customer.phone_number.toLowerCase().includes(searchLower))
    );
  });

  const handleOpenAdd = () => {
    setIsEditMode(false);
    setFormData({
      name: "",
      email: "",
      phone_number: "",
      address: "",
    });
    setOpen(true);
  };

  const handleOpenEdit = (customer: Customer) => {
    setIsEditMode(true);
    setSelectedCustomer(customer);
    setFormData({
      name: customer.name,
      email: customer.email,
      phone_number: customer.phone_number || "",
      address: customer.address || "",
    });
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setSelectedCustomer(null);
    setFormData({
      name: "",
      email: "",
      phone_number: "",
      address: "",
    });
  };

  const handleDelete = async (customerId: number) => {
    if (window.confirm("Вы уверены, что хотите удалить этого клиента?")) {
      try {
        await api.delete(`api/customers/${customerId}/`);
        setCustomers(customers.filter((c) => c.id !== customerId));
      } catch (error) {
        console.error("Ошибка при удалении клиента:", error);
      }
    }
  };

  const handleFormSubmit = async () => {
    if (!formData.name.trim() || !formData.email.trim()) {
      alert("Пожалуйста, заполните обязательные поля: Имя и Email.");
      return;
    }

    try {
      if (isEditMode && selectedCustomer) {
        // Обновление существующего клиента
        const res = await api.put(
          `api/customers/${selectedCustomer.id}/`,
          formData
        );
        if (res.data) {
          setCustomers(
            customers.map((c) => (c.id === selectedCustomer.id ? res.data : c))
          );
          handleClose();
        }
      } else {
        // Создание нового клиента
        const res = await api.post("api/customers/", formData);
        if (res.data) {
          setCustomers([...customers, res.data]);
          handleClose();
        }
      }
    } catch (error) {
      console.error(
        isEditMode
          ? "Ошибка при обновлении клиента:"
          : "Ошибка при создании клиента:",
        error
      );
      alert(
        isEditMode
          ? "Не удалось обновить клиента. Проверьте введённые данные."
          : "Не удалось создать клиента. Проверьте введённые данные."
      );
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold">Клиенты</h2>
        <Button onClick={handleOpenAdd}>Добавить клиента</Button>
      </div>

      <SearchBar value={search} onChange={setSearch} />

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Имя</TableHead>
            <TableHead>Email</TableHead>
            <TableHead>Телефон</TableHead>
            <TableHead>Адрес</TableHead>
            <TableHead>Действия</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {filtered.map((customer) => (
            <TableRow key={customer.id}>
              <TableCell>{customer.name}</TableCell>
              <TableCell>{customer.email}</TableCell>
              <TableCell>{customer.phone_number || "-"}</TableCell>
              <TableCell>{customer.address || "-"}</TableCell>
              <TableCell className="flex space-x-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleOpenEdit(customer)}
                >
                  <EditIcon className="h-4 w-4" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleDelete(customer.id)}
                >
                  <TrashIcon className="h-4 w-4 text-red-500" />
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      {/* Диалог для добавления/редактирования клиента */}
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="sm:max-w-[500px]">
          <DialogHeader>
            <DialogTitle>
              {isEditMode ? "Редактировать клиента" : "Новый клиент"}
            </DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="name" className="block mb-1">
                Имя<span className="text-red-500">*</span>
              </Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) =>
                  setFormData({ ...formData, name: e.target.value })
                }
                placeholder="Введите имя клиента"
              />
            </div>
            <div>
              <Label htmlFor="email" className="block mb-1">
                Email<span className="text-red-500">*</span>
              </Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) =>
                  setFormData({ ...formData, email: e.target.value })
                }
                placeholder="Введите email клиента"
              />
            </div>
            <div>
              <Label htmlFor="phone_number" className="block mb-1">
                Телефон
              </Label>
              <Input
                id="phone_number"
                value={formData.phone_number}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    phone_number: e.target.value,
                  })
                }
                placeholder="Введите телефон клиента"
              />
            </div>
            <div>
              <Label htmlFor="address" className="block mb-1">
                Адрес
              </Label>
              <Input
                id="address"
                value={formData.address}
                onChange={(e) =>
                  setFormData({ ...formData, address: e.target.value })
                }
                placeholder="Введите адрес клиента"
              />
            </div>
          </div>
          <DialogFooter className="space-x-2">
            <Button variant="secondary" onClick={handleClose}>
              Отмена
            </Button>
            <Button onClick={handleFormSubmit}>
              {isEditMode ? "Сохранить" : "Создать"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};
