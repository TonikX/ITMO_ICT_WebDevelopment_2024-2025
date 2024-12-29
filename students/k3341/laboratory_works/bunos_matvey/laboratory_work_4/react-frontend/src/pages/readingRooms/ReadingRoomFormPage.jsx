// src/pages/readingRooms/ReadingRoomFormPage.jsx
import React, { useState, useEffect, useContext } from 'react';
import { Form, Input, InputNumber, Button, notification } from 'antd';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../../context/AuthContext';

function ReadingRoomFormPage() {
  const { id } = useParams();
  const isEdit = !!id;
  const { authToken } = useContext(AuthContext);
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isEdit) {
      const fetchRoom = async () => {
        setLoading(true);
        try {
          const res = await axios.get(`http://localhost:8000/api/reading-rooms/${id}/`, {
            headers: { Authorization: `Token ${authToken}` },
          });
          form.setFieldsValue({
            name: res.data.name,
            capacity: res.data.capacity,
          });
        } catch (error) {
          notification.error({ message: 'Ошибка при загрузке зала' });
        } finally {
          setLoading(false);
        }
      };
      fetchRoom();
    }
  }, [isEdit, id]);

  const onFinish = async (values) => {
    setLoading(true);
    try {
      if (isEdit) {
        await axios.patch(`http://localhost:8000/api/reading-rooms/${id}/`, values, {
          headers: { Authorization: `Token ${authToken}` },
        });
        notification.success({ message: 'Зал обновлён' });
      } else {
        await axios.post('http://localhost:8000/api/reading-rooms/', values, {
          headers: { Authorization: `Token ${authToken}` },
        });
        notification.success({ message: 'Зал создан' });
      }
      navigate('/reading-rooms');
    } catch (error) {
      notification.error({ message: 'Ошибка при сохранении зала' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ background: '#fff', padding: 24, maxWidth: 600 }}>
      <h2>{isEdit ? 'Редактирование зала' : 'Создание зала'}</h2>
      <Form form={form} layout="vertical" onFinish={onFinish} disabled={loading}>
        <Form.Item
          label="Название зала"
          name="name"
          rules={[{ required: true, message: 'Введите название' }]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Вместимость"
          name="capacity"
          rules={[{ required: true, message: 'Введите вместимость' }]}
        >
          <InputNumber style={{ width: '100%' }} />
        </Form.Item>

        <Button type="primary" htmlType="submit" loading={loading}>
          Сохранить
        </Button>
      </Form>
    </div>
  );
}

export default ReadingRoomFormPage;
