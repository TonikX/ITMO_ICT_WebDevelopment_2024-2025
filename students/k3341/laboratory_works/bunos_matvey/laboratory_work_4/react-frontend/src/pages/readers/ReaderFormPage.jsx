// src/pages/readers/ReaderFormPage.jsx
import React, { useState, useEffect, useContext } from 'react';
import { Form, Input, DatePicker, Select, Switch, Button, notification } from 'antd';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import moment from 'moment';
import { AuthContext } from '../../context/AuthContext';

function ReaderFormPage() {
  const { authToken } = useContext(AuthContext);
  const { id } = useParams(); // undefined если /readers/create
  const isEdit = !!id;
  const navigate = useNavigate();

  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  // Для списка книг (assign/unassign)
  const [allBooks, setAllBooks] = useState([]);
  const [initialAssignedBooks, setInitialAssignedBooks] = useState([]); // чтобы отследить изменения

  // Для списка залов (rooms)
  const [allRooms, setAllRooms] = useState([]);
  let chosenRoomId = null; // При редактировании сохраним исходный зал

  useEffect(() => {
    // Загрузим все книги
    axios
      .get('http://localhost:8000/api/books/', {
        headers: { Authorization: `Token ${authToken}` },
      })
      .then((res) => setAllBooks(res.data))
      .catch(() => { /* ... */ });

    // Загрузим все залы
    axios
      .get('http://localhost:8000/api/reading-rooms/', {
        headers: { Authorization: `Token ${authToken}` },
      })
      .then((res) => setAllRooms(res.data))
      .catch(() => { /* ... */ });

    if (isEdit) {
      setLoading(true);
      axios
        .get(`http://localhost:8000/api/readers/${id}/`, {
          headers: { Authorization: `Token ${authToken}` },
        })
        .then((res) => {
          const r = res.data;
          // Заполним форму
          form.setFieldsValue({
            reader_card_number: r.reader_card_number,
            full_name: r.full_name,
            date_of_birth: r.date_of_birth ? moment(r.date_of_birth) : null,
            address: r.address,
            phone_number: r.phone_number,
            education: r.education,
            academic_degree: r.academic_degree,
            is_active: r.is_active,
            current_room: r.current_room.id
          });
          console.log(r)
        })
        .catch(() => {
          notification.error({ message: 'Ошибка при загрузке читателя' });
        })
        .finally(() => setLoading(false));
    }
  }, [isEdit, id]);

  const onFinish = async (values) => {
    setLoading(true);

    // 1) Сохраним «обычные поля» PATCH /readers/:id (или POST, если создаём)
    let readerId = id;
    try {
      if (isEdit) {
        await axios.patch(
          `http://localhost:8000/api/readers/${readerId}/`,
          {
            reader_card_number: values.reader_card_number,
            full_name: values.full_name,
            date_of_birth: values.date_of_birth
              ? values.date_of_birth.format('YYYY-MM-DD')
              : null,
            address: values.address,
            phone_number: values.phone_number,
            education: values.education,
            academic_degree: values.academic_degree,
            is_active: values.is_active,
          },
          { headers: { Authorization: `Token ${authToken}` } },
        );
      } else {
        const res = await axios.post(
          'http://localhost:8000/api/readers/',
          {
            reader_card_number: values.reader_card_number,
            full_name: values.full_name,
            date_of_birth: values.date_of_birth
              ? values.date_of_birth.format('YYYY-MM-DD')
              : null,
            address: values.address,
            phone_number: values.phone_number,
            education: values.education,
            academic_degree: values.academic_degree,
            is_active: values.is_active,
          },
          { headers: { Authorization: `Token ${authToken}` } },
        );
        readerId = res.data.id;
      }
    } catch (error) {
      notification.error({ message: 'Ошибка при сохранении читателя' });
      setLoading(false);
      return;
    }

    try {
      const newRoomId = values.current_room;
      if (newRoomId) {
        await axios.post(
          `http://localhost:8000/api/readers/${readerId}/change_room/`,
          { room_id: newRoomId },
          { headers: { Authorization: `Token ${authToken}` } },
        );
      }
    } catch (error) {
      notification.error({ message: 'Ошибка при смене зала' });
      setLoading(false);
      return;
    }

    notification.success({ message: 'Читатель сохранён' });
    setLoading(false);
    navigate('/readers');
  };

  return (
    <div style={{ background: '#fff', padding: 24, maxWidth: 800 }}>
      <h2>{isEdit ? 'Редактирование читателя' : 'Создание читателя'}</h2>
      <Form form={form} layout="vertical" onFinish={onFinish} disabled={loading}>
        <Form.Item
          label="Номер читательского билета"
          name="reader_card_number"
          rules={[{ required: true, message: 'Укажите номер' }]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="ФИО"
          name="full_name"
          rules={[{ required: true, message: 'Укажите ФИО' }]}
        >
          <Input />
        </Form.Item>

        <Form.Item label="Дата рождения" name="date_of_birth">
          <DatePicker style={{ width: '100%' }} />
        </Form.Item>

        <Form.Item label="Адрес" name="address">
          <Input />
        </Form.Item>

        <Form.Item label="Номер телефона" name="phone_number">
          <Input />
        </Form.Item>

        <Form.Item label="Образование" name="education">
          <Input />
        </Form.Item>

        <Form.Item label="Ученая степень" name="academic_degree">
          <Input />
        </Form.Item>

        <Form.Item label="Текущий зал" name="current_room">
          <Select allowClear placeholder="Выберите читальный зал">
            {allRooms.map((room) => (
              <Select.Option key={room.id} value={room.id}>
                {room.name}
              </Select.Option>
            ))}
          </Select>
        </Form.Item>

        <Form.Item label="Активен" name="is_active" valuePropName="checked">
          <Switch />
        </Form.Item>

        <Button type="primary" htmlType="submit" loading={loading}>
          Сохранить
        </Button>
      </Form>
    </div>
  );
}

export default ReaderFormPage;
