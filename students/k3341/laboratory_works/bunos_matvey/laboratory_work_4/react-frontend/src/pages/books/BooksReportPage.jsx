// src/pages/books/BooksReportPage.jsx
import React, { useEffect, useState, useContext } from 'react';
import { Typography, Spin, notification } from 'antd';
import { Pie } from '@ant-design/plots';
import axios from 'axios';
import { AuthContext } from '../../context/AuthContext';

const { Title } = Typography;

function BooksReportPage() {
  const { authToken } = useContext(AuthContext);
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchReport = async () => {
    setLoading(true);
    try {
      const res = await axios.get('http://localhost:8000/api/books/books_publication_report/', {
        headers: { Authorization: `Token ${authToken}` },
      });
      setReportData(res.data);
    } catch (error) {
      notification.error({ message: 'Ошибка при загрузке отчёта' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReport();
  }, []);

  if (loading) {
    return <Spin style={{ margin: '50px' }} />;
  }

  if (!reportData) {
    return null; 
  }

  const chartData = reportData.by_year.map((item) => ({
    type: String(item.year),
    value: item.count,
  }));

  const config = {
    appendPadding: 10,
    data: chartData,
    angleField: 'value',
    colorField: 'type',
    radius: 0.8,
    label: {
      type: 'inner',
      offset: '-30%',
      content: '{name} ({percentage})',
      style: {
        fontSize: 14,
        textAlign: 'center',
      },
    },
    interactions: [{ type: 'element-active' }],
  };

  return (
    <div style={{ background: '#fff', padding: 24 }}>
      <Title level={3}>Отчёт по годам издания книг</Title>
      <p>Всего книг: {reportData.total_books}</p>
      <p>Последний год публикации: {reportData.last_publication_year || '—'}</p>

      <Pie {...config} />
    </div>
  );
}

export default BooksReportPage;
