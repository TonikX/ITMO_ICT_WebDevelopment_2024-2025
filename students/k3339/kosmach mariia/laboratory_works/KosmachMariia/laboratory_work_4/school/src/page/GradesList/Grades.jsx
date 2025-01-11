import React, { useCallback, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Button from "react-bootstrap/Button";
import useUser from "../../hooks/useUser";


function Grades({ grade, getGrades }) {
  const navigate = useNavigate();
  const { token } = useUser();
  const [routeData, setRouteData] = useState("");

  const onDelete = (grade) => {
    fetch(`http://127.0.0.1:8000/api/grades/delete/${grade.id}/`, {
      method: "DELETE",
      headers: {
        Authorization: `Token ${token}`,
      },
    }).then(() => getGrades());
  };

  return (
    <div className="grade" style={{display: "flex", justifyContent: "space-between", alignItems: "center"}}>
      <div class="grade-info">
        <div class="grade-info--id">
          <span style={{fontWeight: "600"}}>ID:</span> {grade.id}
        </div>
        <div class="grade-info--grade">
          <span style={{fontWeight: "600"}}>Grade:</span> {grade.grade}
        </div>
        <div class="grade-info--student">
          <span style={{fontWeight: "600"}}>Student ID:</span> {grade.student}
        </div>
        <div class="grade-info--id">
          <span style={{fontWeight: "600"}}>Schedule ID:</span> {grade.schedule}
        </div>
      </div>
      <div className="grade-route">
        <div>{routeData.destination_point}</div>
      </div>
      <div className="grade-buttons">
        {/* <btn
          className="cell-button"
          onClick={() => navigate(`student/edit/${student.id}`)}
        /> */}

        <Button
            onClick={() => navigate(`grade/update/${grade.id}`)}
            variant="outline-info"
          >
            ✏️ Edit
          </Button>

        <Button
            onClick={() => onDelete(grade)}
            variant="outline-danger"
            style={{marginLeft: "20px"}}
          >
            ➖ Delete
          </Button>
      </div>
    </div>
  );
}

export default Grades;