import React, { useState } from 'react';
import { Tab, Tabs } from 'react-bootstrap';
import CreateConcert from '../components/CreateConcert';
import Organization from '../components/Organization';
import MyConcerts from '../components/MyConcerts';
import OrderConfirmation from '../components/OrderConfirmation';
import SalesReport from '../components/SalesReport';

const AdminDashboard = () => {
  const [key, setKey] = useState('createConcert');

  return (
    <div>
      <h1>Админ Панель</h1>
      <Tabs activeKey={key} onSelect={(k) => setKey(k)} id="admin-tabs">
        <Tab eventKey="createConcert" title="Создать концерт">
          <CreateConcert />
        </Tab>
        <Tab eventKey="organization" title="Организация">
          <Organization />
        </Tab>
        <Tab eventKey="myConcerts" title="Мои концерты">
          <MyConcerts />
        </Tab>
        <Tab eventKey="orderConfirmation" title="Подтверждение заказов">
          <OrderConfirmation />
        </Tab>
        <Tab eventKey="salesReport" title="Отчет по продажам">
          <SalesReport />
        </Tab>
      </Tabs>
    </div>
  );
};

export default AdminDashboard;
