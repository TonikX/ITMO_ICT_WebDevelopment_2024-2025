import React, { useEffect, useState } from "react";
import useUser from "../../hooks/useUser";
import { useNavigate } from "react-router-dom";
import { Form, Button, Row, Col } from "react-bootstrap";
import Header from "../../components/Header";


function StudentForm() {
  const { setToken, token } = useUser();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    FIO: "",
    group: null,

  });

  const [availableClasses, setAvailableClasses] = useState([]);


  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/classes/all", {
      method: "GET",
      headers: {
        Authorization: `Token ${token}`,
      },
    })
      .then((response) => response.json())
      .then((result) => {
        setAvailableClasses(result);
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, [token]);

  const handleChange = (event) => {
    const { name, value } = event.target;

    if (name === "class") {
      const selectedValues = Array.from(
        event.target.selectedOptions,
        (option) => option.value
      );

      setFormData({
        ...formData,
        [name]: selectedValues,
      });
    } else {
      setFormData({
        ...formData,
        [name]: value,
      });
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log("Form submitted:", formData);
    fetch("http://127.0.0.1:8000/api/students/create/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((result) => {
        console.log("Success:", result);
        navigate("/");
      })
      .catch((error) => console.error("Error:", error));
  };

  return (
    <div className="container mt-4">
      <Header returnButton={true}/>
      <h1 style={{marginTop: "40px"}}>➕ Adding a student:</h1>
      <hr></hr>
      <Form onSubmit={handleSubmit}>
        <Row className="mb-3">
            <Form.Group controlId="student">
                <Form.Label style={{fontWeight: '600', fontSize: '20px'}}>Full Name:</Form.Label>
                        <Form.Control
                    type="text"
                    name="FIO"
                    value={formData.FIO}
                    onChange={handleChange}
                />
            </Form.Group>
        </Row>

        <Form.Group controlId="group">
          <Form.Label style={{fontWeight: '600', fontSize: '20px'}}>Group:</Form.Label>
          <Form.Select
            name="group"
            value={formData.group}
            onChange={handleChange}
          >
            <option value="">Select a group</option>
            {availableClasses.map((group) => (
              <option key={group.id} value={group.id}>
                {group.year}  {group.litera}
              </option>
            ))}
          </Form.Select>
        </Form.Group>

        <Button variant="outline-success" type="submit" style={{marginTop: "20px"}}>
        ➕ Save
        </Button>
      </Form>
    </div>
  );
}

export default StudentForm;