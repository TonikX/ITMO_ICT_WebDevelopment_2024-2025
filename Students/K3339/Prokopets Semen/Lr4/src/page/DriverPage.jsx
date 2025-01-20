import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useToken } from '../stores/token';
import Header from '../components/header.jsx';
import '../Css/DriverPage.css';

const DriversPage = () => {
    const [drivers, setDrivers] = useState([]);
    const [form, setForm] = useState({
        passport_data: '',
        driver_class: '',
        work_experience: 0,
        salary: '',
        date_of_birth: ''
    });
    const [editDriverId, setEditDriverId] = useState(null);
    const { token } = useToken();

    useEffect(() => {
        fetchDrivers();
    }, []);

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

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm({
            ...form,
            [name]: value,
        });
    };

    const addDriver = async () => {
        try {
            const response = await axios.post('/api/drivers/', form, {
                headers: { Authorization: `Token ${token}` }
            });
            if (response.status === 201) {
                fetchDrivers();
                resetForm();
            }
        } catch (error) {
            console.error('Ошибка при добавлении водителя:', error.response?.data || error.message);
        }
    };

    const resetForm = () => {
        setForm({
            passport_data: '',
            driver_class: '',
            work_experience: 0,
            salary: '',
            date_of_birth: ''
        });
        setEditDriverId(null);
    };

    const editDriver = (driver) => {
        setForm(driver);
        setEditDriverId(driver.id);
    };

    const updateDriver = async () => {
        try {
            const response = await axios.put(`/api/drivers/${editDriverId}/`, form, {
                headers: { Authorization: `Token ${token}` }
            });
            if (response.status === 200) {
                fetchDrivers();
                resetForm();
            }
        } catch (error) {
            console.error('Ошибка при обновлении водителя:', error.response?.data || error.message);
        }
    };

    const deleteDriver = async (id) => {
        if (window.confirm('Вы уверены, что хотите удалить этого водителя?')) {
            try {
                await axios.delete(`/api/drivers/${id}/`, {
                    headers: { Authorization: `Token ${token}` }
                });
                fetchDrivers();
            } catch (error) {
                console.error('Ошибка при удалении водителя:', error.response?.data || error.message);
            }
        }
    };

    return (
        <div className="drivers-container">
            <Header />
            <h2>Список водителей</h2>
            <table>
                <thead>
                <tr>
                    <th>ID</th>
                    <th>Паспортные данные</th>
                    <th>Класс водителя</th>
                    <th>Стаж работы</th>
                    <th>Зарплата</th>
                    <th>Дата рождения</th>
                    <th>Действия</th>
                </tr>
                </thead>
                <tbody>
                {drivers.map((driver) => (
                    <tr key={driver.id}>
                        <td>{driver.id}</td>
                        <td>{driver.passport_data}</td>
                        <td>{driver.driver_class}</td>
                        <td>{driver.work_experience}</td>
                        <td>{driver.salary}</td>
                        <td>{driver.date_of_birth}</td>
                        <td>
                            <button onClick={() => editDriver(driver)}>Редактировать</button>
                            <button onClick={() => deleteDriver(driver.id)}>Удалить</button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>

            <h3>{editDriverId ? 'Редактировать водителя' : 'Добавить водителя'}</h3>
            <input
                type="text"
                name="passport_data"
                placeholder="Паспортные данные"
                value={form.passport_data}
                onChange={handleChange}
                required
            />
            <input
                type="text"
                name="driver_class"
                placeholder="Класс водителя"
                value={form.driver_class}
                onChange={handleChange}
                required
            />
            <input
                type="number"
                name="work_experience"
                placeholder="Стаж работы"
                value={form.work_experience}
                onChange={handleChange}
                required
            />
            <input
                type="text"
                name="salary"
                placeholder="Зарплата"
                value={form.salary}
                onChange={handleChange}
                required
            />
            <input
                type="date"
                name="date_of_birth"
                placeholder="Дата рождения"
                value={form.date_of_birth}
                onChange={handleChange}
                required
            />

            {editDriverId ? (
                <button onClick={updateDriver}>Обновить водителя</button>
            ) : (
                <button onClick={addDriver}>Добавить водителя</button>
            )}
        </div>
    );
};

export default DriversPage;
