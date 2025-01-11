import React, { useCallback, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Button from "react-bootstrap/Button";
import useUser from "../../hooks/useUser";
import Grades from "./Grades";


function GradesList() {
  const navigate = useNavigate();
  const { token } = useUser();
  const [grades, setGrades] = useState([]);

  const getGrades = useCallback(() => {
    fetch("http://localhost:8000/api/grades/all/", {
      method: "GET",
      headers: {
        Authorization: `Token ${token}`,
      },
    })
      .then((response) => response.json())
      .then((result) => {
        setGrades(result);
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, [token]);

  useEffect(() => getGrades(), [getGrades]);

  return (
    <div>
      {grades ? (
        <>
          <div className="grades-group">
            {grades.map((grade, id) => (
              <div>
                <Grades grade={grade} getGrades={getGrades} key={id} />
                <hr></hr>
              </div>
            ))}
          </div>
          <div class="grades-buttons" style={{display: "flex", "justifyContent": "flex-end"}}>
            <Button
              onClick={() => navigate("/grades/create")}
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

export default GradesList;