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
            <header className="page-header">
                <h1>Управление пациентами</h1>
            </header>

            <section className="add-patient-section">
                <div className="form-container">
                    <h2>Добавить нового пациента</h2>
                    <PatientForm
                        patient={editingPatient}
                        onCreate={handleCreate}
                        onUpdate={handleUpdate}
                    />
                </div>
            </section>

            <section className="patients-list-section">
                <div className="list-container">
                    {patients.map((patient) => (
                        <div className="patient-card" key={patient.id}>
                            <div className="card-header">
                                <h3>{`${patient.first_name} ${patient.last_name}`}</h3>
                            </div>
                            <div className="card-body">
                                <p><strong>Дата рождения:</strong> {patient.birth_date}</p>
                            </div>
                            <div className="card-footer">
                                <button className="edit-button"
                                        onClick={() => setEditingPatient(patient)}>Редактировать
                                </button>
                                <button className="delete-button" onClick={() => handleDelete(patient.id)}>Удалить
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            </section>
        </div>
    );
};

export default PatientsPage;
