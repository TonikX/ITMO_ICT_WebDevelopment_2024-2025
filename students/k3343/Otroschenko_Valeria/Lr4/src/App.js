import React from "react";
import { Route, Routes } from "react-router-dom";
import Header from "./Component/Header/Header";
import Footer from "./Component/Footer/Footer";
import Home from "./pages/Home/Home";
import Login from "./pages/Login/Login";
import Signup from "./pages/Signup/Signup";
import PatientsPage from "./pages/Patinets/PatientsPage";
import MedicalCardsPage from "./pages/MedicalCard/MedicalCardsPage";
import DoctorsPage from "./pages/Doctors/DoctorsPage";
import AppointmentsPage from "./pages/AppointmentsPage/AppointmentsPage";
import ServicesPage from "./pages/Services/ServicesPage";

function App() {
    return (
        <div className="wrapper">
            <Header />
            <main className="main-content">
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/signup" element={<Signup />} />
                    <Route path="/patients" element={<PatientsPage />} />
                    <Route path="/medical-cards" element={<MedicalCardsPage />} />
                    <Route path="/doctors" element={<DoctorsPage />} />
                    <Route path="/appointments" element={<AppointmentsPage />} />
                    <Route path="/services" element={<ServicesPage />} />
                </Routes>
            </main>
            <Footer />
        </div>
    );
}

export default App;
