// src/pages/authors/AuthorsListPage.jsx
import React, { useEffect, useState, useContext } from 'react';
import { Table, Button, Popconfirm, notification } from 'antd';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../../context/AuthContext';

function AuthorsListPage() {
  const { authToken } = useContext(AuthContext);
  const navigate = useNavigate();
  const [authors, setAuthors] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchAuthors = async () => {
    setLoading(true);
    try {
      const res = await axios.get('http://localhost:8000/api/authors/', {
        headers: { Authorization: `Token ${authToken}` },
      });
      setAuthors(res.data);
    } catch (error) {
      notification.error({
        message: 'Ошибка при загрузке авторов',
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAuthors();
  }, []);

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/api/authors/${id}/`, {
        headers: { Authorization: `Token ${authToken}` },
      });
      notification.success({ message: 'Автор успешно удалён' });
      fetchAuthors();
    } catch (error) {
      notification.error({ message: 'Ошибка при удалении автора' });
    }
  };

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      width: 80,
    },
    {
      title: 'Имя автора',
      dataIndex: 'name',
    },
    {
      title: 'Действия',
      key: 'actions',
      render: (_, record) => (
        <>
          <Button type="link" onClick={() => navigate(`/authors/${record.id}`)}>
            Редактировать
          </Button>
          <Popconfirm
            title="Удалить автора?"
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
      <h2>Список авторов</h2>
      <Button
        type="primary"
        style={{ marginBottom: 16 }}
        onClick={() => navigate('/authors/create')}
      >
        Создать автора
      </Button>

      <Table
        rowKey="id"
        columns={columns}
        dataSource={authors}
        loading={loading}
      />
    </div>
  );
}

export default AuthorsListPage;
