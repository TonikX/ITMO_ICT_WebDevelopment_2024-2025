import React, { useCallback, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Button from "react-bootstrap/Button";
import useUser from "../../hooks/useUser";


function Student({ student, getStudents }) {
  const navigate = useNavigate();
  const { token } = useUser();
  const [routeData, setRouteData] = useState("");

  return (
    <div className="student" style={{display: "flex", justifyContent: "space-between", alignItems: "center"}}>
      <div class="student-info">
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
      <div className="student-route">
        <div>{routeData.destination_point}</div>
      </div>
      <div className="student-buttons">
        {/* <btn
          className="cell-button"
          onClick={() => navigate(`student/edit/${student.id}`)}
        /> */}
        <Button
            onClick={() => navigate(`student/info/${student.id}`)}
            variant="outline-primary"
          >
            👁️ View
          </Button>
          <span class="divider"></span>
      </div>
    </div>
  );
}

export default Student;