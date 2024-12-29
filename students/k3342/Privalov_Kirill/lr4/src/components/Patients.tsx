import React, { useEffect, useState } from "react";
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  TextField,
  Select,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import api from "../api/api";
import MedicalCards from "./MedicalCards";

interface Patient {
  patientId: number;
  lastName: string;
  firstName: string;
  middleName?: string;
  gender: "M" | "F";
  dateOfBirth: string;
  phone?: string;
  address?: string;
}

const Patients: React.FC = () => {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [searchName, setSearchName] = useState("");
  const [searchPhone, setSearchPhone] = useState("");

  const [open, setOpen] = useState(false);
  const [newFirstName, setNewFirstName] = useState("");
  const [newLastName, setNewLastName] = useState("");
  const [newMiddleName, setNewMiddleName] = useState("");
  const [newPhone, setNewPhone] = useState("");
  const [newAddress, setNewAddress] = useState("");
  const [newDateOfBirth, setNewDateOfBirth] = useState("");
  const [newGender, setNewGender] = useState<"M" | "F" | "">("");
  const [ageError, setAgeError] = useState<string>("");

  const [editOpen, setEditOpen] = useState(false);
  const [currentPatient, setCurrentPatient] = useState<Patient | null>(null);
  const [editFirstName, setEditFirstName] = useState("");
  const [editLastName, setEditLastName] = useState("");
  const [editMiddleName, setEditMiddleName] = useState("");
  const [editPhone, setEditPhone] = useState("");
  const [editAddress, setEditAddress] = useState("");
  const [editGender, setEditGender] = useState<"M" | "F" | "">("");

  const [medicalCardsOpen, setMedicalCardsOpen] = useState(false);
  const [selectedPatientId, setSelectedPatientId] = useState<number | null>(null);

  const minDateOfBirth = (() => {
    const date = new Date();
    date.setFullYear(date.getFullYear() - 120);
    return date.toISOString().split("T")[0];
  })();

  const todayDate = new Date().toISOString().split("T")[0];

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = async () => {
    try {
      const res = await api.get<Patient[]>("/patients", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access")}`,
        },
      });
      setPatients(res.data);
    } catch (error) {
      console.error("Failed to fetch patients:", error);
    }
  };

  const filteredPatients = patients.filter((patient) => {
    const fullName = `${patient.lastName} ${patient.firstName} ${patient.middleName || ""}`.toLowerCase();
    const matchesName = fullName.includes(searchName.toLowerCase());
    const matchesPhone = searchPhone
      ? (patient.phone || "").toLowerCase().includes(searchPhone.toLowerCase())
      : true;
    return matchesName && matchesPhone
  });

  const handleOpen = () => setOpen(true);
  const handleClose = () => {
    setOpen(false);
    setAgeError("");
    resetNewPatientForm();
  };

  const resetNewPatientForm = () => {
    setNewFirstName("");
    setNewLastName("");
    setNewMiddleName("");
    setNewPhone("");
    setNewAddress("");
    setNewDateOfBirth("");
    setNewGender("");
  };

  const handleCreate = async () => {
    const maxDate = new Date();
    maxDate.setFullYear(maxDate.getFullYear() - 120);
    if (newDateOfBirth) {
      const dob = new Date(newDateOfBirth);
      if (dob > new Date()) {
        setAgeError("Date of Birth cannot be in the future.");
        return;
      }
      if (dob < maxDate) {
        setAgeError("Patient age cannot be older than 120 years.");
        return;
      }
    }

    setAgeError("");
    try {
      await api.post(
        "/patients/",
        {
          firstName: newFirstName,
          lastName: newLastName,
          middleName: newMiddleName,
          phone: newPhone,
          address: newAddress,
          dateOfBirth: newDateOfBirth,
          gender: newGender,
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access")}`,
          },
        }
      );
      handleClose();
      fetchPatients();
    } catch (error) {
      console.error("Failed to create patient:", error);
    }
  };

  const handleEditOpen = (patient: Patient) => {
    setCurrentPatient(patient);
    setEditFirstName(patient.firstName);
    setEditLastName(patient.lastName);
    setEditMiddleName(patient.middleName || "");
    setEditPhone(patient.phone || "");
    setEditAddress(patient.address || "");
    setEditGender(patient.gender);
    setEditOpen(true);
  };

  const handleEditClose = () => {
    setEditOpen(false);
    setCurrentPatient(null);
    setAgeError("");
    resetEditPatientForm();
  };

  const resetEditPatientForm = () => {
    setEditFirstName("");
    setEditLastName("");
    setEditMiddleName("");
    setEditPhone("");
    setEditAddress("");
    setEditGender("");
  };

  const handleEditSave = async () => {
    if (currentPatient) {
      const maxDate = new Date();
      maxDate.setFullYear(maxDate.getFullYear() - 120);
      if (currentPatient.dateOfBirth) {
        const dob = new Date(currentPatient.dateOfBirth);
        if (dob < maxDate) {
          setAgeError("Patient age cannot be older than 120 years.");
          return;
        }
      }

      setAgeError("");
      try {
        await api.put(
          `/patients/${currentPatient.patientId}/`,
          {
            firstName: editFirstName,
            lastName: editLastName,
            middleName: editMiddleName,
            phone: editPhone,
            address: editAddress,
            gender: editGender,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access")}`,
            },
          }
        );
        handleEditClose();
        fetchPatients();
      } catch (error) {
        console.error("Failed to edit patient:", error);
      }
    }
  };

  const handleDelete = async (patientId: number) => {
    if (window.confirm("Are you sure you want to delete this patient?")) {
      try {
        await api.delete(`/patients/${patientId}/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access")}`,
          },
        });
        setPatients(patients.filter((p) => p.patientId !== patientId));
      } catch (error) {
        console.error("Failed to delete patient:", error);
      }
    }
  };

  const handleViewMedicalCards = (patientId: number) => {
    setSelectedPatientId(patientId);
    setMedicalCardsOpen(true);
  };

  const handleMedicalCardsClose = () => {
    setMedicalCardsOpen(false);
    setSelectedPatientId(null);
  };

  return (
    <Container sx={{ mt: 4 }}>
      <Paper sx={{ p: 2 }}>
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            gap: 2,
            mb: 2,
          }}
        >
          <TextField
            label="Search Name"
            value={searchName}
            onChange={(e) => setSearchName(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            label="Search Phone"
            value={searchPhone}
            onChange={(e) => setSearchPhone(e.target.value)}
            sx={{ mb: 2 }}
          />
          <Button variant="outlined" onClick={handleOpen}>
            Create Patient
          </Button>
        </Box>
      </Paper>
      <Paper sx={{ mt: 2 }}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Id</TableCell>
                <TableCell>Last Name</TableCell>
                <TableCell>First Name</TableCell>
                <TableCell>Middle Name</TableCell>
                <TableCell>Phone</TableCell>
                <TableCell>Address</TableCell>
                <TableCell>Date of Birth</TableCell>
                <TableCell>Gender</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredPatients.map((p) => (
                <TableRow key={p.patientId}>
                  <TableCell>{p.patientId}</TableCell>
                  <TableCell>{p.lastName}</TableCell>
                  <TableCell>{p.firstName}</TableCell>
                  <TableCell>{p.middleName || ""}</TableCell>
                  <TableCell>{p.phone || ""}</TableCell>
                  <TableCell>{p.address || ""}</TableCell>
                  <TableCell>{p.dateOfBirth || ""}</TableCell>
                  <TableCell>{p.gender || ""}</TableCell>
                  <TableCell>
                    <Button
                      variant="outlined"
                      onClick={() => handleEditOpen(p)}
                      sx={{ mr: 1 }}
                    >
                      Edit
                    </Button>
                    <Button
                      variant="outlined"
                      color="error"
                      onClick={() => handleDelete(p.patientId)}
                      sx={{ mr: 1 }}
                    >
                      Delete
                    </Button>
                    <Button
                      variant="outlined"
                      onClick={() => handleViewMedicalCards(p.patientId)}
                    >
                      View Medical Cards
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
              {filteredPatients.length === 0 && (
                <TableRow>
                  <TableCell colSpan={9} align="center">
                    No patients found.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* Create Patient Dialog */}
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Create New Patient</DialogTitle>
        <DialogContent>
          {ageError && <Typography color="error">{ageError}</Typography>}
          <TextField
            autoFocus
            margin="dense"
            label="First Name"
            fullWidth
            value={newFirstName}
            onChange={(e) => setNewFirstName(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Last Name"
            fullWidth
            value={newLastName}
            onChange={(e) => setNewLastName(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Middle Name"
            fullWidth
            value={newMiddleName}
            onChange={(e) => setNewMiddleName(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Address"
            fullWidth
            value={newAddress}
            onChange={(e) => setNewAddress(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            label="Date of Birth"
            type="date"
            value={newDateOfBirth}
            fullWidth
            onChange={(e) => setNewDateOfBirth(e.target.value)}
            inputProps={{ min: minDateOfBirth, max: todayDate }}
            sx={{ mb: 2 }}
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            label="Gender"
            select
            SelectProps={{ native: true }}
            value={newGender}
            onChange={(e) => setNewGender(e.target.value as "M" | "F" | "")}
            fullWidth
            sx={{ mb: 2 }}
          >
            <option value=""></option>
            <option value="M">M</option>
            <option value="F">F</option>
          </TextField>
          <TextField
            margin="dense"
            label="Phone"
            fullWidth
            value={newPhone}
            onChange={(e) => setNewPhone(e.target.value)}
            sx={{ mb: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleCreate} variant="contained">
            Create
          </Button>
        </DialogActions>
      </Dialog>

      {/* Edit Patient Dialog */}
      <Dialog open={editOpen} onClose={handleEditClose}>
        <DialogTitle>Edit Patient</DialogTitle>
        <DialogContent>
          {ageError && <Typography color="error">{ageError}</Typography>}
          <TextField
            autoFocus
            margin="dense"
            label="First Name"
            fullWidth
            value={editFirstName}
            onChange={(e) => setEditFirstName(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Last Name"
            fullWidth
            value={editLastName}
            onChange={(e) => setEditLastName(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Middle Name"
            fullWidth
            value={editMiddleName}
            onChange={(e) => setEditMiddleName(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Address"
            fullWidth
            value={editAddress}
            onChange={(e) => setEditAddress(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            label="Date of Birth"
            type="date"
            value={currentPatient?.dateOfBirth || ""}
            fullWidth
            InputProps={{
              readOnly: true,
            }}
            sx={{ mb: 2 }}
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            label="Gender"
            select
            SelectProps={{ native: true }}
            value={editGender}
            onChange={(e) => setEditGender(e.target.value as "M" | "F" | "")}
            fullWidth
            sx={{ mb: 2 }}
          >
            <option value=""></option>
            <option value="M">M</option>
            <option value="F">F</option>
          </TextField>
          <TextField
            margin="dense"
            label="Phone"
            fullWidth
            value={editPhone}
            onChange={(e) => setEditPhone(e.target.value)}
            sx={{ mb: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleEditClose}>Cancel</Button>
          <Button onClick={handleEditSave} variant="contained">
            Save
          </Button>
        </DialogActions>
      </Dialog>

      {selectedPatientId && (
        <MedicalCards
          patientId={selectedPatientId}
          onClose={handleMedicalCardsClose}
        />
      )}
    </Container>
  );
}

export default Patients;