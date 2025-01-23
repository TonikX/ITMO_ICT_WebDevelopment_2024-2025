import React, { useState, useEffect } from 'react';
import { Button, Accordion, ListGroup, Form, Modal } from 'react-bootstrap';
import axios from 'axios';

const MyConcerts = () => {
  const [concerts, setConcerts] = useState([]);
  const [selectedConcert, setSelectedConcert] = useState(null);
  const [ticketName, setTicketName] = useState('');
  const [ticketPrice, setTicketPrice] = useState('');
  const [ticketCount, setTicketCount] = useState(1);
  const [showModal, setShowModal] = useState(false);
  const [currentConcertId, setCurrentConcertId] = useState(null);
  const token = localStorage.getItem('token');

  useEffect(() => {
    axios.get('http://localhost:8000/organizer/concerts/', {
      headers: { Authorization: `Token ${token}` },
    })
      .then((response) => setConcerts(response.data))
      .catch((error) => console.error('Ошибка загрузки концертов:', error));
  }, [token]);

  const handleAddTickets = () => {
    if (!ticketName || !ticketPrice || ticketCount <= 0) {
      alert("Пожалуйста, укажите название, цену и количество билетов больше 0.");
      return;
    }


    axios.post(`http://localhost:8000/concerts/tickets/`, {
      concert: currentConcertId,
      name: ticketName,
      price: ticketPrice,
      total_quantity: ticketCount
    }, {
      headers: { Authorization: `Token ${token}` }
    })
    .then(() => {
      alert('Билеты добавлены');
      setTicketName('');
      setTicketPrice('');
      setTicketCount(1);
      setShowModal(false);

      axios.get(`http://localhost:8000/concerts/${currentConcertId}/`, {
        headers: { Authorization: `Token ${token}` },
      })
      .then((response) => {
        setConcerts((prevConcerts) => prevConcerts.map((concert) => {
          if (concert.id === currentConcertId) {
            return { ...concert, tickets: response.data.tickets };
          }
          return concert;
        }));

      })
      .catch((error) => alert('Ошибка обновления билетов: ' + error.response.data));
    })
    .catch((error) => alert('Ошибка добавления билетов: ' + error.response.data));
  };

  const handleConcertClick = (concertId) => {
    if (selectedConcert === concertId) {
      setSelectedConcert(null);
      setTicketName('');
      setTicketPrice('');
      setTicketCount(1);
    } else {
      setSelectedConcert(concertId);
    }
  };

  const handleSendStatusUpdate = (concertId) => {
    axios.post(`http://localhost:8000/concerts/${concertId}/status/`, {}, {
      headers: { Authorization: `Token ${token}` }
    })
    .then(() => {
      alert('Статус концерта изменен на "Подготовлен"');
      setConcerts((prevConcerts) =>
        prevConcerts.map((concert) =>
          concert.id === concertId ? { ...concert, status: 'Подготовлен' } : concert
        )
      );
    })
    .catch((error) => alert('Ошибка при изменении статуса: ' + error.response.data));
  };

  return (
    <div>
      {concerts.length === 0 && <p className="mt-3">Нет доступных концертов</p>}
      <Accordion className="mt-3">
        {concerts.map((concert) => (
          <Accordion.Item key={concert.id} eventKey={concert.id.toString()}>
            <Accordion.Header>{concert.title}</Accordion.Header>
            <Accordion.Body>
              <p>Дата: {concert.date}, Время: {concert.time}</p>

              {/* Отображение билетов для концерта */}
              <ListGroup className="mt-2">
                {concert.tickets && concert.tickets.map((ticket) => (
                  <ListGroup.Item key={ticket.id}>
                    {ticket.name} - Цена: {ticket.price} - Количество: {ticket.total_quantity}
                  </ListGroup.Item>
                ))}
              </ListGroup>

                <div className="d-flex gap-2 mt-3">
                  <div className="d-flex gap-2">
                    <Button onClick={() => {
                      setCurrentConcertId(concert.id);
                      setShowModal(true);
                    }}>Добавить билеты</Button>
                    <Button onClick={() => handleSendStatusUpdate(concert.id)}>Отправить</Button>
                  </div>
                </div>

            </Accordion.Body>
          </Accordion.Item>
        ))}
      </Accordion>

      {/* Модальное окно для добавления билетов */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
      <Modal.Header closeButton>
          <Modal.Title>Добавить билеты</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group>
              <Form.Label>Название билета</Form.Label>
              <Form.Control
                type="text"
                placeholder="Введите название билета"
                value={ticketName}
                onChange={(e) => setTicketName(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mt-2">
              <Form.Label>Цена билета</Form.Label>
              <Form.Control
                type="number"
                placeholder="Введите цену билета"
                value={ticketPrice}
                onChange={(e) => setTicketPrice(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mt-2">
              <Form.Label>Количество билетов</Form.Label>
              <Form.Control
                type="number"
                placeholder="Введите количество билетов"
                value={ticketCount}
                onChange={(e) => setTicketCount(e.target.value)}
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Закрыть
          </Button>
          <Button variant="primary" onClick={handleAddTickets}>
            Добавить
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default MyConcerts;
