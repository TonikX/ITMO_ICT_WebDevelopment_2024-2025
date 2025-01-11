import React, { useCallback, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Button from "react-bootstrap/Button";
import useUser from "../../hooks/useUser";
import Student from "./Student";
import Header from "../../components/Header";


function StudentList() {
  const navigate = useNavigate();
  const { token } = useUser();
  const [students, setStudents] = useState([]);

  const getStudents = useCallback(() => {
    fetch("http://localhost:8000/api/students/all/", {
      method: "GET",
      headers: {
        Authorization: `Token ${token}`,
      },
    })
      .then((response) => response.json())
      .then((result) => {
        setStudents(result);
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, [token]);

  useEffect(() => getStudents(), [getStudents]);

  return (
    <div>
      {students ? (
        <>
          <div className="students-group">
            {students.map((student, id) => (
              <div>
                <Student student={student} getStudents={getStudents} key={id} />
                <hr></hr>
              </div>
            ))}
          </div>
          <div class="students-buttons" style={{display: "flex", "justifyContent": "flex-end"}}>
            <Button
              onClick={() => navigate("/students/create")}
              variant="outline-primary"
            >
              ➕ Add
            </Button>
          </div>
        </>
      ) : (
        <></>
      )}
    </div>
  );
}

export default StudentList;