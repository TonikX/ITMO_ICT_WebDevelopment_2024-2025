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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export interface Customer {
  id: number;
  name: string;
  email: string;
  phone_number?: string;
  address?: string;
}

export interface Author {
  id: number;
  first_name: string;
  last_name: string;
  biography: string;
  email?: string;
  phone_number?: string;
}

export interface BookAuthor {
  author_id: number;
  first_name: string;
  last_name: string;
  position_on_cover: number;
  royalty_percentage: string;
}

export interface Book {
  id: number;
  title: string;
  authors: BookAuthor[];
}

export interface Edition {
  id: number;
  book: Book;
  edition_number: number;
  publication_date: string;
  number_of_pages: number;
  has_illustrations: boolean;
  editors: any[]; // Замените `any` на соответствующий тип, если необходимо
}

export interface OrderItem {
  id: number;
  edition: Edition;
  quantity: number;
}

export interface Order {
  id: number;
  customer: Customer;
  date_ordered: string;
  order_items: OrderItem[];
}
interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
}

function SearchBar({ value, onChange }: SearchBarProps) {
  return (
    <div className="my-4">
      <Input
        placeholder="Поиск по клиенту или дате заказа..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}

export const OrdersTab: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [editions, setEditions] = useState<Edition[]>([]);
  const [search, setSearch] = useState<string>("");
  const [open, setOpen] = useState<boolean>(false);
  const [isEditMode, setIsEditMode] = useState<boolean>(false);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);

  // Формные данные для создания/редактирования заказа
  const [formData, setFormData] = useState<{
    customer_id: number | "";
    date_ordered: string;
    order_items: {
      edition_id: number | "";
      quantity: number;
    }[];
  }>({
    customer_id: "",
    date_ordered: new Date().toISOString().split("T")[0], // Текущая дата в формате YYYY-MM-DD
    order_items: [{ edition_id: "", quantity: 1 }],
  });

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const res = await api.get("api/orders/");
        if (res.data) {
          setOrders(res.data);
        }
      } catch (error) {
        console.error("Ошибка при загрузке заказов:", error);
      }
    };

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

    const fetchEditions = async () => {
      try {
        const res = await api.get("api/editions/");
        if (res.data) {
          setEditions(res.data);
        }
      } catch (error) {
        console.error("Ошибка при загрузке изданий:", error);
      }
    };

    fetchOrders();
    fetchCustomers();
    fetchEditions();
  }, []);

  const filtered = orders.filter((order) => {
    const customerName = order.customer.name.toLowerCase();
    const dateOrdered = order.date_ordered.toLowerCase();
    const searchLower = search.toLowerCase();
    return (
      customerName.includes(searchLower) || dateOrdered.includes(searchLower)
    );
  });

  const handleOpenAdd = () => {
    setIsEditMode(false);
    setFormData({
      customer_id: "",
      date_ordered: new Date().toISOString().split("T")[0],
      order_items: [{ edition_id: "", quantity: 1 }],
    });
    setOpen(true);
  };

  const handleOpenEdit = (order: Order) => {
    setIsEditMode(true);
    setSelectedOrder(order);
    setFormData({
      customer_id: order.customer.id,
      date_ordered: order.date_ordered,
      order_items: order.order_items.map((item) => ({
        edition_id: item.edition.id,
        quantity: item.quantity,
      })),
    });
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setSelectedOrder(null);
    setFormData({
      customer_id: "",
      date_ordered: new Date().toISOString().split("T")[0],
      order_items: [{ edition_id: "", quantity: 1 }],
    });
  };

  const handleDelete = async (orderId: number) => {
    if (window.confirm("Вы уверены, что хотите удалить этот заказ?")) {
      try {
        await api.delete(`api/orders/${orderId}/`);
        setOrders(orders.filter((o) => o.id !== orderId));
      } catch (error) {
        console.error("Ошибка при удалении заказа:", error);
        alert("Не удалось удалить заказ. Попробуйте позже.");
      }
    }
  };

  const handleFormChange = (field: keyof typeof formData, value: any) => {
    setFormData({
      ...formData,
      [field]: value,
    });
  };

  const handleOrderItemChange = (
    index: number,
    field: keyof (typeof formData.order_items)[number],
    value: any
  ) => {
    const updatedOrderItems = [...formData.order_items];
    updatedOrderItems[index] = {
      ...updatedOrderItems[index],
      [field]: value,
    };
    setFormData({
      ...formData,
      order_items: updatedOrderItems,
    });
  };

  const addOrderItem = () => {
    setFormData({
      ...formData,
      order_items: [...formData.order_items, { edition_id: "", quantity: 1 }],
    });
  };

  const removeOrderItem = (index: number) => {
    const updatedOrderItems = formData.order_items.filter(
      (_, i) => i !== index
    );
    setFormData({
      ...formData,
      order_items: updatedOrderItems,
    });
  };

  const handleFormSubmit = async () => {
    // Валидация
    if (!formData.customer_id) {
      alert("Пожалуйста, выберите клиента.");
      return;
    }
    const editionIds = formData.order_items.map((item) => item.edition_id);
    const uniqueEditionIds = new Set(editionIds);
    if (editionIds.length !== uniqueEditionIds.size) {
      alert("Выбраны дублирующиеся издания в позициях заказа.");
      return;
    }
    for (const item of formData.order_items) {
      if (!item.edition_id) {
        alert("Пожалуйста, выберите издание для каждой позиции.");
        return;
      }
      if (item.quantity < 1) {
        alert("Количество должно быть минимум 1.");
        return;
      }
    }

    const payload = {
      customer_id: formData.customer_id,
      date_ordered: formData.date_ordered,
      order_items: formData.order_items.map((item) => ({
        edition_id: item.edition_id,
        quantity: item.quantity,
      })),
    };

    try {
      if (isEditMode && selectedOrder) {
        // Обновление существующего заказа
        const res = await api.put(`api/orders/${selectedOrder.id}/`, payload);
        if (res.data) {
          setOrders(
            orders.map((o) => (o.id === selectedOrder.id ? res.data : o))
          );
          handleClose();
        }
      } else {
        // Создание нового заказа
        const res = await api.post("api/orders/", payload);
        if (res.data) {
          setOrders([...orders, res.data]);
          handleClose();
        }
      }
    } catch (error: any) {
      console.error(
        isEditMode
          ? "Ошибка при обновлении заказа:"
          : "Ошибка при создании заказа:",
        error
      );
      if (error.response && error.response.data) {
        alert(
          isEditMode
            ? `Не удалось обновить заказ: ${JSON.stringify(
                error.response.data
              )}`
            : `Не удалось создать заказ: ${JSON.stringify(error.response.data)}`
        );
      } else {
        alert(
          isEditMode
            ? "Не удалось обновить заказ. Проверьте введённые данные."
            : "Не удалось создать заказ. Проверьте введённые данные."
        );
      }
    }
  };

  // Функция для получения доступных изданий, исключая уже выбранные
  const getAvailableEditions = (currentIndex: number) => {
    const selectedEditionIds = formData.order_items
      .map((item, index) => (index !== currentIndex ? item.edition_id : null))
      .filter((id) => id !== null);
    return editions.filter(
      (edition) => !selectedEditionIds.includes(edition.id)
    );
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold">Заказы</h2>
        <Button onClick={handleOpenAdd}>Добавить заказ</Button>
      </div>

      <SearchBar value={search} onChange={setSearch} />

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ID</TableHead>
            <TableHead>Клиент</TableHead>
            <TableHead>Дата заказа</TableHead>
            <TableHead>Количество позиций</TableHead>
            <TableHead>Действия</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {filtered.map((order) => (
            <TableRow key={order.id}>
              <TableCell>{order.id}</TableCell>
              <TableCell>{order.customer.name}</TableCell>
              <TableCell>{order.date_ordered}</TableCell>
              <TableCell>{order.order_items.length}</TableCell>
              <TableCell className="flex space-x-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleOpenEdit(order)}
                >
                  <EditIcon className="h-4 w-4" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleDelete(order.id)}
                >
                  <TrashIcon className="h-4 w-4 text-red-500" />
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      {/* Диалог для добавления/редактирования заказа */}
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="sm:max-w-[700px]">
          <DialogHeader>
            <DialogTitle>
              {isEditMode ? "Редактировать заказ" : "Новый заказ"}
            </DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            {/* Выбор клиента */}
            <div>
              <Label htmlFor="customer" className="block mb-1">
                Клиент<span className="text-red-500">*</span>
              </Label>
              <Select
                onValueChange={(value) =>
                  handleFormChange("customer_id", Number(value))
                }
                value={
                  formData.customer_id ? formData.customer_id.toString() : ""
                }
              >
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Выберите клиента" />
                </SelectTrigger>
                <SelectContent>
                  {customers.map((customer) => (
                    <SelectItem
                      key={customer.id}
                      value={customer.id.toString()}
                    >
                      {customer.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Выбор даты заказа */}
            <div>
              <Label htmlFor="date_ordered" className="block mb-1">
                Дата заказа<span className="text-red-500">*</span>
              </Label>
              <Input
                id="date_ordered"
                type="date"
                value={formData.date_ordered}
                onChange={(e) =>
                  handleFormChange("date_ordered", e.target.value)
                }
              />
            </div>

            {/* Позиции заказа */}
            <div>
              <Label className="block mb-1">
                Позиции заказа<span className="text-red-500">*</span>
              </Label>
              {formData.order_items.map((item, index) => (
                <div key={index} className="flex items-end space-x-4 mb-2">
                  {/* Выбор издания */}
                  <div className="flex-1">
                    <Label htmlFor={`edition-${index}`} className="block mb-1">
                      Издание<span className="text-red-500">*</span>
                    </Label>
                    <Select
                      onValueChange={(value) =>
                        handleOrderItemChange(
                          index,
                          "edition_id",
                          Number(value)
                        )
                      }
                      value={item.edition_id ? item.edition_id.toString() : ""}
                    >
                      <SelectTrigger className="w-full">
                        <SelectValue placeholder="Выберите издание" />
                      </SelectTrigger>
                      <SelectContent>
                        {getAvailableEditions(index).map((edition) => (
                          <SelectItem
                            key={edition.id}
                            value={edition.id.toString()}
                          >
                            {edition.book.title} - Издание{" "}
                            {edition.edition_number}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Ввод количества */}
                  <div className="w-24">
                    <Label htmlFor={`quantity-${index}`} className="block mb-1">
                      Количество<span className="text-red-500">*</span>
                    </Label>
                    <Input
                      id={`quantity-${index}`}
                      type="number"
                      min={1}
                      value={item.quantity}
                      onChange={(e) =>
                        handleOrderItemChange(
                          index,
                          "quantity",
                          Number(e.target.value)
                        )
                      }
                    />
                  </div>

                  {/* Кнопка удаления позиции */}
                  {formData.order_items.length > 1 && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => removeOrderItem(index)}
                      className="mt-4"
                    >
                      <TrashIcon className="h-4 w-4 text-red-500" />
                    </Button>
                  )}
                </div>
              ))}

              {/* Кнопка добавления позиции */}
              <Button variant="outline" size="sm" onClick={addOrderItem}>
                Добавить позицию
              </Button>
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
