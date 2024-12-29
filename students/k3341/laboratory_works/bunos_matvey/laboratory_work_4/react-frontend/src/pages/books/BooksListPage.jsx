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
      const res = await axios.get('http://localhost:8000/api/books/', {
        headers: { Authorization: `Token ${authToken}` },
      });
      setBooks(res.data);
    } catch (error) {
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
      await axios.delete(`http://localhost:8000/api/books/${id}/`, {
        headers: { Authorization: `Token ${authToken}` },
      });
      notification.success({ message: 'Книга удалена' });
      fetchBooks();
    } catch (error) {
      notification.error({ message: 'Ошибка при удалении книги' });
    }
  };

  const columns = [
    { title: 'ID', dataIndex: 'id', width: 60 },
    { title: 'Шифр', dataIndex: 'book_code', width: 100 },
    { title: 'Название', dataIndex: 'title' },
    { title: 'Издательство', dataIndex: 'publisher' },
    {
      title: 'Действия',
      key: 'actions',
      render: (_, record) => (
        <>
          <Button type="link" onClick={() => navigate(`/books/${record.id}`)}>
            Ред.
          </Button>
          <Popconfirm title="Удалить книгу?" onConfirm={() => handleDelete(record.id)}>
            <Button type="link" danger>
              Удал.
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
