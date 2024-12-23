
# Проект: DOGS SHOW

## Описание

**DOGS SHOW** — это веб-приложение для управления выставками собак, владельцами, экспертами и результатами соревнований. 
Приложение включает в себя авторизацию, панели администратора, страницы для управления данными и дашборд с аналитикой.

## Основные разделы приложения

1. **Владельцы собак (Owners)**  

    - Просмотр списка владельцев.  
    - Добавление и редактирование данных о владельце.

2. **Собаки (Dogs)**  

    - Просмотр списка собак.  
    - Просмотр всех участий конкретной собаки.  
    - Добавление новой собаки и участие в выставках.  

3. **Выставки (Shows)**  

    - Просмотр списка выставок.  
    - Добавление собак к выставкам.  
    - Просмотр результатов выставок.

4. **Эксперты (Experts)**  

    - Управление экспертами.
    - Присвоение экспертов к выставкам.

5. **Дашборд (Dashboard)**  

    - Общая статистика по участникам, экспертам, выставкам.  
    - Списки предстоящих и прошедших выставок.

## Структура проекта

```plaintext
src/
├── api/             # API-запросы
├── components/      # Общие компоненты (например, Header)
├── pages/           # Страницы приложения
├── context/         # Контекст для авторизации
├── shared/          # Общие типы данных
└── App.tsx          # Основной компонент маршрутизации
```

## Важные компоненты

### 1. **AppHeader** — Шапка приложения

```tsx
import React from 'react';
import { Layout, Avatar, Dropdown, Menu, Typography } from 'antd';
import { UserOutlined, MenuOutlined } from '@ant-design/icons';
import { NavLink, useNavigate } from "react-router-dom";

const { Header } = Layout;
const { Text } = Typography;

const AppHeader: React.FC = () => {
  const navigate = useNavigate();
  const username = localStorage.getItem('username');

  if (!username) return null;

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  return (
    <Header style={{ display: 'flex', justifyContent: 'space-between' }}>
      {/* Меню */}
      <Dropdown overlay={<Menu>
        <Menu.Item key="1"><NavLink to="/owners">Владельцы</NavLink></Menu.Item>
      </Menu>}>
        <Avatar icon={<MenuOutlined />} />
      </Dropdown>

      {/* Заголовок */}
      <Text onClick={() => navigate('/')} style={{ fontSize: '28px', fontWeight: 'bold' }}>DOGS SHOW</Text>

      {/* Пользователь */}
      <Dropdown overlay={<Menu>
        <Menu.Item key="1" onClick={handleLogout}>Logout</Menu.Item>
      </Menu>}>
        <Avatar icon={<UserOutlined />} />
      </Dropdown>
    </Header>
  );
};
```

### 2. **Dashboard** — Дашборд

```tsx
import React, { useEffect, useState } from 'react';
import { Row, Col, Card, Statistic, List } from 'antd';
import { fetchDogs, fetchExperts, fetchShows } from '../api/api';

const Dashboard: React.FC = () => {
  const [dogsCount, setDogsCount] = useState(0);
  const [upcomingShows, setUpcomingShows] = useState([]);
  const [pastShows, setPastShows] = useState([]);

  useEffect(() => {
    fetchDogs().then(data => setDogsCount(data.length));
    fetchShows().then(data => {
      const now = new Date();
      setUpcomingShows(data.filter(show => new Date(show.date) > now));
      setPastShows(data.filter(show => new Date(show.date) <= now));
    });
  }, []);

  return (
    <Row gutter={16}>
      <Col span={8}><Card><Statistic title="Собаки" value={dogsCount} /></Card></Col>
      <Col span={8}><List header="Предстоящие выставки" dataSource={upcomingShows} /></Col>
      <Col span={8}><List header="Прошедшие выставки" dataSource={pastShows} /></Col>
    </Row>
  );
};
```

### 3. **DogDetail** — Детальная информация о собаке

```tsx
import React, { useEffect, useState } from 'react';
import { Table, Modal, Select, Button } from 'antd';
import { fetchParticipations, createGrade } from '../api/api';

const DogDetail: React.FC = () => {
  const [participations, setParticipations] = useState([]);
  const [selectedParticipationId, setSelectedParticipationId] = useState(null);

  useEffect(() => {
    fetchParticipations().then(data => setParticipations(data));
  }, []);

  return (
    <Table
      dataSource={participations}
      rowKey="id"
      expandable={{
        expandedRowRender: record => (
          <Table dataSource={record.grades} columns={[{ title: 'Оценка', dataIndex: 'score' }]} />
        )
      }}
    />
  );
};
```

## Маршрутизация

```tsx
import { Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import DogDetail from './pages/DogDetail';

<Routes>
  <Route path="/" element={<Dashboard />} />
  <Route path="/dogs/:id" element={<DogDetail />} />
</Routes>
```

## Авторизация

- Локальное хранилище (`localStorage`) используется для хранения токена авторизации.  
- При отсутствии токена пользователя перенаправляют на `/login`.  

## Инструкция по запуску

1. Установите зависимости:  
   ```
   npm install
   ```

2. Запустите сервер разработки:  
   ```
   npm run start
   ```

3. Откройте [http://localhost:3000](http://localhost:3000).