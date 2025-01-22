import React, { useState, useEffect } from 'react';

const PatientForm = ({ patient, onCreate, onUpdate }) => {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [birthDate, setBirthDate] = useState('');
    const [address, setAddress] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');

    // Заполнение формы данными пациента при редактировании
    useEffect(() => {
        if (patient) {
            setFirstName(patient.first_name);
            setLastName(patient.last_name);
            setBirthDate(patient.birth_date);
            setAddress(patient.address);
            setPhoneNumber(patient.phone_number);
        }
    }, [patient]);

    const handleSubmit = (e) => {
        e.preventDefault();
        const patientData = { first_name: firstName, last_name: lastName, birth_date: birthDate, address, phone_number: phoneNumber };

        if (patient) {
            onUpdate({ ...patientData, id: patient.id });
        } else {
            onCreate(patientData);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                placeholder="Имя"
            />
            <input
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                placeholder="Фамилия"
            />
            <input
                type="date"
                value={birthDate}
                onChange={(e) => setBirthDate(e.target.value)}
            />
            <input
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                placeholder="Адрес"
            />
            <input
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                placeholder="Номер телефона"
            />
            <button type="submit">{patient ? 'Обновить' : 'Добавить пациента'}</button>
        </form>
    );
};

export default PatientForm;
