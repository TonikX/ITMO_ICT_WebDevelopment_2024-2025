import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useToken } from '../stores/token';
import Header from '../components/header.jsx';
import '../Css/RoutePage.css';
const RoutesPage = () => {
    const [routes, setRoutes] = useState([]);
    const [form, setForm] = useState({
        number: '',
        start_point: '',
        end_point: '',
        operation_start_time: '',
        operation_end_time: '',
        interval: '',
        duration: ''
    });
    const [editRouteId, setEditRouteId] = useState(null);
    const { token } = useToken();

    useEffect(() => {
        fetchRoutes();
    }, []);

    const fetchRoutes = async () => {
        try {
            const response = await axios.get('/api/routes/', {
                headers: { Authorization: `Token ${token}` }
            });
            setRoutes(response.data);
        } catch (error) {
            console.error('Ошибка при получении маршрутов:', error.response?.data || error.message);
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm({
            ...form,
            [name]: value,
        });
    };

    const addRoute = async () => {
        try {
            const response = await axios.post('/api/routes/', form, {
                headers: { Authorization: `Token ${token}` }
            });
            if (response.status === 201) {
                fetchRoutes();
                resetForm();
            }
        } catch (error) {
            console.error('Ошибка при добавлении маршрута:', error.response?.data || error.message);
        }
    };

    const resetForm = () => {
        setForm({
            number: '',
            start_point: '',
            end_point: '',
            operation_start_time: '',
            operation_end_time: '',
            interval: '',
            duration: ''
        });
        setEditRouteId(null);
    };

    const editRoute = (route) => {
        setForm({
            number: route.number,
            start_point: route.start_point,
            end_point: route.end_point,
            operation_start_time: route.operation_start_time,
            operation_end_time: route.operation_end_time,
            interval: route.interval,
            duration: route.duration
        });
        setEditRouteId(route.id);
    };

    const updateRoute = async () => {
        try {
            const response = await axios.put(`/api/routes/${editRouteId}/`, form, {
                headers: { Authorization: `Token ${token}` }
            });
            if (response.status === 200) {
                fetchRoutes();
                resetForm();
            }
        } catch (error) {
            console.error('Ошибка при обновлении маршрута:', error.response?.data || error.message);
        }
    };

    const deleteRoute = async (id) => {
        if (window.confirm('Вы уверены, что хотите удалить этот маршрут?')) {
            try {
                await axios.delete(`/api/routes/${id}/`, {
                    headers: { Authorization: `Token ${token}` }
                });
                fetchRoutes();
            } catch (error) {
                console.error('Ошибка при удалении маршрута:', error.response?.data || error.message);
            }
        }
    };

    return (
        <div className="routes-container">
            <Header></Header>
            <h2>Список маршрутов</h2>
            <table>
                <thead>
                <tr>
                    <th>ID</th>
                    <th>Номер</th>
                    <th>Начальная точка</th>
                    <th>Конечная точка</th>
                    <th>Время начала работы</th>
                    <th>Время окончания работы</th>
                    <th>Интервал</th>
                    <th>Продолжительность</th>
                    <th>Действия</th>
                </tr>
                </thead>
                <tbody>
                {routes.map((route) => (
                    <tr key={route.id}>
                        <td>{route.id}</td>
                        <td>{route.number}</td>
                        <td>{route.start_point}</td>
                        <td>{route.end_point}</td>
                        <td>{route.operation_start_time}</td>
                        <td>{route.operation_end_time}</td>
                        <td>{route.interval}</td>
                        <td>{route.duration}</td>
                        <td>
                            <button onClick={() => editRoute(route)}>Редактировать</button>
                            <button onClick={() => deleteRoute(route.id)}>Удалить</button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>

            <h3>{editRouteId ? 'Редактировать маршрут' : 'Добавить маршрут'}</h3>
            <input
                type="text"
                name="number"
                placeholder="Номер"
                value={form.number}
                onChange={handleChange}
                required
            />
            <input
                type="text"
                name="start_point"
                placeholder="Начальная точка"
                value={form.start_point}
                onChange={handleChange}
                required
            />
            <input
                type="text"
                name="end_point"
                placeholder="Конечная точка"
                value={form.end_point}
                onChange={handleChange}
                required
            />
            <input
                type="time"
                name="operation_start_time"
                placeholder="Время начала работы"
                value={form.operation_start_time}
                onChange={handleChange}
                required
            />
            <input
                type="time"
                name="operation_end_time"
                placeholder="Время окончания работы"
                value={form.operation_end_time}
                onChange={handleChange}
                required
            />
            <input
                type="text"
                name="interval"
                placeholder="Интервал"
                value={form.interval}
                onChange={handleChange}
                required
            />
            <input
                type="text"
                name="duration"
                placeholder="Продолжительность"
                value={form.duration}
                onChange={handleChange}
                required
            />

            {editRouteId ? (
                <button onClick={updateRoute}>Обновить маршрут</button>
            ) : (
                <button onClick={addRoute}>Добавить маршрут</button>
            )}
        </div>
    );
};

export default RoutesPage;
