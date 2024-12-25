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

interface Book {
  id: number;
  title: string;
}

interface Author {
  id: number;
  first_name: string;
  last_name: string;
  biography: string;
  email?: string;
  phone_number?: string;
}

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
}

function SearchBar({ value, onChange }: SearchBarProps) {
  return (
    <div className="my-4">
      <Input
        placeholder="Поиск по имени или фамилии автора..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}

export const AuthorsTab: React.FC = () => {
  const [authors, setAuthors] = useState<Author[]>([]);
  const [search, setSearch] = useState<string>("");
  const [selectedAuthor, setSelectedAuthor] = useState<Author | null>(null);
  const [authorDialogOpen, setAuthorDialogOpen] = useState<boolean>(false);
  const [authorBooks, setAuthorBooks] = useState<Book[]>([]);

  useEffect(() => {
    const fetchAuthors = async () => {
      const res = await api.get("api/authors");
      if (res.data) {
        setAuthors(res.data);
      }
    };
    fetchAuthors();
  }, []);

  const filtered = authors.filter((author) => {
    const fullName = `${author.first_name} ${author.last_name}`.toLowerCase();
    const searchLower = search.toLowerCase();
    return fullName.includes(searchLower);
  });

  async function handleAuthorClick(author: Author) {
    setSelectedAuthor(author);
    // Делаем запрос за книгами, связанными с этим автором
    // Предполагается, что API поддерживает фильтрацию по author_id
    const res = await api.get(`api/books?author_id=${author.id}`);
    if (res.data) {
      setAuthorBooks(res.data);
    } else {
      setAuthorBooks([]);
    }

    setAuthorDialogOpen(true);
  }

  return (
    <div>
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold">Авторы</h2>
        {/* Если нужно добавлять авторов, можно реализовать */}
      </div>

      <SearchBar value={search} onChange={setSearch} />

      {/* Диалог для просмотра детальной информации об авторе */}
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
              {authorBooks && authorBooks.length > 0 && (
                <div>
                  <strong>Книги автора:</strong>{" "}
                  {authorBooks.map((b) => b.title).join(", ")}
                </div>
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
            <TableHead>Имя</TableHead>
            <TableHead>Фамилия</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {filtered.map((author) => (
            <TableRow key={author.id}>
              <TableCell className="font-medium">
                <button
                  type="button"
                  className="text-blue-500 underline hover:text-blue-700"
                  onClick={() => handleAuthorClick(author)}
                >
                  {author.first_name}
                </button>
              </TableCell>
              <TableCell>
                <button
                  type="button"
                  className="text-blue-500 underline hover:text-blue-700"
                  onClick={() => handleAuthorClick(author)}
                >
                  {author.last_name}
                </button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};
