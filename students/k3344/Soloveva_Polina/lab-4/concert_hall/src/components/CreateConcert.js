import React, { useState, useEffect } from 'react';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios';

const CreateConcert = () => {
  const [concertDetails, setConcertDetails] = useState({
    title: '',
    performer: '',
    description: '',
    date: '',
    time: '',
    age_limit: '',
    image: null, // Добавлено для фото
  });

  const [performers, setPerformers] = useState([]);

  const token = localStorage.getItem('token');

  useEffect(() => {
    axios.get('http://localhost:8000/performers/', {
      headers: token ? { Authorization: `Token ${token}` } : {},
    })
      .then((response) => {
        setPerformers(response.data);
      })
      .catch((error) => {
        console.error('Ошибка при получении списка исполнителей', error);
      });
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setConcertDetails((prev) => ({ ...prev, [name]: value }));
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setConcertDetails((prev) => ({ ...prev, image: file }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('title', concertDetails.title);
    formData.append('performer', concertDetails.performer);
    formData.append('description', concertDetails.description);
    formData.append('date', concertDetails.date);
    formData.append('time', concertDetails.time);
    formData.append('age_limit', concertDetails.age_limit);
    if (concertDetails.image) {
      formData.append('image', concertDetails.image);
    }

    axios.post('http://localhost:8000/concerts/create/', formData, {
      headers: {
        Authorization: `Token ${token}`,
        'Content-Type': 'multipart/form-data',
      },
    })
      .then((response) => {
        console.log('Концерт создан', response.data);
      })
      .catch((error) => {
        console.error('Ошибка при создании концерта', error);
      });
  };

  return (
    <div>
      <Form onSubmit={handleSubmit} className="mt-3">
        <Form.Group>
          <Form.Label>Название концерта</Form.Label>
          <Form.Control
            type="text"
            name="title"
            value={concertDetails.title}
            onChange={handleChange}
          />
        </Form.Group>

        {/* Выпадающий список для исполнителей */}
        <Form.Group>
          <Form.Label className="mt-3">Исполнитель</Form.Label>
          <Form.Control
            as="select"
            name="performer"
            value={concertDetails.performer}
            onChange={handleChange}
          >
            <option value="">Выберите исполнителя</option>
            {performers.map((performer) => (
              <option key={performer.id} value={performer.id}>
                {performer.name}
              </option>
            ))}
          </Form.Control>
        </Form.Group>

        <Form.Group>
          <Form.Label className="mt-3">Описание</Form.Label>
          <Form.Control
            type="text"
            name="description"
            value={concertDetails.description}
            onChange={handleChange}
          />
        </Form.Group>
        <Form.Group>
          <Form.Label className="mt-3">Дата</Form.Label>
          <Form.Control
            type="date"
            name="date"
            value={concertDetails.date}
            onChange={handleChange}
          />
        </Form.Group>
        <Form.Group className="mt-3">
          <Form.Label>Время</Form.Label>
          <Form.Control
            type="time"
            name="time"
            value={concertDetails.time}
            onChange={handleChange}
          />
        </Form.Group>
        <Form.Group className="mt-3">
          <Form.Label>Возрастное ограничение</Form.Label>
          <Form.Control
            type="text"
            name="age_limit"
            value={concertDetails.age_limit}
            onChange={handleChange}
          />
        </Form.Group>

        {/* Поле для загрузки фото */}
        <Form.Group className="mt-3">
          <Form.Label>Фото</Form.Label>
          <Form.Control
            type="file"
            onChange={handleFileChange}
          />
        </Form.Group>

      <Button type="submit" className="mt-3">Создать концерт</Button>
      </Form>
    </div>
  );
};

export default CreateConcert;
