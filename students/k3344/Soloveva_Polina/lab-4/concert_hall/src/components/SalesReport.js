import React, { useState, useEffect } from "react";
import axios from "axios";

const SalesReport = () => {
  const [report, setReport] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const response = await axios.get("http://localhost:8000/report/", {
          headers: { Authorization: `Token ${localStorage.getItem("token")}` },
        });
        setReport(response.data);
      } catch (error) {
        console.error("Ошибка при загрузке отчета:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchReport();
  }, []);

  if (loading) return <div className="container mt-4">Загрузка отчета...</div>;

  const totalRevenue = report.reduce((acc, concert) => acc + concert.total_revenue, 0);

  return (
    <div className="container mt-4">
      <table className="table">
        <thead>
          <tr>
            <th>#</th>
            <th>Концерт</th>
            <th>Дата</th>
            <th>Продано билетов</th>
            <th>Выручка (₽)</th>
          </tr>
        </thead>
        <tbody>
          {report.map((concert, index) => (
            <tr key={concert.concert_id}>
              <td>{index + 1}</td>
              <td>{concert.concert_title}</td>
              <td>{new Date(concert.date).toLocaleDateString()}</td>
              <td>{concert.tickets_sold}</td>
              <td>{concert.total_revenue.toLocaleString()} ₽</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="mt-3">
        <strong>Общая выручка: </strong>
        {totalRevenue.toLocaleString()} ₽
      </div>
    </div>
  );
};

export default SalesReport;
