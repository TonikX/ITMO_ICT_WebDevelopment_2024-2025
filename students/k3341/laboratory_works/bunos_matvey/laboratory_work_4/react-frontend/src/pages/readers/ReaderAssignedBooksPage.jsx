// src/pages/readers/ReaderAssignedBooksPage.jsx
import React, { useEffect, useState, useContext } from 'react';
import { Table, Button, notification, Typography } from 'antd';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../../context/AuthContext';

const { Title } = Typography;

function ReaderAssignedBooksPage() {
  const { authToken } = useContext(AuthContext);
  const { id } = useParams(); // ID читателя
  const [reader, setReader] = useState(null);
  const [assignedBooks, setAssignedBooks] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchReader = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`http://localhost:8000/api/readers/${id}/`, {
        headers: { Authorization: `Token ${authToken}` },
      });
      setReader(res.data);
      setAssignedBooks(res.data.assigned_books.map(book => book.book) || []);
    } catch (error) {
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
      <p>ФИО: {reader?.full_name || '...'}</p>

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
