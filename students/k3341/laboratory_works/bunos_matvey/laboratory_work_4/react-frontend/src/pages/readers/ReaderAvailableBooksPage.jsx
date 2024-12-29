// src/pages/readers/ReaderAvailableBooksPage.jsx
import React, { useEffect, useState, useContext } from 'react';
import { Table, Button, notification, Typography } from 'antd';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../../context/AuthContext';

const { Title } = Typography;

function ReaderAvailableBooksPage() {
  const { authToken } = useContext(AuthContext);
  const { id } = useParams(); // ID читателя

  const [reader, setReader] = useState(null);
  const [allBooks, setAllBooks] = useState([]);
  const [availableBooks, setAvailableBooks] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      // 1) Получить данные читателя (и список уже assigned_books)
      const readerRes = await axios.get(`http://localhost:8000/api/readers/${id}/`, {
        headers: { Authorization: `Token ${authToken}` },
      });
      setReader(readerRes.data);
      const assignedBooks = readerRes.data.assigned_books || [];

      // 2) Получить все книги
      const booksRes = await axios.get(`http://localhost:8000/api/books/`, {
        headers: { Authorization: `Token ${authToken}` },
      });
      setAllBooks(booksRes.data);

      // 3) Отфильтруем
      const assignedIds = assignedBooks.map((b) => b.id);
      const notAssigned = booksRes.data.filter((bk) => !assignedIds.includes(bk.id));
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
        `http://localhost:8000/api/books/${bookId}/assign_to_reader/`,
        { reader_id: id },
        { headers: { Authorization: `Token ${authToken}` } }
      );
      notification.success({ message: `Книга #${bookId} назначена` });
      // Удалим из availableBooks (или пересчитаем fetchData())
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

  console.log(availableBooks)

  return (
    <div style={{ background: '#fff', padding: 24 }}>
      <Title level={3}>Назначить книги читателю #{id}</Title>
      <p>ФИО: {reader?.full_name || '...'}</p>

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
