import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const statusColors = {
  confirmed: "bg-success",
  pending: "bg-warning",
  returned: "bg-danger"
};

const statusLabels = {
  confirmed: "Подтверждено",
  pending: "В ожидании",
  returned: "Возврат"
};

const UserProfile = () => {
  const [orders, setOrders] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await axios.get("http://localhost:8000/orders/my/", {
          headers: { Authorization: `Token ${localStorage.getItem("token")}` },
        });
        setOrders(response.data);
      } catch (error) {
        console.error("Ошибка при загрузке заказов:", error);
      }
    };

    fetchOrders();
  }, []);

  return (
    <div className="container mt-4">
      <h2>Мои билеты</h2>
      {orders.length > 0 ? (
        <ul className="list-group mt-2">
          {orders.map(order => (
            <li
              key={order.id}
              className="list-group-item d-flex justify-content-between align-items-center"
              onClick={() => navigate(`/concerts/${order.concert.id}`)}
              style={{ cursor: "pointer" }}
            >
              <div>
                <p className="mb-1"><strong>{order.concert.title}</strong> - {order.ticket.name}</p>
                <p className="mb-1">Количество: {order.quantity} ({order.ticket.price * order.quantity} ₽)</p>
              </div>
              <span className={`badge ${statusColors[order.status]} text-white p-2`}>
                {statusLabels[order.status]}
              </span>
            </li>
          ))}
        </ul>
      ) : (
        <p>У вас пока нет заказов.</p>
      )}
    </div>
  );
};

export default UserProfile;
