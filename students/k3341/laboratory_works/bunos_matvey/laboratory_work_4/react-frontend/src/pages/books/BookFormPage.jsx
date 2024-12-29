// src/pages/books/BookFormPage.jsx
import React, { useState, useEffect, useContext } from 'react';
import { Form, Input, InputNumber, Select, Button, notification } from 'antd';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../../context/AuthContext';

function BookFormPage() {
  const { authToken } = useContext(AuthContext);
  const { id } = useParams();       // undefined, если /books/create
  const isEdit = !!id;
  const navigate = useNavigate();

  const [form] = Form.useForm();
  const [authors, setAuthors] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Загрузим всех авторов (для multiple select)
    axios
      .get('http://localhost:8000/api/authors/', {
        headers: { Authorization: `Token ${authToken}` },
      })
      .then((res) => setAuthors(res.data))
      .catch(() => { /* ... */ });

    // Если редактирование, подгружаем данные книги
    if (isEdit) {
      setLoading(true);
      axios
        .get(`http://localhost:8000/api/books/${id}/`, {
          headers: { Authorization: `Token ${authToken}` },
        })
        .then((res) => {
          const book = res.data;
          form.setFieldsValue({
            book_code: book.book_code,
            title: book.title,
            publisher: book.publisher,
            year_of_publication: book.year_of_publication,
            section: book.section,
            authors: book.authors.map(author => author.id),
          });
        })
        .catch(() => notification.error({ message: 'Ошибка при загрузке книги' }))
        .finally(() => setLoading(false));
    }
  }, [isEdit, id]);

  const onFinish = async (values) => {
    setLoading(true);
    try {
      let bookId = id;

      if (isEdit) {
        // Обновляем основные поля книги
        await axios.patch(`http://localhost:8000/api/books/${bookId}/`, {
          book_code: values.book_code,
          title: values.title,
          publisher: values.publisher,
          year_of_publication: values.year_of_publication,
          section: values.section,
          // (authors не отправляем здесь, т. к. будет отдельный запрос set_authors)
        }, {
          headers: { Authorization: `Token ${authToken}` },
        });
      } else {
        // Создаём новую книгу
        const res = await axios.post(`http://localhost:8000/api/books/`, {
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

      await axios.post(
        `http://localhost:8000/api/books/${bookId}/set_authors/`,
        { authors_ids: values.authors || [] },
        { headers: { Authorization: `Token ${authToken}` } }
      );

      console.log(values.authors)

      notification.success({ message: 'Книга сохранена' });
      navigate('/books');
    } catch (error) {
      notification.error({ message: 'Ошибка при сохранении' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ background: '#fff', padding: 24, maxWidth: 800 }}>
      <h2>{isEdit ? 'Редактирование книги' : 'Создание книги'}</h2>
      <Form
        form={form}
        layout="vertical"
        onFinish={onFinish}
        disabled={loading}
      >
        <Form.Item
          label="Шифр книги"
          name="book_code"
          rules={[{ required: true, message: 'Укажите шифр книги' }]}
        >
          <Input />
        </Form.Item>

        {/* Остальные поля */}
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

        {/* Выбор авторов (Multiple Select) */}
        <Form.Item
          label="Авторы"
          name="authors"
        >
          <Select mode="multiple" allowClear>
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
