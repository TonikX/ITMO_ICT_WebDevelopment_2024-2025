import React, { useEffect, useState } from "react";
import { getAppointments, addAppointment, updateAppointment, deleteAppointment } from "../../api/appointments";
import { getPatients, getDoctors, getCabinets, getServices } from "../../api/utils";
import "./AppointmentsPage.css";

const AppointmentsPage = () => {
    const [appointments, setAppointments] = useState([]);
    const [patients, setPatients] = useState([]);
    const [doctors, setDoctors] = useState([]);
    const [cabinets, setCabinets] = useState([]);
    const [services, setServices] = useState([]);
    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [isEditModalOpen, setIsEditModalOpen] = useState(false);
    const [newAppointment, setNewAppointment] = useState({
        appointment_date: "",
        appointment_time: "",
        patient: "",
        doctor: "",
        cabinet: "",
        service: "",
    });
    const [selectedAppointment, setSelectedAppointment] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [appointmentsData, patientsData, doctorsData, cabinetsData, servicesData] = await Promise.all([
                    getAppointments(),
                    getPatients(),
                    getDoctors(),
                    getCabinets(),
                    getServices(),
                ]);
                setAppointments(appointmentsData);
                setPatients(patientsData);
                setDoctors(doctorsData);
                setCabinets(cabinetsData);
                setServices(servicesData);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };

        fetchData();
    }, []);

    const handleAddAppointment = async () => {
        try {
            await addAppointment(newAppointment);
            setIsAddModalOpen(false);
            setNewAppointment({
                appointment_date: "",
                appointment_time: "",
                patient: "",
                doctor: "",
                cabinet: "",
                service: "",
            });
            const updatedAppointments = await getAppointments();
            setAppointments(updatedAppointments);
        } catch (error) {
            console.error("Error adding appointment:", error);
            alert("Failed to add appointment.");
        }
    };

    const handleEditAppointment = (appointment) => {
        setSelectedAppointment(appointment);
        setNewAppointment(appointment);
        setIsEditModalOpen(true);
    };

    const handleUpdateAppointment = async () => {
        try {
            await updateAppointment(selectedAppointment.id, newAppointment);
            setIsEditModalOpen(false);
            setSelectedAppointment(null);
            setNewAppointment({
                appointment_date: "",
                appointment_time: "",
                patient: "",
                doctor: "",
                cabinet: "",
                service: "",
            });
            const updatedAppointments = await getAppointments();
            setAppointments(updatedAppointments);
        } catch (error) {
            console.error("Error updating appointment:", error);
            alert("Failed to update appointment.");
        }
    };

    const handleDeleteAppointment = async (appointmentId) => {
        try {
            await deleteAppointment(appointmentId);
            const updatedAppointments = await getAppointments();
            setAppointments(updatedAppointments);
        } catch (error) {
            console.error("Error deleting appointment:", error);
        }
    };

    const getPatientName = (patientId) => {
        const patient = patients.find((p) => p.id === patientId);
        return patient ? `${patient.first_name} ${patient.last_name}` : "Unknown";
    };

    const getDoctorName = (doctorId) => {
        const doctor = doctors.find((d) => d.id === doctorId);
        return doctor ? `${doctor.first_name} ${doctor.last_name}` : "Unknown";
    };

    return (
        <div className="appointments-page">
            <h1>Appointments</h1>
            <div className="appointments-list">
                {appointments.map((appointment) => (
                    <div key={appointment.id} className="appointment-card">
                        <h2>
                            {getPatientName(appointment.patient)} - {getDoctorName(appointment.doctor)}
                        </h2>
                        <p>
                            {appointment.appointment_date} {appointment.appointment_time}
                        </p>
                        <button onClick={() => handleEditAppointment(appointment)}>Edit</button>
                        <button onClick={() => handleDeleteAppointment(appointment.id)} className="delete-button">
                            Delete
                        </button>
                    </div>
                ))}
            </div>
            <button onClick={() => setIsAddModalOpen(true)}>Add Appointment</button>
            {isAddModalOpen && (
                <div className="modal">
                    <h2>Add Appointment</h2>
                    <form>
                        <input
                            type="date"
                            value={newAppointment.appointment_date}
                            onChange={(e) => setNewAppointment({ ...newAppointment, appointment_date: e.target.value })}
                        />
                        <input
                            type="time"
                            value={newAppointment.appointment_time}
                            onChange={(e) => setNewAppointment({ ...newAppointment, appointment_time: e.target.value })}
                        />
                        <select
                            value={newAppointment.patient}
                            onChange={(e) => setNewAppointment({ ...newAppointment, patient: e.target.value })}
                        >
                            <option value="">Select Patient</option>
                            {patients.map((p) => (
                                <option key={p.id} value={p.id}>
                                    {p.first_name} {p.last_name}
                                </option>
                            ))}
                        </select>
                        <select
                            value={newAppointment.doctor}
                            onChange={(e) => setNewAppointment({ ...newAppointment, doctor: e.target.value })}
                        >
                            <option value="">Select Doctor</option>
                            {doctors.map((d) => (
                                <option key={d.id} value={d.id}>
                                    {d.first_name} {d.last_name}
                                </option>
                            ))}
                        </select>
                        <select
                            value={newAppointment.cabinet}
                            onChange={(e) => setNewAppointment({ ...newAppointment, cabinet: e.target.value })}
                        >
                            <option value="">Select Cabinet</option>
                            {cabinets.map((c) => (
                                <option key={c.id} value={c.id}>
                                    Cabinet {c.number}
                                </option>
                            ))}
                        </select>
                        <select
                            value={newAppointment.service}
                            onChange={(e) => setNewAppointment({ ...newAppointment, service: e.target.value })}
                        >
                            <option value="">Select Service</option>
                            {services.map((s) => (
                                <option key={s.id} value={s.id}>
                                    {s.name}
                                </option>
                            ))}
                        </select>
                        <button type="button" onClick={handleAddAppointment}>
                            Add
                        </button>
                        <button type="button" onClick={() => setIsAddModalOpen(false)}>
                            Cancel
                        </button>
                    </form>
                </div>
            )}
            {isEditModalOpen && (
                <div className="modal">
                    <h2>Edit Appointment</h2>
                    <form>
                        <input
                            type="date"
                            value={newAppointment.appointment_date}
                            onChange={(e) => setNewAppointment({ ...newAppointment, appointment_date: e.target.value })}
                        />
                        <input
                            type="time"
                            value={newAppointment.appointment_time}
                            onChange={(e) => setNewAppointment({ ...newAppointment, appointment_time: e.target.value })}
                        />
                        <select
                            value={newAppointment.patient}
                            onChange={(e) => setNewAppointment({ ...newAppointment, patient: e.target.value })}
                        >
                            <option value="">Select Patient</option>
                            {patients.map((p) => (
                                <option key={p.id} value={p.id}>
                                    {p.first_name} {p.last_name}
                                </option>
                            ))}
                        </select>
                        <select
                            value={newAppointment.doctor}
                            onChange={(e) => setNewAppointment({ ...newAppointment, doctor: e.target.value })}
                        >
                            <option value="">Select Doctor</option>
                            {doctors.map((d) => (
                                <option key={d.id} value={d.id}>
                                    {d.first_name} {d.last_name}
                                </option>
                            ))}
                        </select>
                        <select
                            value={newAppointment.cabinet}
                            onChange={(e) => setNewAppointment({ ...newAppointment, cabinet: e.target.value })}
                        >
                            <option value="">Select Cabinet</option>
                            {cabinets.map((c) => (
                                <option key={c.id} value={c.id}>
                                    Cabinet {c.number}
                                </option>
                            ))}
                        </select>
                        <select
                            value={newAppointment.service}
                            onChange={(e) => setNewAppointment({ ...newAppointment, service: e.target.value })}
                        >
                            <option value="">Select Service</option>
                            {services.map((s) => (
                                <option key={s.id} value={s.id}>
                                    {s.name}
                                </option>
                            ))}
                        </select>
                        <button type="button" onClick={handleUpdateAppointment}>
                            Save
                        </button>
                        <button type="button" onClick={() => setIsEditModalOpen(false)}>
                            Cancel
                        </button>
                    </form>
                </div>
            )}
        </div>
    );
};

export default AppointmentsPage;
