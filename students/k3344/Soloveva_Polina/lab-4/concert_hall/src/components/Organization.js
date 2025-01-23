import React, { useState, useEffect } from "react";
import { Button, Card, Modal, Form } from "react-bootstrap";
import axios from "axios";

const Organization = () => {
  const [concerts, setConcerts] = useState([]);
  const [editConcert, setEditConcert] = useState(null);
  const [performers, setPerformers] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const token = localStorage.getItem("token");

  useEffect(() => {
    fetchConcerts();
    fetchPerformers();
  }, []);

  const fetchConcerts = () => {
    axios
      .get("http://localhost:8000/concerts/", {
        headers: { Authorization: `Token ${token}` },
      })
      .then((response) => {
        const filteredConcerts = response.data.filter(
          (concert) => concert.status === "created"
        );
        setConcerts(filteredConcerts);
      })
      .catch((error) => console.error("Ошибка загрузки концертов:", error));
  };

  const fetchPerformers = () => {
    axios
      .get("http://localhost:8000/performers/", {
        headers: { Authorization: `Token ${token}` },
      })
      .then((response) => {
        setPerformers(response.data);
      })
      .catch((error) => console.error("Ошибка при получении списка исполнителей", error));
  };

  const handleTakeInWork = (concertId) => {
    axios
      .post(`http://localhost:8000/organizer/assign/${concertId}/`, {}, {
        headers: { Authorization: `Token ${token}` },
      })
      .then(() => {
        setConcerts((prev) => prev.filter((concert) => concert.id !== concertId));
        alert("Концерт успешно взят в работу!");
      })
      .catch((error) => alert("Ошибка при назначении концерта"));
  };

  const handleDeleteConcert = (concertId) => {
    axios
      .delete(`http://localhost:8000/concerts/${concertId}/delete/`, {
        headers: { Authorization: `Token ${token}` },
      })
      .then(() => {
        setConcerts((prev) => prev.filter((concert) => concert.id !== concertId));
        alert("Концерт удален");
      })
      .catch((error) => alert("Ошибка при удалении концерта"));
  };

  const handleEditConcert = (concert) => {
    setEditConcert(concert);
    setShowModal(true);
  };

  const handleSaveConcert = () => {
    const formData = new FormData();
    formData.append("title", editConcert.title);
    formData.append("description", editConcert.description);
    formData.append("performer", editConcert.performer);
    formData.append("image", editConcert.image);

    axios
      .patch(`http://localhost:8000/concerts/${editConcert.id}/update/`, formData, {
        headers: {
          Authorization: `Token ${token}`,
          "Content-Type": "multipart/form-data",  // Важный момент
        },
      })
      .then(() => {
        fetchConcerts();
        setShowModal(false);
      })
      .catch((error) => alert("Ошибка при обновлении концерта"));
  };

  const handleCreateConcert = (newConcert) => {
    const formData = new FormData();
    formData.append("title", newConcert.title);
    formData.append("description", newConcert.description);
    formData.append("performer", newConcert.performer);
    formData.append("image", newConcert.image);

    axios
      .post("http://localhost:8000/concerts/create/", formData, {
        headers: {
          Authorization: `Token ${token}`,
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        setConcerts((prevConcerts) => [...prevConcerts, response.data]);
        alert("Концерт успешно создан!");
      })
      .catch((error) => alert("Ошибка при создании концерта"));
  };

  return (
    <div>
      {concerts.length === 0 ? <p className="mt-3">Нет доступных концертов</p> : null}
      {concerts.map((concert) => (
        <Card key={concert.id} className="mt-3">
          <Card.Body >
            <Card.Title>{concert.title}</Card.Title>
            <Card.Text>{concert.description}</Card.Text>
            <Button variant="success" onClick={() => handleTakeInWork(concert.id)}>
              Взять в работу
            </Button>{" "}
            <Button variant="warning" onClick={() => handleEditConcert(concert)}>
              Редактировать
            </Button>{" "}
            <Button variant="danger" onClick={() => handleDeleteConcert(concert.id)}>
              Удалить
            </Button>
          </Card.Body>
        </Card>
      ))}

      {/* Модальное окно редактирования концерта */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Редактировать концерт</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Название</Form.Label>
              <Form.Control
                type="text"
                value={editConcert?.title || ""}
                onChange={(e) => setEditConcert({ ...editConcert, title: e.target.value })}
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Описание</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                value={editConcert?.description || ""}
                onChange={(e) => setEditConcert({ ...editConcert, description: e.target.value })}
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Исполнитель</Form.Label>
              <Form.Control
                as="select"
                value={editConcert?.performer || ""}
                onChange={(e) => setEditConcert({ ...editConcert, performer: e.target.value })}
              >
                <option value="">Выберите исполнителя</option>
                {performers.map((performer) => (
                  <option key={performer.id} value={performer.id}>
                    {performer.name}
                  </option>
                ))}
              </Form.Control>
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Фото</Form.Label>
              <Form.Control
                type="file"
                onChange={(e) => setEditConcert({ ...editConcert, image: e.target.files[0] })}
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Отмена
          </Button>
          <Button variant="primary" onClick={handleSaveConcert}>
            Сохранить
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default Organization;
