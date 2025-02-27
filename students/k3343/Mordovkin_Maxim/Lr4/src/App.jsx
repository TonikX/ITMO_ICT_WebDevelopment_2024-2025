// src/App.jsx
import React from 'react';
import { Provider } from 'react-redux';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { MantineProvider } from '@mantine/core';

import { store } from './store/store';
import AppLayout from './components/Layout/AppLayout';

import LoginForm from './components/Auth/LoginForm';
import RegisterForm from './components/Auth/RegisterForm';
import PrivateRoute from './components/Auth/PrivateRoute';

import Home from './components/Home/Home';
import FlightList from './components/Flights/FlightList';
import FlightForm from './components/Flights/FlightForm';
import FlightDetails from './components/Flights/FlightDetails'; // Добавлено
import Reports from './components/Reports/Reports';
import Profile from './components/Profile/Profile';
import CrewRequests from './components/Crew/CrewRequests';

import CarrierList from './components/Carriers/CarrierList'; // Добавлено
import CarrierForm from './components/Carriers/CarrierForm'; // Добавлено

import AircraftMaintenanceList from './components/AircraftMaintenance/AircraftMaintenanceList'; // Добавлено
import AircraftMaintenanceForm from './components/AircraftMaintenance/AircraftMaintenanceForm'; // Добавлено

function App() {
    return (
        <Provider store={store}>
            <MantineProvider>
                <BrowserRouter>
                    <Routes>

                        {/* Публичные маршруты (доступны без токена) */}
                        <Route path="/login" element={<LoginForm />} />
                        <Route path="/register" element={<RegisterForm />} />

                        {/* Защищённые маршруты (требуется токен) */}
                        <Route
                            path="/"
                            element={
                                <PrivateRoute>
                                    <AppLayout />
                                </PrivateRoute>
                            }
                        >
                            {/* При заходе на "/" рендерится Home */}
                            <Route index element={<Home />} />

                            {/* Список рейсов */}
                            <Route path="flights" element={<FlightList />} />

                            {/* Создание нового рейса (для ADMIN) */}
                            <Route path="flights/new" element={<FlightForm />} />

                            {/* Просмотр деталей рейса */}
                            <Route path="flights/:flightId" element={<FlightDetails />} />

                            {/* Редактирование рейса */}
                            <Route path="flights/:flightId/edit" element={<FlightForm />} />

                            {/* Управление экипажем */}
                            <Route path="flights/:flightId/crew" element={<FlightDetails />} /> {/* Можно создать отдельный компонент, если требуется */}

                            {/* Список авиаперевозчиков */}
                            <Route path="carriers" element={<CarrierList />} />

                            {/* Создание нового авиаперевозчика */}
                            <Route path="carriers/new" element={<CarrierForm />} />

                            {/* Редактирование авиаперевозчика */}
                            <Route path="carriers/:carrierId/edit" element={<CarrierForm />} />

                            {/* Список технических состояний самолётов */}
                            <Route path="aircraft-maintenances" element={<AircraftMaintenanceList />} />

                            {/* Создание нового технического состояния */}
                            <Route path="maintenance/new" element={<AircraftMaintenanceForm />} />

                            {/* Редактирование технического состояния */}
                            <Route path="maintenance/:maintenanceId/edit" element={<AircraftMaintenanceForm />} />

                            {/* Отчёты */}
                            <Route path="reports" element={<Reports />} />

                            {/* Профиль */}
                            <Route path="profile" element={<Profile />} />

                            {/* Страница заявок экипажа (для ADMIN) */}
                            <Route path="crew-requests" element={<CrewRequests />} />

                            {/* Любой неизвестный путь → на главную */}
                            <Route path="*" element={<Navigate to="/" replace />} />
                        </Route>
                    </Routes>
                </BrowserRouter>
            </MantineProvider>
        </Provider>
    );
}

export default App;
