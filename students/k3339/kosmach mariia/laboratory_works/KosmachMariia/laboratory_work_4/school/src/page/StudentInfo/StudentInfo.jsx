import React, { useCallback, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Button from "react-bootstrap/Button";
import useUser from "../../hooks/useUser";
import Header from "../../components/Header";


function StudentInfo() {
    const [student, setStudent] = useState([]);
    const navigate = useNavigate();
    const { studentId } = useParams();
    const { token } = useUser();

    const onDelete = (student) => {
      fetch(`http://127.0.0.1:8000/api/students/delete/${student.id}/`, {
        method: "DELETE",
        headers: {
          Authorization: `Token ${token}`,
        },
      }).then(() => navigate(`/`));
    };
    
    const getStudents = useCallback(() => {

    }, [studentId,token]);
    useEffect(() => {fetch(`http://127.0.0.1:8000/api/students/${studentId}`,{
        method: "GET",
        headers: {
          Authorization: `Token ${token}`,
        },
      })
        .then(response => response.json())
        .then(data => {setStudent(data); console.log(data)})
        .catch(error => console.error('Ошибка:', error));}, [studentId, token, setStudent]);
  
    return (
      <div className="main-container container">
        <Header returnButton={true}/>
        <div>
          <h1 style={{marginTop: "40px"}}>Information about the student:</h1>
          <hr></hr>
          <div class="student-info" style={{fontSize: "20px"}}>
            <div class="student-info--id">
              <span style={{fontWeight: "600"}}>ID:</span> {student.id}
            </div>
            <div class="student-info--name">
              <span style={{fontWeight: "600"}}>Full name:</span> {student.FIO}
            </div>
            <div class="student-info--id">
              <span style={{fontWeight: "600"}}>Group ID:</span> {student.group}
            </div>
          </div>
          <h2 style={{marginTop: "40px"}}>Grades List:</h2>
          <hr></hr>
          <div class="grades-info">
          {student.grades_set?.map(grade => (
            //<li key={grade.id}>
            //  Оценка: {grade.grade}, Пропуск: {grade.attendance === null ? 'Не указан' : (grade.attendance ? 'Присутствовал' : 'Отсутствовал')}
            //</li>
            <div class="grade-info">
              <div class="grade-info--id">
                <span style={{fontWeight: "600"}}>ID:</span> {grade.id}
              </div>
              <div class="grade-info--id">
                <span style={{fontWeight: "600"}}>Grade:</span> {grade.grade}
              </div>
              <div class="grade-info--id">
                <span style={{fontWeight: "600"}}>Attendance:</span> {grade.attendance === null ? '❓' : (grade.attendance ? '✔️' : '❌')}
              </div>
              <hr></hr>
            </div>
          ))}
        </div>
        <div class="student-buttons" style={{display: "flex", justifyContent: "flex-end"}}>
          <Button
              onClick={() => onDelete(student)}
              variant="outline-danger"
            >
              ➖ Delete
          </Button>
        </div>
          {/* <h2>Расписание:</h2>
          <ul>
            {student.schedules.map(schedule => (
              <li key={schedule}>Расписание {schedule}</li>
            ))}
          </ul>  */}
        </div>
      </div>
    );
}

export default StudentInfo;