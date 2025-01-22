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
    const [isModalOpen, setIsModalOpen] = useState(false); // Состояние для управления модальным окном

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
        setIsModalOpen(true); // Открыть модальное окно
    };

    const handleSaveCard = async () => {
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
            setIsModalOpen(false); // Закрыть модальное окно
            console.log('Медицинская карта добавлена');
        } catch (error) {
            console.error('Ошибка при добавлении новой медицинской карты:', error);
        }
    };

    const handleChangeNewCardData = (e) => {
        const { name, value } = e.target;
        setNewCardData({ ...newCardData, [name]: value });
    };

    const handleCloseModal = () => {
        setIsModalOpen(false); // Закрыть модальное окно
    };

    return (
        <div className="medical-cards-page">
            <header className="page-header">
                <h1>Медицинские карты</h1>
                <button className="add-card-button" onClick={handleAddCard}>
                    Добавить карту
                </button>
            </header>

            <section className="filters-section">
                <h2>Фильтры</h2>
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
            </section>

            <section className="cards-list">
                {filteredCards.length > 0 ? (
                    filteredCards.map((card, index) => (
                        <div className="card" key={index}>
                            <div className="card-header">
                                <h3>{card.patient_full_name}</h3>
                                <span>{card.record_date}</span>
                            </div>
                            <div className="card-body">
                                <p><strong>Диагноз:</strong> {card.diagnosis}</p>
                            </div>
                            <div className="card-footer">
                                <button className="delete-button" onClick={() => handleDelete(card.patient.id)}>
                                    Удалить
                                </button>
                            </div>
                        </div>
                    ))
                ) : (
                    <p className="no-data-message">Нет данных</p>
                )}
            </section>

            {/* Модальное окно */}
            {isModalOpen && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h2>Добавить новую карту</h2>
                        <form>
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
                                placeholder="Дата записи"
                                value={newCardData.recordDate}
                                onChange={handleChangeNewCardData}
                            />
                            <div className="modal-actions">
                                <button type="button" onClick={handleSaveCard}>
                                    Сохранить
                                </button>
                                <button type="button" onClick={handleCloseModal}>
                                    Отмена
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default MedicalCardsPage;