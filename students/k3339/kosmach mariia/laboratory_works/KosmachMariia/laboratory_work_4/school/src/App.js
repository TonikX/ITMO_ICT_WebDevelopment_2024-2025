import React, { useEffect, useState } from "react";
import { Route, Routes, useLocation, useNavigate } from "react-router-dom";
import Login from "./page/Login";
import { PrivateRoute } from "./components/PrivateRoute";
import "./App.css";
import Registration from "./page/Registration";
import StudentList from "./page/StudentList"
import StudentForm from "./page/StudentForm/StudentForm";
import GradesList from "./page/GradesList/GradesList";
import GradesForm from "./page/GradesForm/GradesForm";
import GradeUpdateForm from "./page/GradeUpdateForm/GradeUpdateForm";
import Main from "./page/Main";
import StudentInfo from "./page/StudentInfo/StudentInfo";

function App() {
  return (
    <div>
      <Routes>
        <Route path="/">
          <Route path="/login" element={<Login />} />
          <Route path="/registration" element={<Registration />} />

          <Route element={<PrivateRoute />}>
            <Route index element={<Main />} />
            <Route path="/students" element={<StudentList />} />
            <Route path="/students/create" element={<StudentForm />} />
            <Route path="/grades/create" element={<GradesForm />} />
            <Route path="/grade/update/:gradeId" element={<GradeUpdateForm />} />
            <Route path="student/info/:studentId" element={<StudentInfo />} />
            <Route path="/grade" element={<GradesList />} />
          </Route>
        </Route>
      </Routes>
    </div>
  );
}

export default App;
