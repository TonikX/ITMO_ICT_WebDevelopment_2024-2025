import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useToken } from '../stores/token';
import Header from '../components/header.jsx';
import '../Css/WorkShiftsPage.css';

const WorkShiftsPage = () => {
    const [workShifts, setWorkShifts] = useState([]);
    const [drivers, setDrivers] = useState([]);
    const [buses, setBuses] = useState([]);
    const [routes, setRoutes] = useState([]);
    const [form, setForm] = useState({
        date: '',
        shift_start_time: '',
        shift_end_time: '',
        status: 'Worked',
        reason: '',
        driver: 0,
        bus: 0,
        route: 0
    });
    const [editShiftId, setEditShiftId] = useState(null);
    const { token } = useToken();

    useEffect(() => {
        fetchWorkShifts();
        fetchDrivers();
        fetchBuses();
        fetchRoutes();
    }, []);

    const fetchWorkShifts = async () => {
        try {
            const response = await axios.get('/api/work-shifts/', {
                headers: { Authorization: `Token ${token}` }
            });
            setWorkShifts(response.data);
        } catch (error) {
            console.error('Ошибка при получении рабочих смен:', error.response?.data || error.message);
        }
    };

    const fetchDrivers = async () => {
        try {
            const response = await axios.get('/api/drivers/', {
                headers: { Authorization: `Token ${token}` }
            });
            setDrivers(response.data);
        } catch (error) {
            console.error('Ошибка при получении водителей:', error.response?.data || error.message);
        }
    };

    const fetchBuses = async () => {
        try {
            const response = await axios.get('/api/buses/', {
                headers: { Authorization: `Token ${token}` }
            });
            setBuses(response.data);
        } catch (error) {
            console.error('Ошибка при получении автобусов:', error.response?.data || error.message);
        }
    };

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

    const addWorkShift = async () => {
        try {
            const response = await axios.post('/api/work-shifts/', form, {
                headers: { Authorization: `Token ${token}` }
            });
            if (response.status === 201) {
                fetchWorkShifts();
                resetForm();
            }
        } catch (error) {
            console.error('Ошибка при добавлении рабочей смены:', error.response?.data || error.message);
        }
    };

    const resetForm = () => {
        setForm({
            date: '',
            shift_start_time: '',
            shift_end_time: '',
            status: 'Worked',
            reason: '',
            driver: 0,
            bus: 0,
            route: 0
        });
        setEditShiftId(null);
    };

    const editWorkShift = (shift) => {
        setForm(shift);
        setEditShiftId(shift.id);
    };

    const updateWorkShift = async () => {
        try {
            const response = await axios.put(`/api/work-shifts/${editShiftId}/`, form, {
                headers: { Authorization: `Token ${token}` }
            });
            if (response.status === 200) {
                fetchWorkShifts();
                resetForm();
            }
        } catch (error) {
            console.error('Ошибка при обновлении рабочей смены:', error.response?.data || error.message);
        }
    };

    const deleteWorkShift = async (id) => {
        if (window.confirm('Вы уверены, что хотите удалить эту рабочую смену?')) {
            try {
                await axios.delete(`/api/work-shifts/${id}/`, {
                    headers: { Authorization: `Token ${token}` }
                });
                fetchWorkShifts();
            } catch (error) {
                console.error('Ошибка при удалении рабочей смены:', error.response?.data || error.message);
            }
        }
    };

    return (
        <div className="work-shifts-container">
            <Header />
            <h2>Список рабочих смен</h2>
            <table>
                <thead>
                <tr>
                    <th>ID</th>
                    <th>Дата</th>
                    <th>Время начала</th>
                    <th>Время окончания</th>
                    <th>Статус</th>
                    <th>Причина</th>
                    <th>Водитель</th>
                    <th>Автобус</th>
                    <th>Маршрут</th>
                    <th>Действия</th>
                </tr>
                </thead>
                <tbody>
                {workShifts.map((shift) => (
                    <tr key={shift.id}>
                        <td>{shift.id}</td>
                        <td>{shift.date}</td>
                        <td>{shift.shift_start_time}</td>
                        <td>{shift.shift_end_time}</td>
                        <td>{shift.status}</td>
                        <td>{shift.reason}</td>
                        <td>{shift.driver}</td>
                        <td>{shift.bus}</td>
                        <td>{shift.route}</td>
                        <td>
                            <button onClick={() => editWorkShift(shift)}>Редактировать</button>
                            <button onClick={() => deleteWorkShift(shift.id)}>Удалить</button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>

            <h3>{editShiftId ? 'Редактировать рабочую смену' : 'Добавить рабочую смену'}</h3>

            <input
                type="date"
                name="date"
                placeholder="Дата"
                value={form.date}
                onChange={handleChange}
                required
            />
            <input
                type="time"
                name="shift_start_time"
                placeholder="Время начала"
                value={form.shift_start_time}
                onChange={handleChange}
                required
            />
            <input
                type="time"
                name="shift_end_time"
                placeholder="Время окончания"
                value={form.shift_end_time}
                onChange={handleChange}
                required
            />
            <input
                type="text"
                name="status"
                placeholder="Статус"
                value={form.status}
                onChange={handleChange}
                required
            />
            <input
                type="text"
                name="reason"
                placeholder="Причина"
                value={form.reason}
                onChange={handleChange}
            />

            <h4>Выберите водителя:</h4>
            <select name="driver" value={form.driver} onChange={handleChange} required>
                <option value="">Выберите водителя</option>
                {drivers.map(driver => (
                    <option key={driver.id} value={driver.id}>
                        {driver.passport_data} - {driver.driver_class}
                    </option>
                ))}
            </select>

            <h4>Выберите автобус:</h4>
            <select name="bus" value={form.bus} onChange={handleChange} required>
                <option value="">Выберите автобус</option>
                {buses.map(bus => (
                    <option key={bus.id} value={bus.id}>
                        {bus.registration_number}
                    </option>
                ))}
            </select>

            <h4>Выберите маршрут:</h4>
            <select name="route" value={form.route} onChange={handleChange} required>
                <option value="">Выберите маршрут</option>
                {routes.map(route => (
                    <option key={route.id} value={route.id}>
                        {route.number} - {route.start_point} до {route.end_point}
                    </option>
                ))}
            </select>

            {editShiftId ? (
                <button onClick={updateWorkShift}>Обновить рабочую смену</button>
            ) : (
                <button onClick={addWorkShift}>Добавить рабочую смену</button>
            )}
        </div>
    );
};

export default WorkShiftsPage;
