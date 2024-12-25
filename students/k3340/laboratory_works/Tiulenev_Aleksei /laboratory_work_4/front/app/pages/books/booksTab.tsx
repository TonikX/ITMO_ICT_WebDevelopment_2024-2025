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
import {
  TableHeader,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
  Table,
} from "@/components/ui/table";
import { api } from "@/api/api";
import { Checkbox } from "@/components/ui/checkbox";

interface Author {
  id: number;
  first_name: string;
  last_name: string;
  biography: string;
  email?: string;
  phone_number?: string;
}

interface BookAuthorData {
  author_id: number;
  position_on_cover: number;
  royalty_percentage: string;
}

interface BookAuthorDisplay {
  author_id: number;
  first_name: string;
  last_name: string;
  position_on_cover: number;
  royalty_percentage: string;
}

interface Book {
  id: number;
  title: string;
  authors: Author[];
}

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
}

function SearchBar({ value, onChange }: SearchBarProps) {
  return (
    <div className="my-4">
      <Input
        placeholder="Поиск по названию или автору..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}

export const BooksTab: React.FC = () => {
  const [books, setBooks] = useState<Book[]>([]);
  const [authors, setAuthors] = useState<Author[]>([]);
  const [search, setSearch] = useState<string>("");
  const [open, setOpen] = useState<boolean>(false);

  const [newBookTitle, setNewBookTitle] = useState<string>("");

  const [authorsData, setAuthorsData] = useState<BookAuthorData[]>([]);

  // Состояние для отображения данных о выбранном авторе
  const [selectedAuthor, setSelectedAuthor] = useState<Author | null>(null);
  const [authorDialogOpen, setAuthorDialogOpen] = useState<boolean>(false);

  useEffect(() => {
    const fetchBooks = async () => {
      const res = await api.get("api/books");
      if (res.data) {
        setBooks(res.data);
      }
    };

    const fetchAuthors = async () => {
      const res = await api.get("api/authors");
      if (res.data) {
        setAuthors(res.data);
      }
    };

    fetchBooks();
    fetchAuthors();
  }, []);

  const filtered = books.filter((b) => {
    const titleMatch = b.title.toLowerCase().includes(search.toLowerCase());
    const authorsMatch = b.authors.some(
      (a) =>
        a.first_name.toLowerCase().includes(search.toLowerCase()) ||
        a.last_name.toLowerCase().includes(search.toLowerCase())
    );
    return titleMatch || authorsMatch;
  });

  // Изменение чекбокса выбора автора
  function toggleAuthorSelection(authorId: number) {
    const index = authorsData.findIndex((a) => a.author_id === authorId);
    if (index === -1) {
      // Автор не выбран - добавляем с дефолтными значениями
      setAuthorsData([
        ...authorsData,
        {
          author_id: authorId,
          position_on_cover: 1,
          royalty_percentage: "0.00",
        },
      ]);
    } else {
      // Автор уже выбран - снимаем выбор
      setAuthorsData(authorsData.filter((a) => a.author_id !== authorId));
    }
  }

  // Проверка выбран автор или нет
  function isAuthorSelected(authorId: number) {
    return authorsData.some((a) => a.author_id === authorId);
  }

  // Обновляем поля position_on_cover и royalty_percentage для выбранного автора
  function updateAuthorField(
    authorId: number,
    field: "position_on_cover" | "royalty_percentage",
    value: string
  ) {
    setAuthorsData((prev) =>
      prev.map((a) =>
        a.author_id === authorId
          ? {
              ...a,
              [field]:
                field === "position_on_cover"
                  ? parseInt(value, 10) || 1
                  : value,
            }
          : a
      )
    );
  }

  async function addBook() {
    if (!newBookTitle.trim()) return;
    const payload = {
      title: newBookTitle,
      authors_data: authorsData,
    };
    const res = await api.post("api/books/", payload);
    if (res.data) {
      // Добавляем новую книгу в список
      setBooks([...books, res.data]);
    }
    // Сброс формы
    setNewBookTitle("");
    setAuthorsData([]);
    setOpen(false);
  }

  // Обработчик клика по автору
  function handleAuthorClick(author_id: number) {
    const foundAuthor = authors.find((a) => a.id === author_id);
    console.log(foundAuthor, authors, author_id);

    if (foundAuthor) {
      setSelectedAuthor(foundAuthor);
      setAuthorDialogOpen(true);
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold">Книги</h2>
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger asChild>
            <Button>Добавить книгу</Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Новая книга</DialogTitle>
            </DialogHeader>
            <div className="space-y-4">
              <div>
                <Label className="mb-1">Название</Label>
                <Input
                  value={newBookTitle}
                  onChange={(e) => setNewBookTitle(e.target.value)}
                />
              </div>
              <div>
                <Label className="mb-2">Авторы</Label>
                <div className="max-h-40 overflow-auto space-y-2 border p-2 rounded">
                  {authors.map((author) => {
                    const selected = isAuthorSelected(author.id);
                    const authorData = authorsData.find(
                      (a) => a.author_id === author.id
                    );
                    return (
                      <div key={author.id} className="space-y-2">
                        <div className="flex items-center space-x-2">
                          <Checkbox
                            checked={selected}
                            onCheckedChange={() =>
                              toggleAuthorSelection(author.id)
                            }
                          />
                          <span>
                            {author.first_name} {author.last_name}
                          </span>
                        </div>
                        {selected && authorData && (
                          <div className="pl-6 space-y-2">
                            <div>
                              <Label className="mb-1">Позиция на обложке</Label>
                              <Input
                                type="number"
                                value={authorData.position_on_cover}
                                onChange={(e) =>
                                  updateAuthorField(
                                    author.id,
                                    "position_on_cover",
                                    e.target.value
                                  )
                                }
                              />
                            </div>
                            <div>
                              <Label className="mb-1">Процент роялти</Label>
                              <Input
                                type="text"
                                value={authorData.royalty_percentage}
                                onChange={(e) =>
                                  updateAuthorField(
                                    author.id,
                                    "royalty_percentage",
                                    e.target.value
                                  )
                                }
                              />
                            </div>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
            <DialogFooter className="space-x-2">
              <Button variant="secondary" onClick={() => setOpen(false)}>
                Отмена
              </Button>
              <Button onClick={addBook}>Сохранить</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      <SearchBar value={search} onChange={setSearch} />

      {/* Диалог отображения подробностей автора */}
      <Dialog open={authorDialogOpen} onOpenChange={setAuthorDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {selectedAuthor
                ? `${selectedAuthor.first_name} ${selectedAuthor.last_name}`
                : "Автор"}
            </DialogTitle>
          </DialogHeader>
          {selectedAuthor && (
            <div className="space-y-4">
              <p>
                <strong>Биография:</strong>{" "}
                {selectedAuthor.biography || "Нет данных"}
              </p>
              {selectedAuthor.email && (
                <p>
                  <strong>Email:</strong> {selectedAuthor.email}
                </p>
              )}
              {selectedAuthor.phone_number && (
                <p>
                  <strong>Телефон:</strong> {selectedAuthor.phone_number}
                </p>
              )}
            </div>
          )}
          <DialogFooter>
            <Button onClick={() => setAuthorDialogOpen(false)}>Закрыть</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Название</TableHead>
            <TableHead>Авторы</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {filtered.map((book) => (
            <TableRow key={book.id}>
              <TableCell className="font-medium">{book.title}</TableCell>
              <TableCell>
                {book.authors.map((author, idx) => (
                  <React.Fragment key={author.id}>
                    <button
                      type="button"
                      className="text-blue-500 underline hover:text-blue-700"
                      onClick={() => handleAuthorClick(author.id)}
                    >
                      {author.first_name} {author.last_name}
                    </button>
                    {idx < book.authors.length - 1 && ", "}
                  </React.Fragment>
                ))}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};
