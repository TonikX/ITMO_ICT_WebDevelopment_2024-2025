import React, { useEffect, useState } from "react";
import { getServices, createService, deleteService } from "../../api/services";
import "./ServicesPage.css";

const ServicesPage = () => {
    const [services, setServices] = useState([]);
    const [newServiceName, setNewServiceName] = useState("");
    const [newServiceDescription, setNewServiceDescription] = useState("");

    // Загрузка списка сервисов
    useEffect(() => {
        fetchServices();
    }, []);

    const fetchServices = async () => {
        try {
            const data = await getServices();
            setServices(data);
        } catch (error) {
            console.error("Ошибка при получении сервисов:", error);
        }
    };

    // Добавление нового сервиса
    const handleAddService = async () => {
        if (!newServiceName.trim()) {
            alert("Название сервиса не может быть пустым.");
            return;
        }

        if (!newServiceDescription.trim()) {
            alert("Описание сервиса не может быть пустым.");
            return;
        }

        try {
            await createService({
                service_name: newServiceName,
                description: newServiceDescription,
            });
            setNewServiceName("");
            setNewServiceDescription("");
            fetchServices(); // Обновление списка
        } catch (error) {
            console.error("Ошибка при добавлении сервиса:", error);
        }
    };

    // Удаление сервиса
    const handleDeleteService = async (serviceId) => {
        try {
            await deleteService(serviceId);
            fetchServices(); // Обновление списка
        } catch (error) {
            console.error("Ошибка при удалении сервиса:", error);
        }
    };

    return (
        <div className="services-page">
            <h1>Services</h1>
            <div className="services-list">
                {services.length === 0 ? (
                    <p>No services available.</p>
                ) : (
                    services.map((service) => (
                        <div key={service.id} className="service-item">
                            <div className="service-details">
                                <span className="service-name">{service.service_name}</span>
                                <p className="service-description">{service.description}</p>
                            </div>
                            <button
                                className="delete-button"
                                onClick={() => handleDeleteService(service.id)}
                            >
                                Delete
                            </button>
                        </div>
                    ))
                )}
            </div>
            <div className="add-service">
                <input
                    type="text"
                    value={newServiceName}
                    onChange={(e) => setNewServiceName(e.target.value)}
                    placeholder="Service Name"
                    className="input-field"
                />
                <textarea
                    value={newServiceDescription}
                    onChange={(e) => setNewServiceDescription(e.target.value)}
                    placeholder="Service Description"
                    className="textarea-field"
                />
                <button className="add-button" onClick={handleAddService}>
                    Add Service
                </button>
            </div>
        </div>
    );
};

export default ServicesPage;
