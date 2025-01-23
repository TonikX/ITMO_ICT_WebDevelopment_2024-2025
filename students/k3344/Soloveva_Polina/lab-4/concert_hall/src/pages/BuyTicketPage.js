import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

const BuyTicketPage = () => {
  const { ticketId } = useParams();
  const [quantity, setQuantity] = useState(1);
  const [ticket, setTicket] = useState(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      alert("Необходима авторизация");
      navigate("/login");
      return;
    }

    const fetchTicket = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/tickets/${ticketId}/`);
        setTicket(response.data);
      } catch (error) {
        console.error("Ошибка при загрузке данных билета:", error);
      }
    };

    fetchTicket();
  }, [ticketId, navigate]);

  if (!ticket) {
    return <div className="container mt-4">Загрузка...</div>;
  }

  const handleIncrease = () => {
    if (quantity < Math.min(10, ticket.available_quantity)) {
      setQuantity((prevQuantity) => prevQuantity + 1);
    }
  };

  const handleDecrease = () => {
    if (quantity > 1) {
      setQuantity((prevQuantity) => prevQuantity - 1);
    }
  };

  const handlePurchase = async () => {
    setLoading(true);
    try {
      await axios.post(
        `http://localhost:8000/orders/${ticketId}/`,
        { ticket: ticketId, quantity },
        { headers: { Authorization: `Token ${localStorage.getItem("token")}` } }
      );
      setSuccess(true);
      alert("Заказ успешно оформлен!");
      navigate(`/concerts/${ticket.concert}/`);
    } catch (error) {
      console.error("Ошибка при оформлении заказа:", error);
      alert("Не удалось оформить заказ.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-4">
      <h2>Покупка билета</h2>
      <p><strong>Билет:</strong> {ticket.name}</p>
      <p><strong>Цена за билет:</strong> {ticket.price} ₽</p>
      <p><strong>Осталось билетов:</strong> {ticket.available_quantity}</p>

      {ticket.available_quantity > 0 ? (
        <>
          <div className="d-flex align-items-center">
            <button className="btn btn-outline-secondary" onClick={handleDecrease}>−</button>
            <span className="mx-3">{quantity}</span>
            <button className="btn btn-outline-secondary" onClick={handleIncrease}>+</button>
          </div>

          <h4 className="mt-3">Общая стоимость: {ticket.price * quantity} ₽</h4>

          <button
            className="btn btn-primary mt-3"
            onClick={handlePurchase}
            disabled={loading || success || ticket.available_quantity === 0}
          >
            {loading ? "Оформление..." : `Купить ${quantity} билет(ов) за ${ticket.price * quantity} ₽`}
          </button>
        </>
      ) : (
        <p className="text-danger mt-3">Билеты распроданы</p>
      )}
    </div>
  );
};

export default BuyTicketPage;
