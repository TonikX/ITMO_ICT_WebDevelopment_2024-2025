import React, { useState, useEffect } from 'react';
import { getMedicalCards, deleteMedicalCard, createMedicalCard } from '../../api/medicalCards'; // Импортируем функции
import "./MedicalCard.css";

const MedicalCardsPage = () => {
    const [cards, setCards] = useState([]);
    const [filteredCards, setFilteredCards] = useState([]);
    const [filters, setFilters] = useState({ date: '', lastName: '', diagnosis: '' });
    const [newCardData, setNewCardData] = useState({
        patientFirstName: '',
        patientLastName: '',
        patientBirthDate: '',
        diagnosis: '',
        recordDate: ''
    });

    useEffect(() => {
        fetchMedicalCards();
    }, []);

    const fetchMedicalCards = async () => {
        try {
            const data = await getMedicalCards();
            const normalizedData = data.map(card => ({
                ...card,
                patient_full_name: `${card.patient.first_name} ${card.patient.last_name}`,
            }));
            setCards(normalizedData); 
            setFilteredCards(normalizedData);
        } catch (error) {
            console.error('Ошибка при получении медицинских карт:', error);
        }
    };

    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        setFilters({ ...filters, [name]: value });

        const filtered = cards.filter(card =>
            (filters.date === '' || card.record_date.includes(filters.date)) &&
            (filters.lastName === '' || card.patient.last_name.toLowerCase().includes(filters.lastName.toLowerCase())) &&
            (filters.diagnosis === '' || card.diagnosis.toLowerCase().includes(filters.diagnosis.toLowerCase()))
        );
        setFilteredCards(filtered); 
    };

    const handleDelete = async (patientId) => {
        try {
            if (!patientId) {
                console.error('Не удалось найти ID пациента для удаления');
                return;
            }

            
            await deleteMedicalCard(patientId);
            setCards(cards.filter(card => card.patient.id !== patientId)); 
            setFilteredCards(filteredCards.filter(card => card.patient.id !== patientId));
            console.log('Медицинская карта и пациент удалены');
        } catch (error) {
            console.error('Ошибка при удалении пациента и медицинской карты:', error);
        }
    };

    const handleAddCard = async () => {
        try {
            const newCard = await createMedicalCard({
                patient: {
                    first_name: newCardData.patientFirstName,
                    last_name: newCardData.patientLastName,
                    birth_date: newCardData.patientBirthDate,
                },
                record_date: newCardData.recordDate,
                diagnosis: newCardData.diagnosis
            });
            setCards([newCard, ...cards]); 
            setFilteredCards([newCard, ...filteredCards]);
            console.log('Медицинская карта добавлена');
        } catch (error) {
            console.error('Ошибка при добавлении новой медицинской карты:', error);
        }
    };

    const handleChangeNewCardData = (e) => {
        const { name, value } = e.target;
        setNewCardData({ ...newCardData, [name]: value });
    };

    return (
        <div className="medical-cards-page">
            <h1>Список медицинских карт</h1>

            <div className="filters">
                <input
                    type="text"
                    name="lastName"
                    placeholder="Фамилия пациента"
                    value={filters.lastName}
                    onChange={handleFilterChange}
                />
                <input
                    type="date"
                    name="date"
                    value={filters.date}
                    onChange={handleFilterChange}
                />
                <input
                    type="text"
                    name="diagnosis"
                    placeholder="Диагноз"
                    value={filters.diagnosis}
                    onChange={handleFilterChange}
                />
            </div>

            <button onClick={handleAddCard}>Добавить медицинскую карту</button>

            <div className="new-card-form">
                <input
                    type="text"
                    name="patientFirstName"
                    placeholder="Имя пациента"
                    value={newCardData.patientFirstName}
                    onChange={handleChangeNewCardData}
                />
                <input
                    type="text"
                    name="patientLastName"
                    placeholder="Фамилия пациента"
                    value={newCardData.patientLastName}
                    onChange={handleChangeNewCardData}
                />
                <input
                    type="date"
                    name="patientBirthDate"
                    placeholder="Дата рождения пациента"
                    value={newCardData.patientBirthDate}
                    onChange={handleChangeNewCardData}
                />
                <input
                    type="text"
                    name="diagnosis"
                    placeholder="Диагноз"
                    value={newCardData.diagnosis}
                    onChange={handleChangeNewCardData}
                />
                <input
                    type="date"
                    name="recordDate"
                    value={newCardData.recordDate}
                    onChange={handleChangeNewCardData}
                />
            </div>

            <table className="medical-cards-table">
                <thead>
                <tr>
                    <th>ФИО пациента</th>
                    <th>Дата создания карты</th>
                    <th>Диагноз</th>
                    <th>Действия</th>
                </tr>
                </thead>
                <tbody>
                {filteredCards.length > 0 ? (
                    filteredCards.map((card, index) => (
                        <tr key={index}>
                            <td>{card.patient_full_name}</td>
                            <td>{card.record_date}</td>
                            <td>{card.diagnosis}</td>
                            <td>
                                <button onClick={() => handleDelete(card.patient.id)}>Удалить</button> {/* Используем patient.id для удаления */}
                            </td>
                        </tr>
                    ))
                ) : (
                    <tr>
                        <td colSpan="4">Нет данных</td>
                    </tr>
                )}
                </tbody>
            </table>
        </div>
    );
};

export default MedicalCardsPage;
