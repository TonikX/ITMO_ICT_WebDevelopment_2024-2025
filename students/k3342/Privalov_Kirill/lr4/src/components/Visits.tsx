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
  FormControl,
  InputLabel,
} from "@mui/material";
import { DatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { format, isSameDay } from "date-fns";
import api from "../api/api";

interface IVisit {
  visitId: number;
  visitDate: string;
  visitTime: string;
  patient: IPatient;
  doctor: IDoctor;
  officeId?: number | null;
  currentConditionNotes?: string;
  visitStatus: "Scheduled" | "Completed" | "Canceled";
}

interface IPatient {
  patientId: number;
  firstName: string;
  lastName: string;
  middleName?: string;
  gender: string;
  dateOfBirth: string;
  phone?: string;
  address?: string;
}

interface IDoctor {
  doctorId: number;
  firstName: string;
  lastName: string;
  middleName?: string;
  position: IPosition;
  gender: string;
  dateOfBirth: string;
  education?: string;
}

interface IPosition {
  positionId: number;
  title: string;
  category: string;
  salary: string;
}

interface ISchedule {
  scheduleId: number;
  date: string;
  isWorkingDay: boolean;
  shift: string;
  doctorId: number;
  startTime: string;
  endTime: string;
}

const Visits: React.FC = () => {
  const [visits, setVisits] = useState<IVisit[]>([]);
  const [patients, setPatients] = useState<IPatient[]>([]);
  const [doctors, setDoctors] = useState<IDoctor[]>([]);
  const [schedules, setSchedules] = useState<ISchedule[]>([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [currentVisit, setCurrentVisit] = useState<IVisit | null>(null);
  const [formData, setFormData] = useState({
    visitDate: "",
    visitTime: "",
    patientId: "",
    doctorId: "",
    visitStatus: "Scheduled" as "Scheduled" | "Completed" | "Canceled",
    currentConditionNotes: "",
  });
  const [availableTimes, setAvailableTimes] = useState<string[]>([]);
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [doctorNameSearch, setDoctorNameSearch] = useState<string>("");
  const [patientNameSearch, setPatientNameSearch] = useState<string>("");

  useEffect(() => {
    fetchVisits();
    fetchPatients();
    fetchDoctors();
  }, []);

  useEffect(() => {
    if (formData.doctorId) {
      fetchSchedules(parseInt(formData.doctorId));
    } else {
      setSchedules([]);
    }
  }, [formData.doctorId]);

  useEffect(() => {
    if (selectedDate && formData.doctorId) {
      generateAvailableTimes(selectedDate, parseInt(formData.doctorId), currentVisit?.visitId);
    } else {
      setAvailableTimes([]);
    }
  }, [selectedDate, formData.doctorId, visits]);

  const fetchVisits = async () => {
    try {
      const res = await api.get<IVisit[]>("/visits/", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access")}`,
        },
      });
      setVisits(res.data);
    } catch (err) {
      console.error("Failed to fetch visits:", err);
    }
  };

  const fetchPatients = async () => {
    try {
      const res = await api.get<IPatient[]>("/patients/");
      setPatients(res.data);
    } catch (err) {
      console.error("Error fetching patients:", err);
    }
  };

  const fetchDoctors = async () => {
    try {
      const res = await api.get<IDoctor[]>("/doctors/");
      setDoctors(res.data);
    } catch (err) {
      console.error("Error fetching doctors:", err);
    }
  };

  const fetchSchedules = async (doctorId: number) => {
    try {
      const res = await api.get<ISchedule[]>("/schedules/", {
        params: { doctorId: doctorId },
      });
      setSchedules(res.data.filter((s) => s.isWorkingDay));
    } catch (err) {
      console.error("Error fetching schedules:", err);
    }
  };

  const generateAvailableTimes = (date: Date, doctorId: number, currentVisitId?: number) => {
    const schedule = schedules.find((s) =>
      isSameDay(new Date(s.date), date)
    );
    if (!schedule) {
      setAvailableTimes([]);
      return;
    }

    const [startHour, startMinute] = schedule.startTime.split(":").map(Number);
    const [endHour, endMinute] = schedule.endTime.split(":").map(Number);
    const startDate = new Date(date);
    startDate.setHours(startHour, startMinute, 0, 0);
    const endDate = new Date(date);
    endDate.setHours(endHour, endMinute, 0, 0);

    const times: string[] = [];
    let current = new Date(startDate);
    while (current < endDate) {
      const timeStr = format(current, "HH:mm");
      const isBooked = visits.some(
        (visit) =>
          visit.doctor.doctorId === doctorId &&
          visit.visitDate === format(date, "yyyy-MM-dd") &&
          visit.visitTime === `${timeStr}:00` &&
          visit.visitStatus !== "Canceled" &&
          (currentVisitId ? visit.visitId !== currentVisitId : true)
      );
      if (!isBooked) {
        times.push(timeStr);
      }
      current.setHours(current.getHours() + 1);
    }
    setAvailableTimes(times);
  };

  const handleOpenDialog = (visit?: IVisit) => {
    if (visit) {
      setCurrentVisit(visit);
      setFormData({
        visitDate: visit.visitDate,
        visitTime: visit.visitTime.slice(0, 5),
        patientId: visit.patient.patientId.toString(),
        doctorId: visit.doctor.doctorId.toString(),
        visitStatus: visit.visitStatus,
        currentConditionNotes: visit.currentConditionNotes || "",
      });
      setSelectedDate(new Date(visit.visitDate));
      generateAvailableTimes(new Date(visit.visitDate), visit.doctor.doctorId, visit.visitId);
    } else {
      setCurrentVisit(null);
      setFormData({
        visitDate: "",
        visitTime: "",
        patientId: "",
        doctorId: "",
        visitStatus: "Scheduled",
        currentConditionNotes: "",
      });
      setSelectedDate(null);
      setAvailableTimes([]);
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setCurrentVisit(null);
    setSelectedDate(null);
    setAvailableTimes([]);
    setIsSubmitting(false);
  };

  const handleSubmit = async () => {
    if (
      !formData.visitDate ||
      !formData.visitTime ||
      !formData.patientId ||
      !formData.doctorId
    ) {
      alert("Please fill in all required fields.");
      return;
    }

    const isStillBooked = visits.some(
      (visit) =>
        visit.doctor.doctorId === parseInt(formData.doctorId) &&
        visit.visitDate === formData.visitDate &&
        visit.visitTime === `${formData.visitTime}:00` &&
        visit.visitStatus !== "Canceled" &&
        (currentVisit ? visit.visitId !== currentVisit.visitId : true)
    );

    if (isStillBooked) {
      alert(
        "The selected time slot has just been booked by another user. Please choose a different time."
      );
      if (selectedDate) {
        generateAvailableTimes(
          selectedDate,
          parseInt(formData.doctorId),
          currentVisit?.visitId
        );
      }
      return;
    }

    setIsSubmitting(true);

    try {
      if (currentVisit) {
        await api.put(`/visits/${currentVisit.visitId}/`, {
          visitDate: formData.visitDate,
          visitTime: `${formData.visitTime}:00`,
          patientId: parseInt(formData.patientId),
          doctorId: parseInt(formData.doctorId),
          visitStatus: formData.visitStatus,
          currentConditionNotes: formData.currentConditionNotes,
          officeId: currentVisit.officeId,
        });
      } else {
        await api.post("/visits/", {
          visitDate: formData.visitDate,
          visitTime: `${formData.visitTime}:00`,
          patientId: parseInt(formData.patientId),
          doctorId: parseInt(formData.doctorId),
          visitStatus: formData.visitStatus,
          currentConditionNotes: formData.currentConditionNotes,
          officeId: null,
        });
      }
      await fetchVisits();
      handleCloseDialog();
    } catch (err: any) {
      console.error("Error submitting visit", err);
      if (err.response && err.response.data && err.response.data.message) {
        alert(err.response.data.message);
      } else {
        alert(
          "An error occurred while submitting the visit. Please try again."
        );
      }
      setIsSubmitting(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await api.delete(`/visits/${id}/`);
      fetchVisits();
    } catch (err) {
      console.error("Error deleting visit", err);
    }
  };

  const isDateDisabled = (date: Date) => {
    return !schedules.some((schedule) =>
      isSameDay(new Date(schedule.date), date)
    );
  };

  const filteredVisits = visits.filter((visit) => {
    const doctor = doctors.find(d => d.doctorId === visit.doctor.doctorId);
    const patient = patients.find(p => p.patientId === visit.patient.patientId);

    const matchesDoctorName = doctorNameSearch
      ? `${doctor?.firstName} ${doctor?.lastName}`
          .toLowerCase()
          .includes(doctorNameSearch.toLowerCase())
      : true;
    const matchesPatientName = patientNameSearch
      ? `${patient?.firstName} ${patient?.lastName}`
          .toLowerCase()
          .includes(patientNameSearch.toLowerCase())
      : true;

    return matchesDoctorName && matchesPatientName;
  });

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Manage Visits
      </Typography>

      <Box sx={{ display: "flex", flexWrap: "wrap", gap: 2, mb: 2 }}>
        <TextField
          label="Search Doctor Name"
          variant="outlined"
          value={doctorNameSearch}
          onChange={(e) => setDoctorNameSearch(e.target.value)}
          sx={{ minWidth: 200 }}
        />

        <TextField
          label="Search Patient Name"
          variant="outlined"
          value={patientNameSearch}
          onChange={(e) => setPatientNameSearch(e.target.value)}
          sx={{ minWidth: 200 }}
        />
      </Box>

      <Button
        variant="contained"
        color="primary"
        onClick={() => handleOpenDialog()}
        disabled={isSubmitting}
      >
        Book Visit
      </Button>

      <TableContainer component={Paper} sx={{ mt: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Visit Date</TableCell>
              <TableCell>Visit Time</TableCell>
              <TableCell>Patient</TableCell>
              <TableCell>Doctor</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredVisits.map((visit) => (
              <TableRow key={visit.visitId}>
                <TableCell>{visit.visitDate}</TableCell>
                <TableCell>{visit.visitTime.slice(0, 5)}</TableCell>
                <TableCell>
                  {visit.patient
                    ? `${visit.patient.firstName} ${visit.patient.lastName}`
                    : "N/A"}
                </TableCell>
                <TableCell>
                  {visit.doctor
                    ? `Dr. ${visit.doctor.firstName} ${visit.doctor.lastName}`
                    : "N/A"}
                </TableCell>
                <TableCell>{visit.visitStatus}</TableCell>
                <TableCell>
                  <Button onClick={() => handleOpenDialog(visit)}>
                    Edit
                  </Button>
                  <Button
                    color="error"
                    onClick={() => handleDelete(visit.visitId)}
                  >
                    Cancel
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog
        open={openDialog}
        onClose={handleCloseDialog}
        fullWidth
        maxWidth="sm"
      >
        <DialogTitle>{currentVisit ? "Edit Visit" : "Book Visit"}</DialogTitle>
        <DialogContent>
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}>
            <FormControl fullWidth>
              <InputLabel id="doctor-label">Doctor</InputLabel>
              <Select
                labelId="doctor-label"
                value={formData.doctorId}
                label="Doctor"
                onChange={(e) =>
                  setFormData({ ...formData, doctorId: e.target.value })
                }
                disabled={isSubmitting}
              >
                <MenuItem value="">
                  <em>Select Doctor</em>
                </MenuItem>
                {doctors.map((doctor) => (
                  <MenuItem key={doctor.doctorId} value={doctor.doctorId}>
                    Dr. {doctor.firstName} {doctor.lastName}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <LocalizationProvider dateAdapter={AdapterDateFns}>
              <DatePicker
                label="Visit Date"
                value={selectedDate}
                onChange={(newDate: Date | null) => {
                  setSelectedDate(newDate);
                  if (newDate) {
                    setFormData({
                      ...formData,
                      visitDate: format(newDate, "yyyy-MM-dd"),
                      visitTime: "",
                    });
                    generateAvailableTimes(newDate, parseInt(formData.doctorId), currentVisit?.visitId);
                  } else {
                    setFormData({ ...formData, visitDate: "", visitTime: "" });
                    setAvailableTimes([]);
                  }
                }}
                shouldDisableDate={isDateDisabled}
                // @ts-ignore
                renderInput={(params) => <TextField {...params} />}
                disabled={isSubmitting}
              />
            </LocalizationProvider>

            <FormControl fullWidth>
              <InputLabel id="timeslot-label">Visit Time</InputLabel>
              <Select
                labelId="timeslot-label"
                value={formData.visitTime}
                label="Visit Time"
                onChange={(e) =>
                  setFormData({ ...formData, visitTime: e.target.value })
                }
                disabled={isSubmitting || availableTimes.length === 0}
              >
                <MenuItem value="">
                  <em>Select Time</em>
                </MenuItem>
                {availableTimes.length > 0 ? (
                  availableTimes.map((time) => (
                    <MenuItem key={time} value={time}>
                      {time}
                    </MenuItem>
                  ))
                ) : (
                  <MenuItem value="" disabled>
                    No Available Times
                  </MenuItem>
                )}
              </Select>
            </FormControl>

            <FormControl fullWidth>
              <InputLabel id="patient-label">Patient</InputLabel>
              <Select
                labelId="patient-label"
                value={formData.patientId}
                label="Patient"
                onChange={(e) =>
                  setFormData({ ...formData, patientId: e.target.value })
                }
                disabled={isSubmitting}
              >
                <MenuItem value="">
                  <em>Select Patient</em>
                </MenuItem>
                {patients.map((patient) => (
                  <MenuItem key={patient.patientId} value={patient.patientId}>
                    {patient.firstName} {patient.lastName}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl fullWidth>
              <InputLabel id="status-label">Status</InputLabel>
              <Select
                labelId="status-label"
                value={formData.visitStatus}
                label="Status"
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    visitStatus: e.target.value as
                      | "Scheduled"
                      | "Completed"
                      | "Canceled",
                  })
                }
                disabled={isSubmitting}
              >
                <MenuItem value="Scheduled">Scheduled</MenuItem>
                <MenuItem value="Completed">Completed</MenuItem>
                <MenuItem value="Canceled">Canceled</MenuItem>
              </Select>
            </FormControl>

            <TextField
              label="Current Condition Notes"
              variant="outlined"
              multiline
              rows={4}
              value={formData.currentConditionNotes}
              onChange={(e) =>
                setFormData({ ...formData, currentConditionNotes: e.target.value })
              }
              disabled={isSubmitting}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog} disabled={isSubmitting}>
            Cancel
          </Button>
          <Button
            variant="contained"
            onClick={handleSubmit}
            disabled={isSubmitting || availableTimes.length === 0}
          >
            {isSubmitting
              ? currentVisit
                ? "Updating..."
                : "Booking..."
              : currentVisit
              ? "Update"
              : "Book"}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Visits;