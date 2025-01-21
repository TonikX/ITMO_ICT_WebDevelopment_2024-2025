import React, { useEffect, useState } from 'react';
import api from './api'; // Настроенный экземпляр axios
import './Organizations.css';
import Main from "./Main";

function Organizations() {
    const [organizations, setOrganizations] = useState([]);
    const [editingOrg, setEditingOrg] = useState(null);
    const [showAddForm, setShowAddForm] = useState(false);
    const [newOrgData, setNewOrgData] = useState({
        code: '',
        full_name: '',
        short_name: '',
        address: '',
        bank_details: '',
        specialization: ''
    });

    useEffect(() => {
        api.get('/organizations/')
            .then(response => setOrganizations(response.data))
            .catch(error => console.error('Error fetching organizations:', error));
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewOrgData(prevState => ({ ...prevState, [name]: value }));
    };

    const handleDeleteOrganization = (id) => {
        api.delete(`/organizations/${id}/`)
            .then(() => setOrganizations(organizations.filter(org => org.id !== id)))
            .catch(error => console.error('Error deleting organization:', error));
    };

    const handleEditOrganization = (org) => {
        setEditingOrg(org);
        setNewOrgData(org);
    };

    const handleUpdateOrganization = () => {
        api.put(`/organizations/${editingOrg.id}/`, newOrgData)
            .then(response => {
                setOrganizations(organizations.map(org => org.id === editingOrg.id ? response.data : org));
                setEditingOrg(null);
                setNewOrgData({
                    code: '',
                    full_name: '',
                    short_name: '',
                    address: '',
                    bank_details: '',
                    specialization: ''
                });
            })
            .catch(error => console.error('Error updating organization:', error));
    };

    const handleAddOrganization = () => {
        api.post('/organizations/', newOrgData)
            .then(response => {
                setOrganizations([...organizations, response.data]);
                setShowAddForm(false);
                setNewOrgData({
                    code: '',
                    full_name: '',
                    short_name: '',
                    address: '',
                    bank_details: '',
                    specialization: ''
                });
            })
            .catch(error => console.error('Error adding organization:', error));
    };

    return (
        <div className="organizations-container">
            <Main />
            <h1>Организации</h1>
            <button onClick={() => setShowAddForm(true)} className="add-org-btn">Добавить организацию</button>

            {showAddForm && (
                <div className="add-org-form">
                    <h3>Добавить новую организацию</h3>
                    <label>
                        Код:
                        <input
                            type="text"
                            name="code"
                            value={newOrgData.code}
                            onChange={handleInputChange}
                        />
                    </label>
                    <label>
                        Полное имя:
                        <input
                            type="text"
                            name="full_name"
                            value={newOrgData.full_name}
                            onChange={handleInputChange}
                        />
                    </label>
                    <label>
                        Краткое имя:
                        <input
                            type="text"
                            name="short_name"
                            value={newOrgData.short_name}
                            onChange={handleInputChange}
                        />
                    </label>
                    <label>
                        Адрес:
                        <input
                            type="text"
                            name="address"
                            value={newOrgData.address}
                            onChange={handleInputChange}
                        />
                    </label>
                    <label>
                        Банковские реквизиты:
                        <input
                            type="text"
                            name="bank_details"
                            value={newOrgData.bank_details}
                            onChange={handleInputChange}
                        />
                    </label>
                    <label>
                        Специализация:
                        <input
                            type="text"
                            name="specialization"
                            value={newOrgData.specialization}
                            onChange={handleInputChange}
                        />
                    </label>
                    <button onClick={handleAddOrganization}>Добавить</button>
                    <button onClick={() => setShowAddForm(false)}>Отмена</button>
                </div>
            )}

            {organizations.map(org => (
                <div key={org.id} className="organization-card">
                    <div className="card-header">
                        <h3>{org.full_name}</h3>
                        <button onClick={() => handleEditOrganization(org)} className="edit-org-btn">&#9998;</button>
                    </div>
                    <div className="card-details">
                        <p><strong>Код:</strong> {org.code}</p>
                        <p><strong>Краткое имя:</strong> {org.short_name}</p>
                        <p><strong>Адрес:</strong> {org.address}</p>
                        <p><strong>Банковские реквизиты:</strong> {org.bank_details}</p>
                        <p><strong>Специализация:</strong> {org.specialization}</p>
                        <button onClick={() => handleDeleteOrganization(org.id)} className="delete-org-btn">&times;</button>
                    </div>
                    {editingOrg && editingOrg.id === org.id && (
                        <div className="edit-org-form">
                            <h3>Редактировать организацию</h3>
                            <label>
                                Код:
                                <input
                                    type="text"
                                    name="code"
                                    value={newOrgData.code}
                                    onChange={handleInputChange}
                                />
                            </label>
                            <label>
                                Полное имя:
                                <input
                                    type="text"
                                    name="full_name"
                                    value={newOrgData.full_name}
                                    onChange={handleInputChange}
                                />
                            </label>
                            <label>
                                Краткое имя:
                                <input
                                    type="text"
                                    name="short_name"
                                    value={newOrgData.short_name}
                                    onChange={handleInputChange}
                                />
                            </label>
                            <label>
                                Адрес:
                                <input
                                    type="text"
                                    name="address"
                                    value={newOrgData.address}
                                    onChange={handleInputChange}
                                />
                            </label>
                            <label>
                                Банковские реквизиты:
                                <input
                                    type="text"
                                    name="bank_details"
                                    value={newOrgData.bank_details}
                                    onChange={handleInputChange}
                                />
                            </label>
                            <label>
                                Специализация:
                                <input
                                    type="text"
                                    name="specialization"
                                    value={newOrgData.specialization}
                                    onChange={handleInputChange}
                                />
                            </label>
                            <button onClick={handleUpdateOrganization}>Обновить</button>
                            <button onClick={() => setEditingOrg(null)}>Отмена</button>
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
}

export default Organizations;
