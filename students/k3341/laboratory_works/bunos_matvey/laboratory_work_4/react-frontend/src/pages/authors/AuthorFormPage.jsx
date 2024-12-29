// src/pages/authors/AuthorFormPage.jsx
import React, { useState, useEffect, useContext } from 'react';
import { Form, Input, Button, notification } from 'antd';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../../context/AuthContext';

function AuthorFormPage() {
  const { id } = useParams(); // undefined, если "/authors/create"
  const isEdit = !!id;
  const { authToken } = useContext(AuthContext);
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isEdit) {
      // Загрузить данные автора
      const fetchAuthor = async () => {
        setLoading(true);
        try {
          const res = await axios.get(`http://localhost:8000/api/authors/${id}/`, {
            headers: { Authorization: `Token ${authToken}` },
          });
          form.setFieldsValue({ name: res.data.name });
        } catch (error) {
          notification.error({ message: 'Ошибка при загрузке автора' });
        } finally {
          setLoading(false);
        }
      };
      fetchAuthor();
    }
  }, [isEdit, id]);

  const onFinish = async (values) => {
    setLoading(true);
    try {
      if (isEdit) {
        await axios.patch(`http://localhost:8000/api/authors/${id}/`, values, {
          headers: { Authorization: `Token ${authToken}` },
        });
        notification.success({ message: 'Автор обновлён' });
      } else {
        await axios.post(`http://localhost:8000/api/authors/`, values, {
          headers: { Authorization: `Token ${authToken}` },
        });
        notification.success({ message: 'Автор создан' });
      }
      navigate('/authors');
    } catch (error) {
      notification.error({ message: 'Ошибка при сохранении автора' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ background: '#fff', padding: 24, maxWidth: 600 }}>
      <h2>{isEdit ? 'Редактирование автора' : 'Создание автора'}</h2>
      <Form form={form} layout="vertical" onFinish={onFinish} disabled={loading}>
        <Form.Item
          label="Имя автора"
          name="name"
          rules={[{ required: true, message: 'Введите имя' }]}
        >
          <Input />
        </Form.Item>

        <Button type="primary" htmlType="submit" loading={loading}>
          Сохранить
        </Button>
      </Form>
    </div>
  );
}

export default AuthorFormPage;
