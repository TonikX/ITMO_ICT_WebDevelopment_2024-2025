import React, { useState, useEffect } from 'react';
import { Button, ListGroup, Accordion, Badge, Row, Col } from 'react-bootstrap';
import axios from 'axios';

const OrderConfirmation = () => {
  const [pendingOrders, setPendingOrders] = useState([]);
  const [historyOrders, setHistoryOrders] = useState([]);

  const fetchOrders = () => {
    const token = localStorage.getItem("token");

    axios.get('http://localhost:8000/orders/', {
      headers: { Authorization: `Token ${token}` }
    })
      .then((response) => {
        const pending = response.data.filter(order => order.status === "pending");
        const history = response.data.filter(order => order.status === "confirmed" || order.status === "returned");

        setPendingOrders(pending);
        setHistoryOrders(history);
      })
      .catch((error) => console.error("Ошибка загрузки заказов", error));
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const handleConfirmOrder = (orderId) => {
    const token = localStorage.getItem("token");

    axios.post(`http://localhost:8000/orders/${orderId}/confirm/`, {}, {
      headers: { Authorization: `Token ${token}` }
    })
      .then(() => {
        fetchOrders();  // Загружаем обновленные заказы
      })
      .catch((error) => console.error("Ошибка подтверждения заказа", error));
  };

  const handleReturnOrder = (orderId) => {
    const token = localStorage.getItem("token");

    axios.post(`http://localhost:8000/orders/${orderId}/return/`, {}, {
      headers: { Authorization: `Token ${token}` }
    })
      .then(() => {
        fetchOrders();
      })
      .catch((error) => console.error("Ошибка возврата заказа", error));
  };

  return (
    <div>
      <ListGroup className="mt-3">
        {pendingOrders.length === 0 ? <p className="mt-3">Нет заказов для подтверждения</p> : null}
        {pendingOrders.map((order) => (
          <ListGroup.Item key={order.id} className="order-item">
            <Row>
              <Col md={8}>
                <p><strong>{order.concert.title}</strong></p>
                <p>{order.user.username} - {order.user.email}</p>
                <p>{order.quantity} билетов - {order.total_price} ₽</p>
              </Col>
              <Col md={4} className="text-end d-flex flex-column align-items-end justify-content-center">
                <Button variant="success" onClick={() => handleConfirmOrder(order.id)} style={{ width: "100%" }} className="mb-2">
                  Подтвердить
                </Button>
                <Button variant="danger" onClick={() => handleReturnOrder(order.id)} style={{ width: "100%" }}>
                  Возврат
                </Button>
              </Col>
            </Row>
          </ListGroup.Item>
        ))}
      </ListGroup>

      <h2 className="mt-4">История заказов</h2>
      <Accordion>
        <Accordion.Item eventKey="0">
          <Accordion.Header>Показать историю заказов</Accordion.Header>
          <Accordion.Body>
            <ListGroup>
              {historyOrders.length === 0 ? <p>История заказов пуста</p> : null}
              {historyOrders.map((order) => (
                <ListGroup.Item key={order.id} className="order-item">
                  <Row>
                    <Col md={8}>
                      <p><strong>{order.concert.title}</strong></p>
                      <p>{order.user.username} - {order.user.email}</p>
                      <p>{order.quantity} билетов - {order.total_price} ₽</p>
                    </Col>
                    <Col md={4} className="text-end d-flex align-items-center justify-content-end">
                      <Badge className="orders-bd" bg={order.status === "confirmed" ? "success" : "danger"}>
                        {order.status === "confirmed" ? "Подтвержден" : "Возвращен"}
                      </Badge>
                    </Col>
                  </Row>
                </ListGroup.Item>
              ))}
            </ListGroup>
          </Accordion.Body>
        </Accordion.Item>
      </Accordion>
    </div>
  );
};

export default OrderConfirmation;
