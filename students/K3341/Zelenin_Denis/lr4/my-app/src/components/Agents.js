import React, { useEffect, useState } from 'react';
import api from './api'; // Настроенный экземпляр axios
import './Agents.css';
import Main from "./Main";

function Agents() {
    const [contracts, setContracts] = useState([]);
    const [editingAgent, setEditingAgent] = useState(null);
    const [showAddForm, setShowAddForm] = useState(false);
    const [newAgentData, setNewAgentData] = useState({
        full_name: '',
        passport_details: '',
        contact_details: ''
    });

    // Загружаем данные контрактов при монтировании компонента
    useEffect(() => {
        api.get('/employment-contracts/')
            .then(response => setContracts(response.data))
            .catch(error => console.error('Error fetching contracts:', error));
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewAgentData(prevState => ({ ...prevState, [name]: value }));
    };

    const handleDeleteAgent = (agentId) => {
        api.delete(`/agents/${agentId}/`)
            .then(() => {
                setContracts(contracts.filter(contract => contract.insurance_agent.id !== agentId));
            })
            .catch(error => console.error('Error deleting agent:', error));
    };

    const handleEditAgent = (contract) => {
        setEditingAgent(contract.insurance_agent);
        setNewAgentData({
            full_name: contract.insurance_agent.full_name || '',
            passport_details: contract.insurance_agent.passport_details || '',
            contact_details: contract.insurance_agent.contact_details || ''
        });
    };

    const handleUpdateAgent = () => {
        if (!editingAgent) {
            console.error('No agent selected for update.');
            return;
        }

        api.put(`/agents/${editingAgent.id}/`, newAgentData)
            .then(response => {
                const updatedContracts = contracts.map(contract =>
                    contract.insurance_agent.id === editingAgent.id
                        ? { ...contract, insurance_agent: response.data }
                        : contract
                );
                setContracts(updatedContracts);
                setEditingAgent(null);
                setNewAgentData({
                    full_name: '',
                    passport_details: '',
                    contact_details: ''
                });
            })
            .catch(error => console.error('Error updating agent:', error));
    };

    const handleAddAgent = () => {
        api.post('/agents/', newAgentData)
            .then(response => {
                setContracts([...contracts, { insurance_agent: response.data }]);
                setShowAddForm(false);
                setNewAgentData({
                    full_name: '',
                    passport_details: '',
                    contact_details: ''
                });
            })
            .catch(error => console.error('Error adding agent:', error));
    };

    return (
        <div className="agents-container">
            <Main />
            <h1>Агенты</h1>
            <button onClick={() => setShowAddForm(true)} className="add-agent-btn">Добавить агента</button>

            {showAddForm && (
                <div className="add-agent-form">
                    <h3>Добавить нового агента</h3>
                    <label>
                        Полное имя:
                        <input
                            type="text"
                            name="full_name"
                            value={newAgentData.full_name}
                            onChange={handleInputChange}
                        />
                    </label>
                    <label>
                        Паспортные данные:
                        <input
                            type="text"
                            name="passport_details"
                            value={newAgentData.passport_details}
                            onChange={handleInputChange}
                        />
                    </label>
                    <label>
                        Контактные данные:
                        <input
                            type="text"
                            name="contact_details"
                            value={newAgentData.contact_details}
                            onChange={handleInputChange}
                        />
                    </label>
                    <button onClick={handleAddAgent}>Добавить</button>
                    <button onClick={() => setShowAddForm(false)}>Отмена</button>
                </div>
            )}

            {contracts.map(contract => (
                <div key={contract.id} className="agent-card">
                    <div className="card-header">
                        <h3>{contract.insurance_agent?.full_name || 'Без имени'}</h3>
                        <button onClick={() => handleEditAgent(contract)} className="edit-agent-btn">&#9998;</button>
                    </div>
                    <div className="card-details">
                        <p><strong>Паспортные данные:</strong> {contract.insurance_agent?.passport_details || 'Не указаны'}</p>
                        <p><strong>Контактные данные:</strong> {contract.insurance_agent?.contact_details || 'Не указаны'}</p>
                        <p><strong>Начало договора:</strong> {contract.start_date || 'Не указано'}</p>
                        <p><strong>Конец договора:</strong> {contract.end_date || 'Не указано'}</p>
                        <button onClick={() => handleDeleteAgent(contract.insurance_agent.id)} className="delete-agent-btn">&times;</button>
                    </div>
                    {editingAgent && editingAgent.id === contract.insurance_agent.id && (
                        <div className="edit-agent-form">
                            <h3>Редактировать агента</h3>
                            <label>
                                Полное имя:
                                <input
                                    type="text"
                                    name="full_name"
                                    value={newAgentData.full_name}
                                    onChange={handleInputChange}
                                />
                            </label>
                            <label>
                                Паспортные данные:
                                <input
                                    type="text"
                                    name="passport_details"
                                    value={newAgentData.passport_details}
                                    onChange={handleInputChange}
                                />
                            </label>
                            <label>
                                Контактные данные:
                                <input
                                    type="text"
                                    name="contact_details"
                                    value={newAgentData.contact_details}
                                    onChange={handleInputChange}
                                />
                            </label>
                            <button onClick={handleUpdateAgent}>Обновить</button>
                            <button onClick={() => setEditingAgent(null)}>Отмена</button>
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
}

export default Agents;
