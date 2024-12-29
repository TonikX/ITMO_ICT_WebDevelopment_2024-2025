# Отчёт по фронтенду приложения Library

Данный документ описывает реализацию клиентской части (React + Vite + Ant Design) приложения **Library**, в котором можно управлять сущностями (например, книги, читатели) и выполнять специфические операции (назначение книг, отвязка книг, отображение статистических отчётов и т.д.). 

## 1. Структура и технологии

Всё находится в папке `react-frontend/`, которая содержит:

```
react-frontend/
├── index.html
├── vite.config.js
├── package.json
├── src/
│   ├── App.jsx
│   ├── main.jsx
│   ├── pages/
│   ├── routes/
│   ├── layout/
│   ├── context/
│   └── services/
└── ...
```

- **React**: основа фронтенд-приложения.
- **Vite**: инструмент для быстрой сборки и запуска в режиме разработки.
- **Ant Design**: библиотека UI-компонентов (таблицы, формы, кнопки и т.д.).
- **Axios**: для HTTP-запросов к API.
- **React Router**: для организации клиентской навигации (роутинг).

## 2. Пример роутинга

```jsx
// src/routes/AppRouter.jsx

import React from 'react';
import { Routes, Route } from 'react-router-dom';
import MainLayout from '../layout/MainLayout';
import BooksListPage from '../pages/books/BooksListPage';
import BookFormPage from '../pages/books/BookFormPage';
import ReadersListPage from '../pages/readers/ReadersListPage';
import ReaderAssignedBooksPage from '../pages/readers/ReaderAssignedBooksPage';
import ReaderAvailableBooksPage from '../pages/readers/ReaderAvailableBooksPage';

function AppRouter() {
  return (
    <Routes>
      <Route
        path="/books"
        element={
          <MainLayout>
            <BooksListPage />
          </MainLayout>
        }
      />
      <Route
        path="/books/create"
        element={
          <MainLayout>
            <BookFormPage />
          </MainLayout>
        }
      />
      <Route
        path="/books/:id"
        element={
          <MainLayout>
            <BookFormPage />
          </MainLayout>
        }
      />
      <Route
        path="/readers"
        element={
          <MainLayout>
            <ReadersListPage />
          </MainLayout>
        }
      />
      <Route
        path="/readers/:id/books-assigned"
        element={
          <MainLayout>
            <ReaderAssignedBooksPage />
          </MainLayout>
        }
      />
      <Route
        path="/readers/:id/books-available"
        element={
          <MainLayout>
            <ReaderAvailableBooksPage />
          </MainLayout>
        }
      />
    </Routes>
  );
}

export default AppRouter;
```

## 3. Страница списка книг

```jsx
// src/pages/books/BooksListPage.jsx

import React, { useEffect, useState, useContext } from 'react';
import { Table, Button, Popconfirm, notification } from 'antd';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../../context/AuthContext';

function BooksListPage() {
  const { authToken } = useContext(AuthContext);
  const navigate = useNavigate();
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchBooks = async () => {
    setLoading(true);
    try {
      const res = await axios.get('http://localhost:8000/books/', {
        headers: { Authorization: `Token ${authToken}` },
      });
      setBooks(res.data);
    } catch {
      notification.error({ message: 'Ошибка при загрузке книг' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBooks();
  }, []);

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/books/${id}/`, {
        headers: { Authorization: `Token ${authToken}` },
      });
      notification.success({ message: 'Книга удалена' });
      fetchBooks();
    } catch {
      notification.error({ message: 'Ошибка при удалении книги' });
    }
  };

  const columns = [
    { title: 'ID', dataIndex: 'id', width: 60 },
    { title: 'Название', dataIndex: 'title' },
    {
      title: 'Действия',
      key: 'actions',
      render: (_, record) => (
        <>
          <Button type="link" onClick={() => navigate(`/books/${record.id}`)}>
            Редактировать
          </Button>
          <Popconfirm
            title="Удалить книгу?"
            onConfirm={() => handleDelete(record.id)}
          >
            <Button type="link" danger>
              Удалить
            </Button>
          </Popconfirm>
        </>
      ),
    },
  ];

  return (
    <div style={{ background: '#fff', padding: 24 }}>
      <h2>Список книг</h2>
      <Button
        type="primary"
        onClick={() => navigate('/books/create')}
        style={{ marginBottom: 16 }}
      >
        Создать книгу
      </Button>
      <Table
        rowKey="id"
        columns={columns}
        dataSource={books}
        loading={loading}
      />
    </div>
  );
}

export default BooksListPage;
```

## 4. Форма книги (создание/редактирование)

```jsx
// src/pages/books/BookFormPage.jsx

import React, { useState, useEffect, useContext } from 'react';
import { Form, Input, InputNumber, Select, Button, notification } from 'antd';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../../context/AuthContext';

function BookFormPage() {
  const { authToken } = useContext(AuthContext);
  const { id } = useParams();
  const isEdit = !!id;
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const [authors, setAuthors] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    axios.get('http://localhost:8000/authors/', {
      headers: { Authorization: `Token ${authToken}` },
    }).then((res) => setAuthors(res.data));

    if (isEdit) {
      setLoading(true);
      axios.get(`http://localhost:8000/books/${id}/`, {
        headers: { Authorization: `Token ${authToken}` },
      })
      .then((res) => {
        form.setFieldsValue({
          book_code: res.data.book_code,
          title: res.data.title,
          publisher: res.data.publisher,
          year_of_publication: res.data.year_of_publication,
          section: res.data.section,
          authors: res.data.authors,
        });
      })
      .catch(() => {
        notification.error({ message: 'Ошибка при загрузке книги' });
      })
      .finally(() => setLoading(false));
    }
  }, [isEdit, id]);

  const onFinish = async (values) => {
    setLoading(true);
    try {
      let bookId = id;
      if (isEdit) {
        await axios.patch(`http://localhost:8000/books/${bookId}/`, {
          book_code: values.book_code,
          title: values.title,
          publisher: values.publisher,
          year_of_publication: values.year_of_publication,
          section: values.section,
        }, {
          headers: { Authorization: `Token ${authToken}` },
        });
      } else {
        const res = await axios.post(`http://localhost:8000/books/`, {
          book_code: values.book_code,
          title: values.title,
          publisher: values.publisher,
          year_of_publication: values.year_of_publication,
          section: values.section,
        }, {
          headers: { Authorization: `Token ${authToken}` },
        });
        bookId = res.data.id;
      }

      // Кастомный эндпоинт для авторов
      await axios.post(
        `http://localhost:8000/books/${bookId}/set_authors/`,
        { authors: values.authors || [] },
        { headers: { Authorization: `Token ${authToken}` } }
      );

      notification.success({ message: 'Книга сохранена' });
      navigate('/books');
    } catch {
      notification.error({ message: 'Ошибка при сохранении книги' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ background: '#fff', padding: 24, maxWidth: 800 }}>
      <h2>{isEdit ? 'Редактирование книги' : 'Создание книги'}</h2>
      <Form form={form} layout="vertical" onFinish={onFinish} disabled={loading}>
        <Form.Item
          label="Шифр книги"
          name="book_code"
          rules={[{ required: true, message: 'Укажите шифр книги' }]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Название"
          name="title"
          rules={[{ required: true, message: 'Укажите название' }]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Издательство"
          name="publisher"
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Год издания"
          name="year_of_publication"
        >
          <InputNumber style={{ width: '100%' }} />
        </Form.Item>

        <Form.Item
          label="Раздел"
          name="section"
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Авторы"
          name="authors"
        >
          <Select mode="multiple">
            {authors.map((author) => (
              <Select.Option key={author.id} value={author.id}>
                {author.name}
              </Select.Option>
            ))}
          </Select>
        </Form.Item>

        <Button type="primary" htmlType="submit" loading={loading}>
          Сохранить
        </Button>
      </Form>
    </div>
  );
}

export default BookFormPage;
```

## 5. Страница читателя: уже привязанные книги

```jsx
// src/pages/readers/ReaderAssignedBooksPage.jsx

import React, { useEffect, useState, useContext } from 'react';
import { Table, Button, notification, Typography } from 'antd';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../../context/AuthContext';

const { Title } = Typography;

function ReaderAssignedBooksPage() {
  const { authToken } = useContext(AuthContext);
  const { id } = useParams();
  const [reader, setReader] = useState(null);
  const [assignedBooks, setAssignedBooks] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchReader = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`http://localhost:8000/readers/${id}/`, {
        headers: { Authorization: `Token ${authToken}` },
      });
      setReader(res.data);
      setAssignedBooks(res.data.assigned_books || []);
    } catch {
      notification.error({ message: 'Ошибка при загрузке читателя' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReader();
  }, [id]);

  const handleUnassign = async (bookId) => {
    try {
      await axios.post(
        `http://localhost:8000/api/books/${bookId}/unassign_from_reader/`,
        { reader_id: id },
        { headers: { Authorization: `Token ${authToken}` } }
      );
      notification.success({ message: `Книга #${bookId} отвязана` });
      setAssignedBooks((prev) => prev.filter((b) => b.id !== bookId));
    } catch {
      notification.error({ message: 'Ошибка при отвязке книги' });
    }
  };

  const columns = [
    { title: 'ID', dataIndex: 'id', width: 60 },
    { title: 'Название', dataIndex: 'title' },
    {
      title: 'Действие',
      render: (_, record) => (
        <Button danger onClick={() => handleUnassign(record.id)}>
          Отвязать
        </Button>
      ),
    },
  ];

  return (
    <div style={{ background: '#fff', padding: 24 }}>
      <Title level={3}>Текущие книги у читателя #{id}</Title>
      <p>ФИО: {reader?.full_name}</p>

      <Table
        rowKey="id"
        columns={columns}
        dataSource={assignedBooks}
        loading={loading}
      />
    </div>
  );
}

export default ReaderAssignedBooksPage;
```

## 6. Страница читателя: все доступные для назначения книги

```jsx
// src/pages/readers/ReaderAvailableBooksPage.jsx

import React, { useEffect, useState, useContext } from 'react';
import { Table, Button, notification, Typography } from 'antd';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../../context/AuthContext';

const { Title } = Typography;

function ReaderAvailableBooksPage() {
  const { authToken } = useContext(AuthContext);
  const { id } = useParams();
  const [reader, setReader] = useState(null);
  const [availableBooks, setAvailableBooks] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const readerRes = await axios.get(`http://localhost:8000/readers/${id}/`, {
        headers: { Authorization: `Token ${authToken}` },
      });
      setReader(readerRes.data);
      const assignedIds = (readerRes.data.assigned_books || []).map((b) => b.id);

      const booksRes = await axios.get(`http://localhost:8000/books/`, {
        headers: { Authorization: `Token ${authToken}` },
      });
      const allBooks = booksRes.data;
      const notAssigned = allBooks.filter((bk) => !assignedIds.includes(bk.id));
      setAvailableBooks(notAssigned);
    } catch {
      notification.error({ message: 'Ошибка при загрузке данных' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [id]);

  const handleAssign = async (bookId) => {
    try {
      await axios.post(
        `http://localhost:8000/readers/${id}/assign_book/`,
        { book_id: bookId },
        { headers: { Authorization: `Token ${authToken}` } }
      );
      notification.success({ message: `Книга #${bookId} назначена` });
      setAvailableBooks((prev) => prev.filter((b) => b.id !== bookId));
    } catch {
      notification.error({ message: 'Ошибка при назначении книги' });
    }
  };

  const columns = [
    { title: 'ID', dataIndex: 'id', width: 60 },
    { title: 'Название', dataIndex: 'title' },
    {
      title: 'Действие',
      render: (_, record) => (
        <Button type="primary" onClick={() => handleAssign(record.id)}>
          Привязать
        </Button>
      ),
    },
  ];

  return (
    <div style={{ background: '#fff', padding: 24 }}>
      <Title level={3}>Назначить книги читателю #{id}</Title>
      <p>ФИО: {reader?.full_name}</p>

      <Table
        rowKey="id"
        columns={columns}
        dataSource={availableBooks}
        loading={loading}
      />
    </div>
  );
}

export default ReaderAvailableBooksPage;
```

## 7. Запуск

1. Установить зависимости:
```
npm install
```

2. Запустить режим разработки:
```
npm run dev
```
Приложение открывается по умолчанию на http://localhost:5173/

3. Собрать production-версию:
```
npm run build
```
Результат появится в папке `dist/`.

## 8. Итоги

В проекте **Library** на фронтенде реализован следующий функционал:
- Отдельные страницы для списка/CRUD по книгам, авторам, читателям и т.д.
- Возможность назначать книги читателю (на одной странице) и отвязывать книги (на другой).
- Формы, таблицы и элементы UI основаны на Ant Design.
- Для обмена данными с сервером используются Axios-запросы и токен-авторизация (хранение токена, передача в заголовках).