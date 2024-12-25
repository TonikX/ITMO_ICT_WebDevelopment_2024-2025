// src/components/EditionsTab.tsx

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

export interface Author {
  id: number;
  first_name: string;
  last_name: string;
  biography: string;
  email?: string;
  phone_number?: string;
}

export interface Book {
  id: number;
  title: string;
  authors: string[]; // Или более подробно, если используется AuthorSerializer
}

export interface Employee {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone_number?: string;
}

export interface EditionEditor {
  id: number;
  editor: Employee;
  editor_id: number;
  is_responsible_editor: boolean;
}

export interface Edition {
  id: number;
  book: Book;
  book_id: number;
  edition_number: number;
  publication_date: string; // ISO формат даты
  number_of_pages: number;
  has_illustrations: boolean;
  editors: EditionEditor[];
}

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
}

function SearchBar({ value, onChange }: SearchBarProps) {
  return (
    <div className="my-4">
      <Input
        placeholder="Поиск по книге или номеру издания..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}

export const EditionsTab: React.FC = () => {
  const [editions, setEditions] = useState<Edition[]>([]);
  const [books, setBooks] = useState<Book[]>([]);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [search, setSearch] = useState<string>("");
  const [open, setOpen] = useState<boolean>(false);
  const [isEditMode, setIsEditMode] = useState<boolean>(false);
  const [selectedEdition, setSelectedEdition] = useState<Edition | null>(null);

  // Формные данные для создания/редактирования издания
  const [formData, setFormData] = useState<{
    book_id: number | "";
    edition_number: number;
    publication_date: string;
    number_of_pages: number;
    has_illustrations: boolean;
    editors: {
      editor_id: number | "";
      is_responsible_editor: boolean;
    }[];
  }>({
    book_id: "",
    edition_number: 1,
    publication_date: new Date().toISOString().split("T")[0],
    number_of_pages: 100,
    has_illustrations: false,
    editors: [{ editor_id: "", is_responsible_editor: false }],
  });

  useEffect(() => {
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

    const fetchBooks = async () => {
      try {
        const res = await api.get("api/books/");
        if (res.data) {
          setBooks(res.data);
        }
      } catch (error) {
        console.error("Ошибка при загрузке книг:", error);
      }
    };

    const fetchEmployees = async () => {
      try {
        const res = await api.get("api/employees/");
        if (res.data) {
          setEmployees(
            res.data.filter((emp: { role: string }) => emp.role === "Editor")
          );
        }
      } catch (error) {
        console.error("Ошибка при загрузке редакторов:", error);
      }
    };

    fetchEditions();
    fetchBooks();
    fetchEmployees();
  }, []);

  const filteredEditions = editions.filter((edition) => {
    const bookTitle = edition.book.title.toLowerCase();
    const editionNumber = edition.edition_number.toString();
    const searchLower = search.toLowerCase();
    return (
      bookTitle.includes(searchLower) || editionNumber.includes(searchLower)
    );
  });

  const handleOpenAdd = () => {
    setIsEditMode(false);
    setFormData({
      book_id: "",
      edition_number: 1,
      publication_date: new Date().toISOString().split("T")[0],
      number_of_pages: 100,
      has_illustrations: false,
      editors: [{ editor_id: "", is_responsible_editor: false }],
    });
    setOpen(true);
  };

  const handleOpenEdit = (edition: Edition) => {
    setIsEditMode(true);
    setSelectedEdition(edition);
    setFormData({
      book_id: edition.book.id,
      edition_number: edition.edition_number,
      publication_date: edition.publication_date,
      number_of_pages: edition.number_of_pages,
      has_illustrations: edition.has_illustrations,
      editors: edition.editors.map((ed) => ({
        editor_id: ed.editor.id,
        is_responsible_editor: ed.is_responsible_editor,
      })),
    });
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setSelectedEdition(null);
    setFormData({
      book_id: "",
      edition_number: 1,
      publication_date: new Date().toISOString().split("T")[0],
      number_of_pages: 100,
      has_illustrations: false,
      editors: [{ editor_id: "", is_responsible_editor: false }],
    });
  };

  const handleDelete = async (editionId: number) => {
    if (window.confirm("Вы уверены, что хотите удалить это издание?")) {
      try {
        await api.delete(`api/editions/${editionId}/`);
        setEditions(editions.filter((e) => e.id !== editionId));
      } catch (error) {
        console.error("Ошибка при удалении издания:", error);
        alert("Не удалось удалить издание. Попробуйте позже.");
      }
    }
  };

  const handleFormChange = (field: keyof typeof formData, value: any) => {
    setFormData({
      ...formData,
      [field]: value,
    });
  };

  const handleEditorChange = (
    index: number,
    field: keyof (typeof formData.editors)[number],
    value: any
  ) => {
    const updatedEditors = [...formData.editors];
    updatedEditors[index] = {
      ...updatedEditors[index],
      [field]: value,
    };
    setFormData({
      ...formData,
      editors: updatedEditors,
    });
  };

  const addEditor = () => {
    setFormData({
      ...formData,
      editors: [
        ...formData.editors,
        { editor_id: "", is_responsible_editor: false },
      ],
    });
  };

  const removeEditor = (index: number) => {
    const updatedEditors = formData.editors.filter((_, i) => i !== index);
    setFormData({
      ...formData,
      editors: updatedEditors,
    });
  };

  const handleFormSubmit = async () => {
    // Валидация
    if (!formData.book_id) {
      alert("Пожалуйста, выберите книгу.");
      return;
    }
    if (formData.editors.length === 0) {
      alert("Пожалуйста, назначьте хотя бы одного редактора.");
      return;
    }
    const editorIds = formData.editors.map((ed) => ed.editor_id);
    const uniqueEditorIds = new Set(editorIds);
    if (editorIds.length !== uniqueEditorIds.size) {
      alert("Назначены дублирующиеся редакторы.");
      return;
    }
    const responsibleEditors = formData.editors.filter(
      (ed) => ed.is_responsible_editor
    );
    if (responsibleEditors.length > 1) {
      alert("Только один редактор может быть ответственным.");
      return;
    }
    for (const editor of formData.editors) {
      if (!editor.editor_id) {
        alert("Пожалуйста, выберите редактора для каждой позиции.");
        return;
      }
    }

    const payload = {
      book_id: formData.book_id,
      edition_number: formData.edition_number,
      publication_date: formData.publication_date,
      number_of_pages: formData.number_of_pages,
      has_illustrations: formData.has_illustrations,
      edition_editors: formData.editors.map((ed) => ({
        editor_id: ed.editor_id,
        is_responsible_editor: ed.is_responsible_editor,
      })),
    };

    try {
      if (isEditMode && selectedEdition) {
        // Обновление существующего издания
        const res = await api.put(
          `api/editions/${selectedEdition.id}/`,
          payload
        );
        if (res.data) {
          setEditions(
            editions.map((e) => (e.id === selectedEdition.id ? res.data : e))
          );
          handleClose();
        }
      } else {
        // Создание нового издания
        const res = await api.post("api/editions/", payload);
        if (res.data) {
          setEditions([...editions, res.data]);
          handleClose();
        }
      }
    } catch (error: any) {
      console.error(
        isEditMode
          ? "Ошибка при обновлении издания:"
          : "Ошибка при создании издания:",
        error
      );
      if (error.response && error.response.data) {
        const errorMessages = [];
        for (const key in error.response.data) {
          if (Array.isArray(error.response.data[key])) {
            error.response.data[key].forEach((msg: string) => {
              errorMessages.push(`${key}: ${msg}`);
            });
          } else {
            errorMessages.push(`${key}: ${error.response.data[key]}`);
          }
        }
        alert(
          isEditMode
            ? `Не удалось обновить издание:\n${errorMessages.join("\n")}`
            : `Не удалось создать издание:\n${errorMessages.join("\n")}`
        );
      } else {
        alert(
          isEditMode
            ? "Не удалось обновить издание. Проверьте введённые данные."
            : "Не удалось создать издание. Проверьте введённые данные."
        );
      }
    }
  };

  // Функция для получения доступных редакторов, исключая уже выбранных
  const getAvailableEditors = (currentIndex: number) => {
    const selectedEditorIds = formData.editors
      .map((ed, index) => (index !== currentIndex ? ed.editor_id : null))
      .filter((id) => id !== null);
    return employees.filter((emp) => !selectedEditorIds.includes(emp.id));
  };
  console.log(filteredEditions);

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold">Издания</h2>
        <Button onClick={handleOpenAdd}>Добавить издание</Button>
      </div>

      <SearchBar value={search} onChange={setSearch} />

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ID</TableHead>
            <TableHead>Книга</TableHead>
            <TableHead>Номер издания</TableHead>
            <TableHead>Дата публикации</TableHead>
            <TableHead>Кол-во страниц</TableHead>
            <TableHead>Иллюстрации</TableHead>
            <TableHead>Редакторы</TableHead>
            <TableHead>Действия</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {filteredEditions.map((edition) => (
            <TableRow key={edition.id}>
              <TableCell>{edition.id}</TableCell>
              <TableCell>{edition.book.title}</TableCell>
              <TableCell>{edition.edition_number}</TableCell>
              <TableCell>{edition.publication_date}</TableCell>
              <TableCell>{edition.number_of_pages}</TableCell>
              <TableCell>{edition.has_illustrations ? "Да" : "Нет"}</TableCell>
              <TableCell>
                {edition.editors.map((ed) => (
                  <div key={ed.id}>
                    {ed.editor.first_name} {ed.editor.last_name}
                    {ed.is_responsible_editor && " (Ответственный)"}
                  </div>
                ))}
              </TableCell>
              <TableCell className="flex space-x-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleOpenEdit(edition)}
                >
                  <EditIcon className="h-4 w-4" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleDelete(edition.id)}
                >
                  <TrashIcon className="h-4 w-4 text-red-500" />
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      {/* Диалог для создания/редактирования издания */}
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="sm:max-w-[700px]">
          <DialogHeader>
            <DialogTitle>
              {isEditMode ? "Редактировать издание" : "Новое издание"}
            </DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            {/* Выбор книги */}
            <div>
              <Label htmlFor="book" className="block mb-1">
                Книга<span className="text-red-500">*</span>
              </Label>
              <Select
                onValueChange={(value) =>
                  handleFormChange("book_id", Number(value))
                }
                value={formData.book_id ? formData.book_id.toString() : ""}
              >
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Выберите книгу" />
                </SelectTrigger>
                <SelectContent>
                  {books.map((book) => (
                    <SelectItem key={book.id} value={book.id.toString()}>
                      {book.title}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Номер издания */}
            <div>
              <Label htmlFor="edition_number" className="block mb-1">
                Номер издания<span className="text-red-500">*</span>
              </Label>
              <Input
                id="edition_number"
                type="number"
                min={1}
                value={formData.edition_number}
                onChange={(e) =>
                  handleFormChange("edition_number", Number(e.target.value))
                }
              />
            </div>

            {/* Дата публикации */}
            <div>
              <Label htmlFor="publication_date" className="block mb-1">
                Дата публикации<span className="text-red-500">*</span>
              </Label>
              <Input
                id="publication_date"
                type="date"
                value={formData.publication_date}
                onChange={(e) =>
                  handleFormChange("publication_date", e.target.value)
                }
              />
            </div>

            {/* Количество страниц */}
            <div>
              <Label htmlFor="number_of_pages" className="block mb-1">
                Количество страниц<span className="text-red-500">*</span>
              </Label>
              <Input
                id="number_of_pages"
                type="number"
                min={1}
                value={formData.number_of_pages}
                onChange={(e) =>
                  handleFormChange("number_of_pages", Number(e.target.value))
                }
              />
            </div>

            {/* Наличие иллюстраций */}
            <div className="flex items-center">
              <Label htmlFor="has_illustrations" className="mr-2">
                Иллюстрации:
              </Label>
              <input
                id="has_illustrations"
                type="checkbox"
                checked={formData.has_illustrations}
                onChange={(e) =>
                  handleFormChange("has_illustrations", e.target.checked)
                }
              />
            </div>

            {/* Управление редакторами */}
            <div>
              <Label className="block mb-1">
                Назначение редакторов<span className="text-red-500">*</span>
              </Label>
              {formData.editors.map((editor, index) => (
                <div key={index} className="flex items-center space-x-2 mb-2">
                  {/* Выбор редактора */}
                  <Select
                    onValueChange={(value) =>
                      handleEditorChange(index, "editor_id", Number(value))
                    }
                    value={editor.editor_id ? editor.editor_id.toString() : ""}
                  >
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="Выберите редактора" />
                    </SelectTrigger>
                    <SelectContent className="flex-1">
                      {getAvailableEditors(index).map((emp) => (
                        <SelectItem key={emp.id} value={emp.id.toString()}>
                          {emp.first_name} {emp.last_name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>

                  {/* Чекбокс ответственного редактора */}
                  <div className="flex items-center">
                    <Label htmlFor={`responsible-${index}`} className="mr-2">
                      Ответственный:
                    </Label>
                    <input
                      id={`responsible-${index}`}
                      type="checkbox"
                      checked={editor.is_responsible_editor}
                      onChange={(e) =>
                        handleEditorChange(
                          index,
                          "is_responsible_editor",
                          e.target.checked
                        )
                      }
                    />
                  </div>

                  {/* Кнопка удаления редактора */}
                  {formData.editors.length > 1 && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => removeEditor(index)}
                    >
                      <TrashIcon className="h-4 w-4 text-red-500" />
                    </Button>
                  )}
                </div>
              ))}

              {/* Кнопка добавления редактора */}
              <Button variant="outline" size="sm" onClick={addEditor}>
                Добавить редактора
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
