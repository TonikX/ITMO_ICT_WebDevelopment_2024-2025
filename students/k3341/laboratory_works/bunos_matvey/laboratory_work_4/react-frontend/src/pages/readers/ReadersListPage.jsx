// src/pages/readers/ReadersListPage.jsx
import React, { useEffect, useState, useContext } from 'react';
import { Table, Button, Popconfirm, notification } from 'antd';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../../context/AuthContext';

function ReadersListPage() {
  const { authToken } = useContext(AuthContext);
  const navigate = useNavigate();
  const [readers, setReaders] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchReaders = async () => {
    setLoading(true);
    try {
      const res = await axios.get('http://localhost:8000/api/readers/', {
        headers: { Authorization: `Token ${authToken}` },
      });
      setReaders(res.data);
    } catch (error) {
      notification.error({ message: 'Ошибка при загрузке читателей' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReaders();
  }, []);

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/api/readers/${id}/`, {
        headers: { Authorization: `Token ${authToken}` },
      });
      notification.success({ message: 'Читатель удалён' });
      fetchReaders();
    } catch (error) {
      notification.error({ message: 'Ошибка при удалении читателя' });
    }
  };

  const columns = [
    { title: 'ID', dataIndex: 'id', width: 60 },
    { title: 'ФИО', dataIndex: 'full_name' },
    { title: 'Номер билета', dataIndex: 'reader_card_number' },
    {
      title: 'Действия',
      key: 'actions',
      render: (_, record) => (
        <>
        <Button
            onClick={() => navigate(`/readers/${record.id}/books-assigned`)}
            type="link"
          >
            Текущие книги
          </Button>
          <Button
            onClick={() => navigate(`/readers/${record.id}/books-available`)}
            type="link"
          >
            Назначить новую книгу
          </Button>
          <Button type="link" onClick={() => navigate(`/readers/${record.id}`)}>
            Ред.
          </Button>
          <Popconfirm
            title="Удалить читателя?"
            onConfirm={() => handleDelete(record.id)}
          >
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
      <h2>Список читателей</h2>
      <Button
        type="primary"
        style={{ marginBottom: 16 }}
        onClick={() => navigate('/readers/create')}
      >
        Новый читатель
      </Button>

      <Table
        rowKey="id"
        columns={columns}
        dataSource={readers}
        loading={loading}
      />
    </div>
  );
}

export default ReadersListPage;
