import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useToken } from '../stores/token';
import Header from '../components/header.jsx';
import '../Css/BusesPage.css';

const BusesPage = () => {
    const [buses, setBuses] = useState([]);
    const [busTypes, setBusTypes] = useState([]);
    const [form, setForm] = useState({
        bus_type: '',
        registration_number: '',
        in_service: false,
    });
    const [editBusId, setEditBusId] = useState(null);
    const { token } = useToken();

    useEffect(() => {
        fetchBuses();
        fetchBusTypes();
    }, []);

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

    const fetchBusTypes = async () => {
        try {
            const response = await axios.get('/api/bus-types/', {
                headers: { Authorization: `Token ${token}` }
            });
            setBusTypes(response.data);
        } catch (error) {
            console.error('Ошибка при получении типов автобусов:', error.response?.data || error.message);
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm({
            ...form,
            [name]: value,
        });
    };

    const handleCheckboxChange = (e) => {
        setForm({
            ...form,
            in_service: e.target.checked,
        });
    };

    const addBus = async () => {
        try {
            const response = await axios.post('/api/buses/', form, {
                headers: { Authorization: `Token ${token}` }
            });
            if (response.status === 201) {
                fetchBuses();
                resetForm();
            }
        } catch (error) {
            console.error('Ошибка при добавлении автобуса:', error.response?.data || error.message);
        }
    };

    const resetForm = () => {
        setForm({
            bus_type: '',
            registration_number: '',
            in_service: false,
        });
        setEditBusId(null);
    };

    const editBus = (bus) => {
        setForm({
            bus_type: bus.bus_type.id,
            registration_number: bus.registration_number,
            in_service: bus.in_service,
        });
        setEditBusId(bus.id);
    };

    const updateBus = async () => {
        try {
            const response = await axios.put(`/api/buses/${editBusId}/`, form, {
                headers: { Authorization: `Token ${token}` }
            });
            if (response.status === 200) {
                fetchBuses();
                resetForm();
            }
        } catch (error) {
            console.error('Ошибка при обновлении автобуса:', error.response?.data || error.message);
        }
    };

    const deleteBus = async (id) => {
        if (window.confirm('Вы уверены, что хотите удалить этот автобус?')) {
            try {
                await axios.delete(`/api/buses/${id}/`, {
                    headers: { Authorization: `Token ${token}` }
                });
                fetchBuses();
            } catch (error) {
                console.error('Ошибка при удалении автобуса:', error.response?.data || error.message);
            }
        }
    };

    return (
        <div className="buses-container">
            <Header />
            <h2>Список автобусов</h2>
            <table>
                <thead>
                <tr>
                    <th>ID</th>
                    <th>Тип автобуса</th>
                    <th>Регистрационный номер</th>
                    <th>В эксплуатации</th>
                    <th>Действия</th>
                </tr>
                </thead>
                <tbody>
                {buses.map((bus) => (
                    <tr key={bus.id}>
                        <td>{bus.id}</td>
                        <td>{bus.bus_type.name}</td>
                        <td>{bus.registration_number}</td>
                        <td>{bus.in_service ? 'Да' : 'Нет'}</td>
                        <td>
                            <button onClick={() => editBus(bus)}>Редактировать</button>
                            <button onClick={() => deleteBus(bus.id)}>Удалить</button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>

            <h3>{editBusId ? 'Редактировать автобус' : 'Добавить автобус'}</h3>

            <select name="bus_type" value={form.bus_type} onChange={handleChange} required>
                <option value="">Выберите тип автобуса</option>
                {busTypes.map((type) => (
                    <option key={type.id} value={type.id}>
                        {type.name} - Вместимость: {type.capacity}
                    </option>
                ))}
            </select>

            <input
                type="text"
                name="registration_number"
                placeholder="Регистрационный номер"
                value={form.registration_number}
                onChange={handleChange}
                required
            />
            <label>
                В эксплуатации:
                <input
                    type="checkbox"
                    checked={form.in_service}
                    onChange={handleCheckboxChange}
                />
            </label>

            {/* Кнопки */}
            {editBusId ? (
                <button onClick={updateBus}>Обновить автобус</button>
            ) : (
                <button onClick={addBus}>Добавить автобус</button>
            )}
        </div>
    );
};

export default BusesPage;
