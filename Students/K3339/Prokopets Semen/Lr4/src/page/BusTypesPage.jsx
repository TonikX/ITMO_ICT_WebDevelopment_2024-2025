import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useToken } from '../stores/token';
import Header from '../components/header.jsx';
import '../Css/BusTypesPage.css';
const BusTypesPage = () => {
    const [busTypes, setBusTypes] = useState([]);
    const [form, setForm] = useState({
        name: '',
        capacity: 0,
    });
    const [editBusTypeId, setEditBusTypeId] = useState(null);
    const { token } = useToken();

    useEffect(() => {
        fetchBusTypes();
    }, []);

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

    const addBusType = async () => {
        try {
            const response = await axios.post('/api/bus-types/', form, {
                headers: { Authorization: `Token ${token}` }
            });
            if (response.status === 201) {
                fetchBusTypes();
                resetForm();
            }
        } catch (error) {
            console.error('Ошибка при добавлении типа автобуса:', error.response?.data || error.message);
        }
    };

    const resetForm = () => {
        setForm({
            name: '',
            capacity: 0,
        });
        setEditBusTypeId(null);
    };

    const editBusType = (busType) => {
        setForm({
            name: busType.name,
            capacity: busType.capacity,
        });
        setEditBusTypeId(busType.id);
    };

    const updateBusType = async () => {
        try {
            const response = await axios.put(`/api/bus-types/${editBusTypeId}/`, form, {
                headers: { Authorization: `Token ${token}` }
            });
            if (response.status === 200) {
                fetchBusTypes();
                resetForm();
            }
        } catch (error) {
            console.error('Ошибка при обновлении типа автобуса:', error.response?.data || error.message);
        }
    };

    const deleteBusType = async (id) => {
        if (window.confirm('Вы уверены, что хотите удалить этот тип автобуса?')) {
            try {
                await axios.delete(`/api/bus-types/${id}/`, {
                    headers: { Authorization: `Token ${token}` }
                });
                fetchBusTypes();
            } catch (error) {
                console.error('Ошибка при удалении типа автобуса:', error.response?.data || error.message);
            }
        }
    };

    return (
        <div className="bus-types-container">
            <Header></Header>
            <h2>Список типов автобусов</h2>
            <table>
                <thead>
                <tr>
                    <th>ID</th>
                    <th>Название</th>
                    <th>Вместимость</th>
                    <th>Действия</th>
                </tr>
                </thead>
                <tbody>
                {busTypes.map((busType) => (
                    <tr key={busType.id}>
                        <td>{busType.id}</td>
                        <td>{busType.name}</td>
                        <td>{busType.capacity}</td>
                        <td>
                            <button onClick={() => editBusType(busType)}>Редактировать</button>
                            <button onClick={() => deleteBusType(busType.id)}>Удалить</button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>

            <h3>{editBusTypeId ? 'Редактировать тип автобуса' : 'Добавить тип автобуса'}</h3>
            <input
                type="text"
                name="name"
                placeholder="Название"
                value={form.name}
                onChange={handleChange}
                required
            />
            <input
                type="number"
                name="capacity"
                placeholder="Вместимость"
                value={form.capacity}
                onChange={handleChange}
                required
            />

            {editBusTypeId ? (
                <button onClick={updateBusType}>Обновить тип автобуса</button>
            ) : (
                <button onClick={addBusType}>Добавить тип автобуса</button>
            )}
        </div>
    );
};

export default BusTypesPage;
