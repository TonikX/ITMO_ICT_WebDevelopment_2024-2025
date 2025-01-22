import React, { useEffect, useState } from "react";
import { getDoctors, addDoctor, deleteDoctor } from "../../api/doctor"; // Предполагаются соответствующие API-функции
import "./DoctorsPage.css";

const DoctorsPage = () => {
    const [doctors, setDoctors] = useState([]);
    const [selectedDoctor, setSelectedDoctor] = useState(null);
    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
    const [newDoctor, setNewDoctor] = useState({
        first_name: "",
        last_name: "",
        sex: "M",
        education: "",
        birth_date: "",
        speciality: "",
    });

    // Загрузка списка врачей
    useEffect(() => {
        const fetchDoctors = async () => {
            try {
                const data = await getDoctors();
                setDoctors(data);
            } catch (error) {
                console.error("Error fetching doctors:", error);
            }
        };

        fetchDoctors();
    }, []);

    const handleAddDoctor = async () => {
        try {
            await addDoctor(newDoctor);
            setIsAddModalOpen(false);
            setNewDoctor({
                first_name: "",
                last_name: "",
                sex: "M",
                education: "",
                birth_date: "",
                speciality: "",
            });
            const updatedDoctors = await getDoctors();
            setDoctors(updatedDoctors);
        } catch (error) {
            console.error("Error adding doctor:", error);
        }
    };

    const handleDeleteDoctor = async (doctorId) => {
        try {
            await deleteDoctor(doctorId);
            setIsDeleteModalOpen(false);
            const updatedDoctors = await getDoctors();
            setDoctors(updatedDoctors);
        } catch (error) {
            console.error("Error deleting doctor:", error);
        }
    };

    return (
        <div className="doctors-page">
            <h1>Our Doctors</h1>
            <div className="doctors-grid">
                {doctors.map((doctor) => (
                    <div
                        key={doctor.id}
                        className="doctor-card"
                        onClick={() => setSelectedDoctor(doctor)}
                    >
                        <h2>{doctor.first_name} {doctor.last_name}</h2>
                        <p>Speciality: {doctor.speciality}</p>
                    </div>
                ))}
            </div>

            <div className="actions">
                <button className="add-button" onClick={() => setIsAddModalOpen(true)}>
                    Add Doctor
                </button>
                <button className="delete-button" onClick={() => setIsDeleteModalOpen(true)}>
                    Delete Doctor
                </button>
            </div>

            {/* Модальное окно подробной информации */}
            {selectedDoctor && (
                <div className="modal-overlay" onClick={() => setSelectedDoctor(null)}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <h2>{selectedDoctor.first_name} {selectedDoctor.last_name}</h2>
                        <p><strong>Sex:</strong> {selectedDoctor.sex === "M" ? "Male" : "Female"}</p>
                        <p><strong>Education:</strong> {selectedDoctor.education}</p>
                        <p><strong>Birth Date:</strong> {selectedDoctor.birth_date}</p>
                        <p><strong>Speciality:</strong> {selectedDoctor.speciality}</p>
                        <button className="close-modal" onClick={() => setSelectedDoctor(null)}>
                            Close
                        </button>
                    </div>
                </div>
            )}

            {/* Модальное окно добавления врача */}
            {isAddModalOpen && (
                <div className="modal-overlay" onClick={() => setIsAddModalOpen(false)}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <h2>Add New Doctor</h2>
                        <input
                            type="text"
                            placeholder="First Name"
                            value={newDoctor.first_name}
                            onChange={(e) => setNewDoctor({ ...newDoctor, first_name: e.target.value })}
                        />
                        <input
                            type="text"
                            placeholder="Last Name"
                            value={newDoctor.last_name}
                            onChange={(e) => setNewDoctor({ ...newDoctor, last_name: e.target.value })}
                        />
                        <select
                            value={newDoctor.sex}
                            onChange={(e) => setNewDoctor({ ...newDoctor, sex: e.target.value })}
                        >
                            <option value="M">Male</option>
                            <option value="F">Female</option>
                        </select>
                        <input
                            type="text"
                            placeholder="Education"
                            value={newDoctor.education}
                            onChange={(e) => setNewDoctor({ ...newDoctor, education: e.target.value })}
                        />
                        <input
                            type="date"
                            value={newDoctor.birth_date}
                            onChange={(e) => setNewDoctor({ ...newDoctor, birth_date: e.target.value })}
                        />
                        <input
                            type="text"
                            placeholder="Speciality"
                            value={newDoctor.speciality}
                            onChange={(e) => setNewDoctor({ ...newDoctor, speciality: e.target.value })}
                        />
                        <button className="submit-button" onClick={handleAddDoctor}>
                            Add
                        </button>
                        <button className="close-modal" onClick={() => setIsAddModalOpen(false)}>
                            Close
                        </button>
                    </div>
                </div>
            )}

            {/* Модальное окно удаления врача */}
            {isDeleteModalOpen && (
                <div className="modal-overlay" onClick={() => setIsDeleteModalOpen(false)}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <h2>Delete Doctor</h2>
                        {doctors.map((doctor) => (
                            <div key={doctor.id} className="delete-item">
                                <span>{doctor.first_name} {doctor.last_name}</span>
                                <button className="delete-button" onClick={() => handleDeleteDoctor(doctor.id)}>
                                    Delete
                                </button>
                            </div>
                        ))}
                        <button className="close-modal" onClick={() => setIsDeleteModalOpen(false)}>
                            Close
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default DoctorsPage;
