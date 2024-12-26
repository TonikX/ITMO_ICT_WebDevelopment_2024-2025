import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { CssBaseline } from "@mui/material";
import Login from "./components/Login";
import SignUp from "./components/SignUp";
import Patients from "./components/Patients";
import DoctorManagement from "./components/Doctors";
import Schedule from "./components/Schedule";
import Visits from "./components/Visits";
import Accounting from "./components/Accounting";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/patients" element={<Patients />} />
        <Route path="/doctors" element={<DoctorManagement />} />
        <Route path="/schedule" element={<Schedule />} />
        <Route path="/visits" element={<Visits />} />
        <Route path="/accounting" element={<Accounting />} />
      </Routes>
    </Router>
  );
}

export default App;
