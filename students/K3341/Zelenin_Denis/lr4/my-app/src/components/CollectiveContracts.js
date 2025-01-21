// src/pages/CollectiveContracts.jsx
import React, { useState, useEffect } from 'react';
import api from './api'; // Настроенный экземпляр axios
import './CollectiveContracts.css';
import Main from "./Main"; // Импортируем стили

function CollectiveContracts() {
    const [contracts, setContracts] = useState([]);
    const [organizations, setOrganizations] = useState([]);
    const [agents, setAgents] = useState([]);
    const [employees, setEmployees] = useState([]);
    const [newContractData, setNewContractData] = useState({
        type: 'collective',
        start_date: '',
        end_date: '',
        total_payout: '',
        organization: '',
        insurance_agent: '',
        employees: []
    });
    const [editingContract, setEditingContract] = useState(null);

    useEffect(() => {
        api.get('/collective-contracts/')
            .then(response => setContracts(response.data))
            .catch(error => console.error('Error fetching contracts:', error));

        api.get('/organizations/')
            .then(response => setOrganizations(response.data))
            .catch(error => console.error('Error fetching organizations:', error));

        api.get('/agents/')
            .then(response => setAgents(response.data))
            .catch(error => console.error('Error fetching agents:', error));

        api.get('/employee/')
            .then(response => setEmployees(response.data))
            .catch(error => console.error('Error fetching employees:', error));
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewContractData(prevState => ({
            ...prevState,
            [name]: name === 'employees' ? Array.from(e.target.selectedOptions, option => parseInt(option.value)) : value
        }));
    };

    const handleAddContract = () => {
        api.post('/collective-contracts/', newContractData)
            .then(response => {
                setContracts([...contracts, response.data]);
                resetForm();
            })
            .catch(error => console.error('Error adding contract:', error));
    };

    const handleEditContract = (contract) => {
        setEditingContract(contract);
        setNewContractData({
            ...contract,
            employees: contract.employees.map(emp => emp.id)
        });
    };

    const handleUpdateContract = () => {
        api.put(`/collective-contracts/${editingContract.id}/`, newContractData)
            .then(response => {
                setContracts(contracts.map(contract => contract.id === editingContract.id ? response.data : contract));
                resetForm();
            })
            .catch(error => console.error('Error updating contract:', error));
    };

    const handleDeleteContract = (id) => {
        api.delete(`/collective-contracts/${id}/`)
            .then(() => setContracts(contracts.filter(contract => contract.id !== id)))
            .catch(error => console.error('Error deleting contract:', error));
    };

    const resetForm = () => {
        setEditingContract(null);
        setNewContractData({
            type: 'collective',
            start_date: '',
            end_date: '',
            total_payout: '',
            organization: '',
            insurance_agent: '',
            employees: []
        });
    };

    return (
        <div className="contracts-container">
            <Main />
            <h1>Коллективные Договоры</h1>
            <table className="contracts-table">
                <thead>
                <tr>
                    <th>Тип</th>
                    <th>Дата начала</th>
                    <th>Дата окончания</th>
                    <th>Общая выплата</th>
                    <th>Организация</th>
                    <th>Агент</th>
                    <th>Сотрудники</th>
                    <th>Действия</th>
                </tr>
                </thead>
                <tbody>
                {contracts.map(contract => (
                    <tr key={contract.id}>
                        <td>{contract.type}</td>
                        <td>{contract.start_date}</td>
                        <td>{contract.end_date}</td>
                        <td>{contract.total_payout}</td>
                        <td>{organizations.find(org => org.id === contract.organization)?.full_name}</td>
                        <td>{agents.find(agent => agent.id === contract.insurance_agent)?.full_name}</td>
                        <td>{contract.employees.map(empId => employees.find(emp => emp.id === empId)?.full_name).join(', ')}</td>
                        <td>
                            <button onClick={() => handleEditContract(contract)}>Редактировать</button>
                            <button onClick={() => handleDeleteContract(contract.id)}>Удалить</button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>

            <div className="add-contract-form">
                <h3>{editingContract ? 'Редактировать договор' : 'Добавить новый договор'}</h3>
                <label>
                    Дата начала:
                    <input type="date" name="start_date" value={newContractData.start_date} onChange={handleInputChange} />
                </label>
                <label>
                    Дата окончания:
                    <input type="date" name="end_date" value={newContractData.end_date} onChange={handleInputChange} />
                </label>
                <label>
                    Общая выплата:
                    <input type="text" name="total_payout" value={newContractData.total_payout} onChange={handleInputChange} />
                </label>
                <label>
                    Организация:
                    <select name="organization" value={newContractData.organization} onChange={handleInputChange}>
                        <option value="">Выберите организацию</option>
                        {organizations.map(org => (
                            <option key={org.id} value={org.id}>{org.full_name}</option>
                        ))}
                    </select>
                </label>
                <label>
                    Агент:
                    <select name="insurance_agent" value={newContractData.insurance_agent} onChange={handleInputChange}>
                        <option value="">Выберите агента</option>
                        {agents.map(agent => (
                            <option key={agent.id} value={agent.id}>{agent.full_name}</option>
                        ))}
                    </select>
                </label>
                <label>
                    Сотрудники:
                    <select name="employees" multiple value={newContractData.employees} onChange={handleInputChange}>
                        {employees.map(emp => (
                            <option key={emp.id} value={emp.id}>{emp.full_name}</option>
                        ))}
                    </select>
                </label>
                <button onClick={editingContract ? handleUpdateContract : handleAddContract}>
                    {editingContract ? 'Обновить' : 'Добавить'}
                </button>
                {editingContract && <button onClick={resetForm}>Отмена</button>}
            </div>
        </div>
    );
}

export default CollectiveContracts;
