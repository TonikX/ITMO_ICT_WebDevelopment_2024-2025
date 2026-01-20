import React, { useState, useEffect } from 'react';
import api from './api'; // Предполагается, что здесь настроен axios экземпляр
import './Employees.css';
import Main from "./Main";
import Footer from "./Footer"; // Стили для компонента

function Employees() {
    const [employees, setEmployees] = useState([]);
    const [newEmployee, setNewEmployee] = useState({
        full_name: '',
        age: '',
        risk_category: ''
    });
    const [editingEmployee, setEditingEmployee] = useState(null);

    useEffect(() => {
        api.get('/employee/')
            .then(response => setEmployees(response.data))
            .catch(error => console.error('Error fetching employees:', error));
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewEmployee(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleAddEmployee = () => {
        api.post('/employee/', newEmployee)
            .then(response => {
                setEmployees([...employees, response.data]);
                resetForm();
            })
            .catch(error => console.error('Error adding employee:', error));
    };

    const handleEditEmployee = (employee) => {
        setEditingEmployee(employee);
        setNewEmployee(employee);
    };

    const handleUpdateEmployee = () => {
        api.put(`/employee/${editingEmployee.id}/`, newEmployee)
            .then(response => {
                setEmployees(employees.map(emp => emp.id === editingEmployee.id ? response.data : emp));
                resetForm();
            })
            .catch(error => console.error('Error updating employee:', error));
    };

    const handleDeleteEmployee = (id) => {
        api.delete(`/employee/${id}/`)
            .then(() => setEmployees(employees.filter(emp => emp.id !== id)))
            .catch(error => console.error('Error deleting employee:', error));
    };

    const resetForm = () => {
        setEditingEmployee(null);
        setNewEmployee({
            full_name: '',
            age: '',
            risk_category: ''
        });
    };

    return (
        <div className="employees-container">
            <Main />
            <h1>Сотрудники</h1>
            <table className="employees-table">
                <thead>
                <tr>
                    <th>Полное имя</th>
                    <th>Возраст</th>
                    <th>Категория риска</th>
                    <th>Действия</th>
                </tr>
                </thead>
                <tbody>
                {employees.map(employee => (
                    <tr key={employee.id}>
                        <td>{employee.full_name}</td>
                        <td>{employee.age}</td>
                        <td>{employee.risk_category}</td>
                        <td>
                            <button onClick={() => handleEditEmployee(employee)}>Редактировать</button>
                            <button onClick={() => handleDeleteEmployee(employee.id)}>Удалить</button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>

            <div className="employee-form">
                <h3>{editingEmployee ? 'Редактировать сотрудника' : 'Добавить нового сотрудника'}</h3>
                <label>
                    Полное имя:
                    <input type="text" name="full_name" value={newEmployee.full_name} onChange={handleInputChange} />
                </label>
                <label>
                    Возраст:
                    <input type="number" name="age" value={newEmployee.age} onChange={handleInputChange} />
                </label>
                <label>
                    Категория риска:
                    <input type="text" name="risk_category" value={newEmployee.risk_category} onChange={handleInputChange} />
                </label>
                <button onClick={editingEmployee ? handleUpdateEmployee : handleAddEmployee}>
                    {editingEmployee ? 'Обновить' : 'Добавить'}
                </button>
                {editingEmployee && <button onClick={resetForm}>Отмена</button>}
            </div>
            <Footer />
        </div>
    );
}

export default Employees;
