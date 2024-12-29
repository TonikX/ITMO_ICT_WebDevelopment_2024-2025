import React, { useState, useEffect } from "react";
import {
  Box,
  TextField,
  List,
  ListItemButton,
  Typography,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
} from "@mui/material";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";
import api from "../api/api";
import "../styles/Schedule.css";

interface IDoctor {
  doctorId: number;
  lastName: string;
  firstName: string;
  middleName?: string;
}

interface ISchedule {
  scheduleId?: number;
  date: string;
  isWorkingDay: boolean;
  shift?: string;
  doctorId: number;
  startTime: string;
  endTime: string;
}

const Schedule: React.FC = () => {
  const [doctors, setDoctors] = useState<IDoctor[]>([]);
  const [searchName, setSearchName] = useState("");
  const [filteredDoctors, setFilteredDoctors] = useState<IDoctor[]>([]);
  const [selectedDoctorId, setSelectedDoctorId] = useState<number | null>(null);

  const [schedules, setSchedules] = useState<ISchedule[]>([]);
  const [currentDate, setCurrentDate] = useState<Date>(new Date());

  const [dayDialogOpen, setDayDialogOpen] = useState(false);
  const [daySchedules, setDaySchedules] = useState<ISchedule[]>([]);
  const [clickedDate, setClickedDate] = useState<Date | null>(null);

  useEffect(() => {
    fetchDoctors();
  }, []);

  useEffect(() => {
    setFilteredDoctors(
      doctors.filter((doc) =>
        `${doc.lastName} ${doc.firstName} ${doc.middleName || ""}`
          .toLowerCase()
          .includes(searchName.toLowerCase())
      )
    );
  }, [searchName, doctors]);

  useEffect(() => {
    if (selectedDoctorId !== null) {
      fetchSchedules(selectedDoctorId);
    }
  }, [selectedDoctorId, currentDate]);

  const fetchDoctors = async () => {
    try {
      const res = await api.get<IDoctor[]>("/doctors/");
      setDoctors(res.data);
      setFilteredDoctors(res.data);
    } catch (error) {
      console.error("Failed to fetch doctors:", error);
    }
  };

  const fetchSchedules = async (doctorId: number) => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth() + 1;
    console.log(`API Request: /schedules/?doctorId=${doctorId}&year=${year}&month=${month}`);
    try {
      const res = await api.get<ISchedule[]>(
        `/schedules/?doctorId=${doctorId}&year=${year}&month=${month}`
      );
      console.log(`Fetched Schedules: `, res.data);
      setSchedules(res.data);
    } catch (error) {
      console.error("Failed to fetch schedules:", error);
    }
  };

  const handleDayClick = (value: Date) => {
    if (!selectedDoctorId) return;
    const dateString = value.toISOString().split("T")[0];
    const daySchedules = schedules.filter((s) => s.date === dateString);
    setDaySchedules(daySchedules);
    setClickedDate(value);
    setDayDialogOpen(true);
  };

  const tileClassName = ({ date, view }: { date: Date; view: string }) => {
    if (view === "month") {
      const dateString = date.toISOString().split("T")[0];
      const daySchedules = schedules.filter((s) => s.date === dateString);

      if (daySchedules.some((sched) => sched.isWorkingDay)) {
        return "working-day";
      } else if (daySchedules.length > 0) {
        return "non-working-day";
      }
    }
    return null;
  };

  return (
    <Box
      sx={{
        display: "flex",
        height: "calc(100vh - 64px)",
      }}
    >
      <Box sx={{ width: "300px", p: 2, borderRight: "1px solid #ccc" }}>
        <Typography variant="h6" gutterBottom>
          Doctors
        </Typography>
        <TextField
          label="Search Doctor"
          variant="outlined"
          fullWidth
          value={searchName}
          onChange={(e) => setSearchName(e.target.value)}
          sx={{ mb: 2 }}
        />
        <List dense sx={{ maxHeight: "70vh", overflow: "auto" }}>
          {filteredDoctors.map((doc) => (
            <ListItemButton
              key={doc.doctorId}
              selected={doc.doctorId === selectedDoctorId}
              onClick={() => setSelectedDoctorId(doc.doctorId)}
            >
              {doc.lastName} {doc.firstName} {doc.middleName}
            </ListItemButton>
          ))}
        </List>
      </Box>

      <Box
        sx={{
          flexGrow: 1,
          p: 2,
          display: "flex",
          justifyContent: "center",
          height: "80vh",
        }}
      >
        <Typography variant="h5" gutterBottom>
          Schedule Calendar
        </Typography>
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            width: "100%",
            height: "130%",
          }}
        >
          {selectedDoctorId ? (
            <Calendar
              value={currentDate}
              onClickDay={handleDayClick}
              tileClassName={tileClassName}
              className="bigCalendar"
            />
          ) : (
            <Typography variant="body1">
              Please select a doctor from the list to view the schedule.
            </Typography>
          )}
        </Box>
      </Box>

      <Dialog
        open={dayDialogOpen}
        onClose={() => setDayDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          Appointments on {clickedDate?.toLocaleDateString("en-US") || ""}
        </DialogTitle>
        <DialogContent dividers>
          {daySchedules.length > 0 ? (
            daySchedules.map((sched) => (
              <Box key={sched.scheduleId} sx={{ mb: 1 }}>
                <Typography>
                  <strong>Shift:</strong> {sched.shift || "No Shift"}
                </Typography>
                <Typography>
                  <strong>Working Day:</strong>{" "}
                  {sched.isWorkingDay ? "Yes" : "No"}
                </Typography>
              </Box>
            ))
          ) : (
            <Typography>No appointments found for this day.</Typography>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDayDialogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Schedule;
