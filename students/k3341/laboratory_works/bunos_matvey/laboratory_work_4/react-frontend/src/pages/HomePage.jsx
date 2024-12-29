// src/pages/HomePage.jsx
import React, { useContext } from 'react';
import { Typography } from 'antd';
import { AuthContext } from '../context/AuthContext';

const { Title } = Typography;

function HomePage() {
  const { authToken } = useContext(AuthContext);

  return (
    <div style={{ padding: 24, background: '#fff', minHeight: 'calc(100vh - 200px)' }}>
      <Title level={2}>Добро пожаловать в Library!</Title>
      {authToken ? (
        <p>Вы уже авторизованы, изучайте нашу библиотеку!</p>
      ) : (
        <p>Пожалуйста, войдите или зарегистрируйтесь, чтобы продолжить.</p>
      )}
    </div>
  );
}

export default HomePage;
