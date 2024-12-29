// src/pages/readingRooms/ReadingRoomsListPage.jsx
import React, { useEffect, useState, useContext } from 'react';
import { Table, Button, Popconfirm, notification } from 'antd';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../../context/AuthContext';

function ReadingRoomsListPage() {
  const { authToken } = useContext(AuthContext);
  const navigate = useNavigate();
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchRooms = async () => {
    setLoading(true);
    try {
      const res = await axios.get('http://localhost:8000/api/reading-rooms/', {
        headers: { Authorization: `Token ${authToken}` },
      });
      setRooms(res.data);
    } catch (error) {
      notification.error({ message: 'Ошибка при загрузке залов' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRooms();
  }, []);

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/api/reading-rooms/${id}/`, {
        headers: { Authorization: `Token ${authToken}` },
      });
      notification.success({ message: 'Зал удалён' });
      fetchRooms();
    } catch (error) {
      notification.error({ message: 'Ошибка при удалении зала' });
    }
  };

  const columns = [
    { title: 'ID', dataIndex: 'id', width: 80 },
    { title: 'Название зала', dataIndex: 'name' },
    { title: 'Вместимость', dataIndex: 'capacity', width: 120 },
    {
      title: 'Действия',
      key: 'actions',
      render: (_, record) => (
        <>
          <Button type="link" onClick={() => navigate(`/reading-rooms/${record.id}`)}>
            Редактировать
          </Button>
          <Popconfirm title="Удалить зал?" onConfirm={() => handleDelete(record.id)}>
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
      <h2>Список читальных залов</h2>
      <Button
        type="primary"
        style={{ marginBottom: 16 }}
        onClick={() => navigate('/reading-rooms/create')}
      >
        Создать зал
      </Button>

      <Table
        rowKey="id"
        columns={columns}
        dataSource={rooms}
        loading={loading}
      />
    </div>
  );
}

export default ReadingRoomsListPage;
