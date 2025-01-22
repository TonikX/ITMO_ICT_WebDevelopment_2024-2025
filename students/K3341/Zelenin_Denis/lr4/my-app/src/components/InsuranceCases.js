// src/pages/InsuranceCases.jsx
import React, { useState, useEffect } from 'react';
import api from './api';
import './InsuranceCases.css';
import Main from './Main';
import Footer from "./Footer";

function InsuranceCases() {
    const [cases, setCases] = useState([]);
    const [contracts, setContracts] = useState([]);
    const [employees, setEmployees] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [newCaseData, setNewCaseData] = useState({
        date: '',
        reason: '',
        decision: true,
        payout_amount: '',
        contract: '',
        emp: ''
    });
    const [editingCase, setEditingCase] = useState(null);

    useEffect(() => {
        api.get('/insurance-cases/')
            .then(response => setCases(response.data))
            .catch(error => console.error('Error fetching cases:', error));

        api.get('/collective-contracts/')
            .then(response => setContracts(response.data))
            .catch(error => console.error('Error fetching contracts:', error));

        api.get('/employee/')
            .then(response => setEmployees(response.data))
            .catch(error => console.error('Error fetching employees:', error));
    }, []);

    const handleInputChange = (e) => {
        const { name, value, type, checked } = e.target;
        setNewCaseData(prevState => ({
            ...prevState,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    const handleAddCase = () => {
        api.post('/insurance-cases/', newCaseData)
            .then(response => {
                setCases([...cases, response.data]);
                resetForm();
            })
            .catch(error => console.error('Error adding case:', error));
    };

    const handleEditCase = (caseItem) => {
        setEditingCase(caseItem);
        setNewCaseData({
            ...caseItem,
            contract: caseItem.contract,
            emp: caseItem.emp
        });
    };

    const handleUpdateCase = () => {
        api.put(`/insurance-cases/${editingCase.id}/`, newCaseData)
            .then(response => {
                setCases(cases.map(caseItem => caseItem.id === editingCase.id ? response.data : caseItem));
                resetForm();
            })
            .catch(error => console.error('Error updating case:', error));
    };

    const handleDeleteCase = (id) => {
        api.delete(`/insurance-cases/${id}/`)
            .then(() => setCases(cases.filter(caseItem => caseItem.id !== id)))
            .catch(error => console.error('Error deleting case:', error));
    };

    const resetForm = () => {
        setEditingCase(null);
        setNewCaseData({
            date: '',
            reason: '',
            decision: true,
            payout_amount: '',
            contract: '',
            emp: ''
        });
    };

    const filteredEmployees = employees.filter(emp =>
        emp.full_name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="cases-container">
            <Main />
            <h1>Страховые Случаи</h1>
            <table className="cases-table">
                <thead>
                <tr>
                    <th>Дата</th>
                    <th>Причина</th>
                    <th>Решение</th>
                    <th>Сумма выплаты</th>
                    <th>Договор</th>
                    <th>Сотрудник</th>
                    <th>Действия</th>
                </tr>
                </thead>
                <tbody>
                {cases.map(caseItem => (
                    <tr key={caseItem.id}>
                        <td>{caseItem.date}</td>
                        <td>{caseItem.reason}</td>
                        <td>{caseItem.decision ? 'Да' : 'Нет'}</td>
                        <td>{caseItem.payout_amount}</td>
                        <td>{contracts.find(contract => contract.id === caseItem.contract)?.type || 'Неизвестно'}</td>
                        <td>{employees.find(emp => emp.id === caseItem.emp)?.full_name || 'Неизвестно'}</td>
                        <td>
                            <button onClick={() => handleEditCase(caseItem)}>Редактировать</button>
                            <button onClick={() => handleDeleteCase(caseItem.id)}>Удалить</button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>

            <div className="add-case-form">
                <h3>{editingCase ? 'Редактировать случай' : 'Добавить новый случай'}</h3>
                <label>
                    Дата:
                    <input type="date" name="date" value={newCaseData.date} onChange={handleInputChange} />
                </label>
                <label>
                    Причина:
                    <input type="text" name="reason" value={newCaseData.reason} onChange={handleInputChange} />
                </label>
                <label>
                    Решение:
                    <input type="checkbox" name="decision" checked={newCaseData.decision} onChange={handleInputChange} />
                </label>
                <label>
                    Сумма выплаты:
                    <input type="text" name="payout_amount" value={newCaseData.payout_amount} onChange={handleInputChange} />
                </label>
                <label>
                    Договор:
                    <select name="contract" value={newCaseData.contract} onChange={handleInputChange}>
                        <option value="">Выберите договор</option>
                        {contracts.map(contract => (
                            <option key={contract.id} value={contract.id}>
                                {`${contract.id} - ${contract.start_date} - ${contract.end_date}`}
                            </option>
                        ))}
                    </select>
                </label>
                <label>
                    Поиск сотрудника:
                    <input
                        type="text"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        placeholder="Введите имя сотрудника"
                    />
                </label>
                <label>
                    Сотрудник:
                    <select name="emp" value={newCaseData.emp} onChange={handleInputChange}>
                        <option value="">Выберите сотрудника</option>
                        {filteredEmployees.map(emp => (
                            <option key={emp.id} value={emp.id}>{emp.full_name}</option>
                        ))}
                    </select>
                </label>
                <button onClick={editingCase ? handleUpdateCase : handleAddCase}>
                    {editingCase ? 'Обновить' : 'Добавить'}
                </button>
                {editingCase && <button onClick={resetForm}>Отмена</button>}
            </div>
            <Footer />
        </div>
    );
}

export default InsuranceCases;
