import React, { useState, useEffect } from 'react';
import { getPatients, createPatient, deletePatient, updatePatient } from '../../api/patients';  // Импортируем API-функции
import PatientForm from '../../Component/Patients/PatientForm';
import './Patients.css';

const PatientsPage = () => {
    const [patients, setPatients] = useState([]);
    const [editingPatient, setEditingPatient] = useState(null);

    useEffect(() => {
        fetchPatients();
    }, []);

    const fetchPatients = async () => {
        try {
            const data = await getPatients();
            setPatients(data);
        } catch (error) {
            console.error("Ошибка при получении пациентов", error);
        }
    };

    const handleCreate = async (patientData) => {
        try {
            await createPatient(patientData);
            fetchPatients();
        } catch (error) {
            console.error("Ошибка при создании пациента", error);
        }
    };

    const handleUpdate = async (patientData) => {
        try {
            await updatePatient(patientData);
            fetchPatients();
        } catch (error) {
            console.error("Ошибка при обновлении пациента", error);
        }
    };

    const handleDelete = async (id) => {
        try {
            await deletePatient(id);
            fetchPatients();
        } catch (error) {
            console.error("Ошибка при удалении пациента", error);
        }
    };

    return (
        <div className="patients-page">
            <div className="add-patient">
                <h1>Добавить пациента</h1>
                <PatientForm
                    patient={editingPatient}
                    onCreate={handleCreate}
                    onUpdate={handleUpdate}
                />
            </div>
            <div className="patients-list">
                <h2>Список пациентов</h2>
                <table>
                    <thead>
                    <tr>
                        <th>Имя</th>
                        <th>Фамилия</th>
                        <th>Дата рождения</th>
                        <th>Действия</th>
                    </tr>
                    </thead>
                    <tbody>
                    {patients.map((patient) => (
                        <tr key={patient.id}>
                            <td>{patient.first_name}</td>
                            <td>{patient.last_name}</td>
                            <td>{patient.birth_date}</td>
                            <td>
                                <button onClick={() => setEditingPatient(patient)}>Редактировать</button>
                                <button onClick={() => handleDelete(patient.id)}>Удалить</button>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default PatientsPage;
