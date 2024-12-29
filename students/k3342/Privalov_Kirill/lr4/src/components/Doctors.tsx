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
  Checkbox,
  FormControlLabel,
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
  IconButton,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Schedule as ScheduleIcon,
  Work as ContractIcon,
} from "@mui/icons-material";
import api from "../api/api";

interface IPosition {
  positionId: number;
  title: string;
  category?: string;
  salary: string;
}

interface IDoctor {
  doctorId: number;
  position: IPosition | null;
  lastName: string;
  firstName: string;
  middleName?: string;
  gender: "M" | "F";
  dateOfBirth: string;
  education?: string;
}

interface ISchedule {
  scheduleId: number;
  date: string;
  isWorkingDay: boolean;
  shift?: string;
  doctorId: number;
  startTime: string;
  endTime: string;
}

interface ILaborContract {
  contractId: number;
  startDate: string;
  endDate?: string;
  contractDetails?: string;
  doctorId: number;
}

const Doctors: React.FC = () => {
  const [doctors, setDoctors] = useState<IDoctor[]>([]);
  const [positions, setPositions] = useState<IPosition[]>([]);
  const [schedules, setSchedules] = useState<ISchedule[]>([]);
  const [laborContracts, setLaborContracts] = useState<ILaborContract[]>([]);
  const [selectedDoctor, setSelectedDoctor] = useState<IDoctor | null>(null);
  const [searchName, setSearchName] = useState("");
  const [specializationFilter, setSpecializationFilter] = useState("");

  const [openCreateDialog, setOpenCreateDialog] = useState(false);
  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [openScheduleDialog, setOpenScheduleDialog] = useState(false);
  const [openContractsDialog, setOpenContractsDialog] = useState(false);
  const [openDeleteConfirm, setOpenDeleteConfirm] = useState(false);

  const [doctorCreateForm, setDoctorCreateForm] = useState<Omit<IDoctor, "doctorId" | "position">>({
    lastName: "",
    firstName: "",
    middleName: "",
    gender: "M",
    dateOfBirth: "",
    education: "",
  });

  const [doctorEditForm, setDoctorEditForm] = useState<Omit<IDoctor, "doctorId" | "position">>({
    lastName: "",
    firstName: "",
    middleName: "",
    gender: "M",
    dateOfBirth: "",
    education: "",
  });

  const [selectedPositionTitleCreate, setSelectedPositionTitleCreate] = useState<string>("");
  const [selectedPositionTitleEdit, setSelectedPositionTitleEdit] = useState<string>("");

  const [scheduleForm, setScheduleForm] = useState<Omit<ISchedule, "scheduleId">>({
    date: "",
    isWorkingDay: true,
    shift: "",
    doctorId: 0,
    startTime: "",
    endTime: "",
  });

  const [contractForm, setContractForm] = useState<Omit<ILaborContract, "contractId">>({
    startDate: "",
    endDate: "",
    contractDetails: "",
    doctorId: 0,
  });

  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));

  const [selectedLaborContract, setSelectedLaborContract] = useState<ILaborContract | null>(null);
  const [isEditLaborContractDialogOpen, setIsEditLaborContractDialogOpen] = useState(false);

  const [selectedSchedule, setSelectedSchedule] = useState<ISchedule | null>(null);
  const [isEditScheduleDialogOpen, setIsEditScheduleDialogOpen] = useState(false);

  useEffect(() => {
    fetchDoctors();
    fetchPositions();
  }, []);

  const fetchDoctors = async () => {
    try {
      const res = await api.get<IDoctor[]>("/doctors/");
      setDoctors(res.data);
    } catch (err) {
      console.error("Error fetching doctors", err);
    }
  };

  const fetchPositions = async () => {
    try {
      const res = await api.get<IPosition[]>("/positions/");
      setPositions(res.data);
    } catch (err) {
      console.error("Error fetching positions", err);
    }
  };

  const fetchSchedulesForDoctor = async (doctorId: number) => {
    try {
      const res = await api.get<ISchedule[]>(`/schedules/?doctorId=${doctorId}`);
      setSchedules(res.data);
    } catch (err) {
      console.error("Error fetching schedules", err);
    }
  };

  const fetchLaborContractsForDoctor = async (doctorId: number) => {
    try {
      const res = await api.get<ILaborContract[]>(`/laborcontracts/?doctorId=${doctorId}`);
      setLaborContracts(res.data);
    } catch (err) {
      console.error("Error fetching labor contracts", err);
    }
  };

  const handleSelectDoctor = (doctor: IDoctor) => {
    setSelectedDoctor(doctor);
    setDoctorEditForm({ 
      lastName: doctor.lastName,
      firstName: doctor.firstName,
      middleName: doctor.middleName || "",
      gender: doctor.gender,
      dateOfBirth: doctor.dateOfBirth,
      education: doctor.education || "",
    });
    if (doctor.doctorId) {
      fetchSchedulesForDoctor(doctor.doctorId);
      fetchLaborContractsForDoctor(doctor.doctorId);
    }
    setOpenEditDialog(true);
  };

  const handleOpenCreateDialog = () => {
    setDoctorCreateForm({
      lastName: "",
      firstName: "",
      middleName: "",
      gender: "M",
      dateOfBirth: "",
      education: "",
    });
    setSelectedPositionTitleCreate("");
    setOpenCreateDialog(true);
  };

  const handleCloseCreateDialog = () => {
    setOpenCreateDialog(false);
  };

  const handleCreateDoctor = async () => {
    try {
      let finalPositionId: number | undefined;
      if (selectedPositionTitleCreate) {
        const foundPos = positions.find((p) => p.title === selectedPositionTitleCreate);
        if (foundPos) {
          finalPositionId = foundPos.positionId;
        }
      }

      await api.post("/doctors/", {
        ...doctorCreateForm,
        positionId: finalPositionId,
      });

      fetchDoctors();
      handleCloseCreateDialog();
    } catch (err) {
      console.error("Error creating doctor", err);
    }
  };

  const handleCloseEditDialog = () => {
    setOpenEditDialog(false);
    setSelectedDoctor(null);
  };

  const handleEditDoctor = async () => {
    if (!selectedDoctor?.doctorId) return;
    try {
      let finalPositionId: number | undefined;
      if (selectedPositionTitleEdit) {
        const foundPos = positions.find((p) => p.title === selectedPositionTitleEdit);
        if (foundPos) {
          finalPositionId = foundPos.positionId;
        }
      }
      await api.patch(`/doctors/${selectedDoctor.doctorId}/`, {
        ...doctorEditForm,
        positionId: finalPositionId ?? selectedDoctor.position?.positionId,
      });

      fetchDoctors();
      handleCloseEditDialog();
    } catch (err) {
      console.error("Error editing doctor", err);
    }
  };

  const handleDeleteDoctor = async () => {
    if (!selectedDoctor?.doctorId) return;
    try {
      await api.delete(`/doctors/${selectedDoctor.doctorId}/`);
      fetchDoctors();
      setSelectedDoctor(null);
      setOpenDeleteConfirm(false);
    } catch (err) {
      console.error("Error deleting doctor", err);
    }
  };

  const handleCreateSchedule = async () => {
    if (!selectedDoctor?.doctorId) return;
    try {
      await api.post("/schedules/", {
        ...scheduleForm,
        doctorId: selectedDoctor.doctorId, 
      });
      fetchSchedulesForDoctor(selectedDoctor.doctorId);
      setScheduleForm({
        date: "",
        isWorkingDay: true,
        shift: "",
        doctorId: selectedDoctor.doctorId,
        startTime: "",
        endTime: "",
      });
    } catch (err) {
      console.error("Error creating schedule", err);
    }
  };

  const handleEditSchedule = async () => {
    if (!selectedSchedule) return;
    try {
      await api.put(`/schedules/${selectedSchedule.scheduleId}/`, selectedSchedule);
      if (selectedDoctor?.doctorId) {
        fetchSchedulesForDoctor(selectedDoctor.doctorId);
      }
      setIsEditScheduleDialogOpen(false);
      setSelectedSchedule(null);
    } catch (err) {
      console.error("Error editing schedule", err);
    }
  };

  const handleDeleteSchedule = async (scheduleId: number) => {
    try {
      await api.delete(`/schedules/${scheduleId}/`);
      if (selectedDoctor?.doctorId) {
        fetchSchedulesForDoctor(selectedDoctor.doctorId);
      }
    } catch (err) {
      console.error("Error deleting schedule", err);
    }
  };

  const handleCreateLaborContract = async () => {
    if (!selectedDoctor?.doctorId) return;
    try {
      await api.post("/laborcontracts/", {
        ...contractForm,
        doctorId: selectedDoctor.doctorId,
      });
      fetchLaborContractsForDoctor(selectedDoctor.doctorId);
      setContractForm({
        startDate: "",
        endDate: "",
        contractDetails: "",
        doctorId: selectedDoctor.doctorId,
      });
    } catch (err) {
      console.error("Error creating labor contract", err);
    }
  };

    const handleEditLaborContract = async () => {
    if (!selectedLaborContract || !selectedDoctor?.doctorId) return;
    try {
      const { contractId, startDate, endDate, contractDetails } = selectedLaborContract;
      await api.put(`/laborcontracts/${contractId}/`, {
        doctorId: selectedDoctor.doctorId, 
        startDate,
        endDate,
        contractDetails,
      });
      fetchLaborContractsForDoctor(selectedDoctor.doctorId);
      setIsEditLaborContractDialogOpen(false);
      setSelectedLaborContract(null);
    } catch (err) {
      console.error("Error editing labor contract", err);
    }
  };

  const handleDeleteLaborContract = async (contractId: number) => {
    try {
      await api.delete(`/laborcontracts/${contractId}/`);
      if (selectedDoctor?.doctorId) {
        fetchLaborContractsForDoctor(selectedDoctor.doctorId);
      }
    } catch (err) {
      console.error("Error deleting labor contract", err);
    }
  };

  const filteredDoctors = doctors.filter((doc) => {
    const fullName = `${doc.lastName} ${doc.firstName} ${doc.middleName || ""}`.toLowerCase();
    const matchesName = fullName.includes(searchName.toLowerCase());
    const matchesSpecialization = specializationFilter
      ? doc.position?.title === specializationFilter
      : true;
    return matchesName && matchesSpecialization;
  });

  const openScheduleDialogHandler = (doctor: IDoctor) => {
    setSelectedDoctor(doctor);
    setOpenScheduleDialog(true);
    if (doctor.doctorId) {
      fetchSchedulesForDoctor(doctor.doctorId);
    }
  };

  const closeScheduleDialogHandler = () => {
    setOpenScheduleDialog(false);
    setSchedules([]);
  };

  const openContractsDialogHandler = (doctor: IDoctor) => {
    setSelectedDoctor(doctor);
    setOpenContractsDialog(true);
    if (doctor.doctorId) {
      fetchLaborContractsForDoctor(doctor.doctorId);
    }
  };

  const closeContractsDialogHandler = () => {
    setOpenContractsDialog(false);
    setLaborContracts([]);
  };

  const confirmDelete = (doctorId: number) => {
    const doctor = doctors.find((d) => d.doctorId === doctorId);
    if (doctor) {
      setSelectedDoctor(doctor);
      setOpenDeleteConfirm(true);
    }
  };

  const closeDeleteConfirm = () => {
    setOpenDeleteConfirm(false);
    setSelectedDoctor(null);
  };

  const renderScheduleRow = (schedule: ISchedule) => (
    <TableRow key={schedule.scheduleId}>
      <TableCell>{schedule.date}</TableCell>
      <TableCell>{schedule.shift || "N/A"}</TableCell>
      <TableCell>{schedule.startTime}</TableCell>
      <TableCell>{schedule.endTime}</TableCell>
      <TableCell>
        <Button
          variant="outlined"
          onClick={() => {
            setSelectedSchedule(schedule);
            setIsEditScheduleDialogOpen(true);
          }}
          sx={{ mr: 1 }}
        >
          Edit
        </Button>
        <Button
          variant="outlined"
          color="error"
          onClick={() => handleDeleteSchedule(schedule.scheduleId)}
        >
          Delete
        </Button>
      </TableCell>
    </TableRow>
  );

  return (
    <Container maxWidth="lg" sx={{ marginTop: 8 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h5" gutterBottom>
          Doctor Management
        </Typography>
        <Box
          sx={{
            display: "flex",
            flexDirection: isMobile ? "column" : "row",
            gap: 2,
            mb: 2,
          }}
        >
          <TextField
            label="Search by name"
            variant="outlined"
            value={searchName}
            onChange={(e) => setSearchName(e.target.value)}
            fullWidth
          />
          <Select
            value={specializationFilter}
            onChange={(e) => setSpecializationFilter(e.target.value as string)}
            displayEmpty
            fullWidth
          >
            <MenuItem value="">
              <em>All Specializations</em>
            </MenuItem>
            {positions.map((pos) => (
              <MenuItem key={pos.positionId} value={pos.title}>
                {pos.title}
              </MenuItem>
            ))}
          </Select>
          <Button variant="contained" onClick={handleOpenCreateDialog}>
            Add New Doctor
          </Button>
        </Box>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Name</TableCell>
                <TableCell>Specialization</TableCell>
                <TableCell align="center">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredDoctors.map((doc) => (
                <TableRow key={doc.doctorId}>
                  <TableCell>
                    {doc.lastName} {doc.firstName} {doc.middleName}
                  </TableCell>
                  <TableCell>
                    {doc.position?.title || "N/A"}
                  </TableCell>
                  <TableCell align="center">
                    <IconButton
                      onClick={() => openScheduleDialogHandler(doc)}
                      color="primary"
                      aria-label="manage schedule"
                    >
                      <ScheduleIcon />
                    </IconButton>
                    <IconButton
                      onClick={() => openContractsDialogHandler(doc)}
                      color="secondary"
                      aria-label="manage contracts"
                    >
                      <ContractIcon />
                    </IconButton>
                    <IconButton
                      onClick={() => handleSelectDoctor(doc)}
                      color="default"
                      aria-label="edit doctor"
                    >
                      <EditIcon />
                    </IconButton>
                    <IconButton
                      onClick={() => confirmDelete(doc.doctorId)}
                      color="error"
                      aria-label="delete doctor"
                    >
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
              {filteredDoctors.length === 0 && (
                <TableRow>
                  <TableCell colSpan={3} align="center">
                    No doctors found.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>

        {/* Create Doctor Dialog */}
        <Dialog
          open={openCreateDialog}
          onClose={handleCloseCreateDialog}
          fullWidth
          maxWidth="sm"
        >
          <DialogTitle>Add New Doctor</DialogTitle>
          <DialogContent
            sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}
          >
            <TextField
              label="Last Name"
              value={doctorCreateForm.lastName}
              onChange={(e) =>
                setDoctorCreateForm({
                  ...doctorCreateForm,
                  lastName: e.target.value,
                })
              }
              fullWidth
              required
            />
            <TextField
              label="First Name"
              value={doctorCreateForm.firstName}
              onChange={(e) =>
                setDoctorCreateForm({
                  ...doctorCreateForm,
                  firstName: e.target.value,
                })
              }
              fullWidth
              required
            />
            <TextField
              label="Middle Name"
              value={doctorCreateForm.middleName || ""}
              onChange={(e) =>
                setDoctorCreateForm({
                  ...doctorCreateForm,
                  middleName: e.target.value,
                })
              }
              fullWidth
            />
            <Box>
              <Typography variant="body1">Gender:</Typography>
              <Select
                value={doctorCreateForm.gender}
                onChange={(e) =>
                  setDoctorCreateForm({
                    ...doctorCreateForm,
                    gender: e.target.value as "M" | "F",
                  })
                }
                fullWidth
                required
              >
                <MenuItem value="M">Male</MenuItem>
                <MenuItem value="F">Female</MenuItem>
                <MenuItem value="O">Other</MenuItem>
              </Select>
            </Box>
            <TextField
              label="Date Of Birth"
              type="date"
              value={doctorCreateForm.dateOfBirth}
              onChange={(e) =>
                setDoctorCreateForm({
                  ...doctorCreateForm,
                  dateOfBirth: e.target.value,
                })
              }
              InputLabelProps={{ shrink: true }}
              fullWidth
              required
            />
            <TextField
              label="Education"
              value={doctorCreateForm.education || ""}
              onChange={(e) =>
                setDoctorCreateForm({
                  ...doctorCreateForm,
                  education: e.target.value,
                })
              }
              fullWidth
            />
            <Box>
              <Typography variant="body1">Select Specialization:</Typography>
              <Select
                value={selectedPositionTitleCreate}
                onChange={(e) =>
                  setSelectedPositionTitleCreate(e.target.value as string)
                }
                displayEmpty
                fullWidth
                required
              >
                <MenuItem value="">
                  <em>Select Position</em>
                </MenuItem>
                {positions.map((pos) => (
                  <MenuItem key={pos.positionId} value={pos.title}>
                    {pos.title}
                  </MenuItem>
                ))}
              </Select>
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseCreateDialog}>Cancel</Button>
            <Button variant="contained" onClick={handleCreateDoctor}>
              Save
            </Button>
          </DialogActions>
        </Dialog>

        {/* Edit Doctor Dialog */}
        <Dialog
          open={openEditDialog}
          onClose={handleCloseEditDialog}
          fullWidth
          maxWidth="sm"
        >
          <DialogTitle>Edit Doctor Info</DialogTitle>
          <DialogContent
            sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}
          >
            <TextField
              label="Last Name"
              value={doctorEditForm.lastName}
              onChange={(e) =>
                setDoctorEditForm({
                  ...doctorEditForm,
                  lastName: e.target.value,
                })
              }
              fullWidth
              required
            />
            <TextField
              label="First Name"
              value={doctorEditForm.firstName}
              onChange={(e) =>
                setDoctorEditForm({
                  ...doctorEditForm,
                  firstName: e.target.value,
                })
              }
              fullWidth
              required
            />
            <TextField
              label="Middle Name"
              value={doctorEditForm.middleName || ""}
              onChange={(e) =>
                setDoctorEditForm({
                  ...doctorEditForm,
                  middleName: e.target.value,
                })
              }
              fullWidth
            />
            <Box>
              <Typography variant="body1">Gender:</Typography>
              <Select
                value={doctorEditForm.gender}
                onChange={(e) =>
                  setDoctorEditForm({
                    ...doctorEditForm,
                    gender: e.target.value as "M" | "F",
                  })
                }
                fullWidth
                required
              >
                <MenuItem value="M">Male</MenuItem>
                <MenuItem value="F">Female</MenuItem>
                <MenuItem value="O">Other</MenuItem>
              </Select>
            </Box>
            <TextField
              label="Date Of Birth"
              type="date"
              value={doctorEditForm.dateOfBirth}
              InputLabelProps={{ shrink: true }}
              InputProps={{ readOnly: true }}
              fullWidth
              required
            />
            <TextField
              label="Education"
              value={doctorEditForm.education || ""}
              onChange={(e) =>
                setDoctorEditForm({
                  ...doctorEditForm,
                  education: e.target.value,
                })
              }
              fullWidth
            />
            <Box>
              <Typography variant="body1">Select Specialization:</Typography>
              <Select
                value={selectedPositionTitleEdit}
                onChange={(e) =>
                  setSelectedPositionTitleEdit(e.target.value as string)
                }
                displayEmpty
                fullWidth
              >
                <MenuItem value="">
                  <em>Keep Current</em>
                </MenuItem>
                {positions.map((pos) => (
                  <MenuItem key={pos.positionId} value={pos.title}>
                    {pos.title}
                  </MenuItem>
                ))}
              </Select>
              <Typography variant="caption">
                If left empty, the specialization stays the same.
              </Typography>
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseEditDialog}>Cancel</Button>
            <Button variant="contained" onClick={handleEditDoctor}>
              Update
            </Button>
          </DialogActions>
        </Dialog>

        {/* Manage Schedules Dialog */}
        <Dialog
          open={openScheduleDialog}
          onClose={closeScheduleDialogHandler}
          fullWidth
          maxWidth="md"
        >
          <DialogTitle>Manage Schedules</DialogTitle>
          <DialogContent>
            <Box
              component="form"
              sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 2 }}
            >
              <TextField
                label="Date"
                type="date"
                InputLabelProps={{ shrink: true }}
                value={scheduleForm.date}
                onChange={(e) =>
                  setScheduleForm({ ...scheduleForm, date: e.target.value })
                }
                fullWidth
                required
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={scheduleForm.isWorkingDay}
                    onChange={(e) =>
                      setScheduleForm({
                        ...scheduleForm,
                        isWorkingDay: e.target.checked,
                      })
                    }
                  />
                }
                label="Is Working Day"
              />
              <TextField
                label="Shift"
                value={scheduleForm.shift}
                onChange={(e) =>
                  setScheduleForm({ ...scheduleForm, shift: e.target.value })
                }
                fullWidth
              />
              <TextField
                label="Start Time"
                type="time"
                InputLabelProps={{ shrink: true }}
                value={scheduleForm.startTime}
                onChange={(e) =>
                  setScheduleForm({
                    ...scheduleForm,
                    startTime: e.target.value,
                  })
                }
                fullWidth
                required
              />
              <TextField
                label="End Time"
                type="time"
                InputLabelProps={{ shrink: true }}
                value={scheduleForm.endTime}
                onChange={(e) =>
                  setScheduleForm({ ...scheduleForm, endTime: e.target.value })
                }
                fullWidth
                required
              />
              <Button variant="contained" onClick={handleCreateSchedule}>
                Create Schedule
              </Button>
            </Box>
            <Typography variant="h6" sx={{ mt: 4 }}>
              Existing Schedules
            </Typography>
            <TableContainer component={Paper} sx={{ mt: 2 }}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Date</TableCell>
                    <TableCell>Shift</TableCell>
                    <TableCell>Start Time</TableCell>
                    <TableCell>End Time</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {schedules.map((schedule) => (
                    <TableRow key={schedule.scheduleId}>
                      <TableCell>{schedule.date}</TableCell>
                      <TableCell>{schedule.shift || "N/A"}</TableCell>
                      <TableCell>{schedule.startTime}</TableCell>
                      <TableCell>{schedule.endTime}</TableCell>
                      <TableCell>
                        <Button
                          variant="outlined"
                          onClick={() => {
                            setSelectedSchedule(schedule);
                            setIsEditScheduleDialogOpen(true);
                          }}
                          sx={{ mr: 1 }}
                        >
                          Edit
                        </Button>
                        <Button
                          variant="outlined"
                          color="error"
                          onClick={() => handleDeleteSchedule(schedule.scheduleId)}
                        >
                          Delete
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                  {schedules.length === 0 && (
                    <TableRow>
                      <TableCell colSpan={5} align="center">
                        No schedules found.
                      </TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </DialogContent>
          <DialogActions>
            <Button onClick={closeScheduleDialogHandler}>Close</Button>
          </DialogActions>
        </Dialog>

        {/* Manage Contracts Dialog */}
        <Dialog
          open={openContractsDialog}
          onClose={closeContractsDialogHandler}
          fullWidth
          maxWidth="md"
        >
          <DialogTitle>
            Manage Labor Contracts for {selectedDoctor?.firstName} {selectedDoctor?.lastName}
          </DialogTitle>
          <DialogContent>
            <Box sx={{ mb: 2 }}>
              <Typography variant="h6">Add New Labor Contract</Typography>
              <Box sx={{ display: "flex", gap: 2, flexWrap: "wrap", mt: 1 }}>
                <TextField
                  label="Start Date"
                  type="date"
                  value={contractForm.startDate}
                  onChange={(e) =>
                    setContractForm({
                      ...contractForm,
                      startDate: e.target.value,
                    })
                  }
                  InputLabelProps={{ shrink: true }}
                  fullWidth
                  required
                />
                <TextField
                  label="End Date"
                  type="date"
                  value={contractForm.endDate}
                  onChange={(e) =>
                    setContractForm({
                      ...contractForm,
                      endDate: e.target.value,
                    })
                  }
                  InputLabelProps={{ shrink: true }}
                  fullWidth
                />
                <TextField
                  label="Contract Details"
                  value={contractForm.contractDetails || ""}
                  onChange={(e) =>
                    setContractForm({
                      ...contractForm,
                      contractDetails: e.target.value,
                    })
                  }
                  fullWidth
                />
                <Button variant="contained" onClick={handleCreateLaborContract}>
                  Add Contract
                </Button>
              </Box>
            </Box>
            <Typography variant="h6">Existing Labor Contracts</Typography>
            <TableContainer component={Paper} sx={{ mt: 1 }}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Start Date</TableCell>
                    <TableCell>End Date</TableCell>
                    <TableCell>Details</TableCell>
                    <TableCell align="center">Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {laborContracts.map((contract) => (
                    <TableRow key={contract.contractId}>
                      <TableCell>{contract.startDate}</TableCell>
                      <TableCell>{contract.endDate || "N/A"}</TableCell>
                      <TableCell>{contract.contractDetails || "N/A"}</TableCell>
                      <TableCell align="center">
                        <Button
                          size="small"
                          onClick={() => {
                            setSelectedLaborContract(contract);
                            setIsEditLaborContractDialogOpen(true);
                          }}
                          variant="outlined"
                          sx={{ mr: 1 }}
                        >
                          Edit
                        </Button>
                        <Button
                          size="small"
                          color="error"
                          onClick={() => handleDeleteLaborContract(contract.contractId)}
                          variant="outlined"
                        >
                          Delete
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                  {laborContracts.length === 0 && (
                    <TableRow>
                      <TableCell colSpan={4} align="center">
                        No labor contracts found.
                      </TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </DialogContent>
          <DialogActions>
            <Button onClick={closeContractsDialogHandler}>Close</Button>
          </DialogActions>
        </Dialog>

        {/* Edit Labor Contract Dialog */}
        <Dialog
          open={isEditLaborContractDialogOpen}
          onClose={() => setIsEditLaborContractDialogOpen(false)}
          fullWidth
          maxWidth="sm"
        >
          <DialogTitle>Edit Labor Contract</DialogTitle>
          <DialogContent
            sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}
          >
            <TextField
              label="Start Date"
              type="date"
              value={selectedLaborContract?.startDate || ""}
              onChange={(e) =>
                setSelectedLaborContract({
                  ...selectedLaborContract!,
                  startDate: e.target.value,
                })
              }
              InputLabelProps={{ shrink: true }}
              fullWidth
              required
            />
            <TextField
              label="End Date"
              type="date"
              value={selectedLaborContract?.endDate || ""}
              onChange={(e) =>
                setSelectedLaborContract({
                  ...selectedLaborContract!,
                  endDate: e.target.value,
                })
              }
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
            <TextField
              label="Contract Details"
              value={selectedLaborContract?.contractDetails || ""}
              onChange={(e) =>
                setSelectedLaborContract({
                  ...selectedLaborContract!,
                  contractDetails: e.target.value,
                })
              }
              fullWidth
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setIsEditLaborContractDialogOpen(false)}>
              Cancel
            </Button>
            <Button variant="contained" onClick={handleEditLaborContract}>
              Save Changes
            </Button>
          </DialogActions>
        </Dialog>

        {/* Edit Schedule Dialog */}
        <Dialog
          open={isEditScheduleDialogOpen}
          onClose={() => setIsEditScheduleDialogOpen(false)}
          fullWidth
          maxWidth="sm"
        >
          <DialogTitle>Edit Schedule</DialogTitle>
          <DialogContent
            sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}
          >
            <TextField
              label="Date"
              type="date"
              value={selectedSchedule?.date || ""}
              onChange={(e) =>
                setSelectedSchedule({
                  ...selectedSchedule!,
                  date: e.target.value,
                })
              }
              fullWidth
              InputLabelProps={{
                shrink: true,
              }}
              required
            />
            <TextField
              label="Start Time"
              type="time"
              value={selectedSchedule?.startTime || ""}
              onChange={(e) =>
                setSelectedSchedule({
                  ...selectedSchedule!,
                  startTime: e.target.value,
                })
              }
              fullWidth
              InputLabelProps={{
                shrink: true,
              }}
              required
            />
            <TextField
              label="End Time"
              type="time"
              value={selectedSchedule?.endTime || ""}
              onChange={(e) =>
                setSelectedSchedule({
                  ...selectedSchedule!,
                  endTime: e.target.value,
                })
              }
              fullWidth
              InputLabelProps={{
                shrink: true,
              }}
              required
            />
            <TextField
              label="Shift"
              value={selectedSchedule?.shift || ""}
              onChange={(e) =>
                setSelectedSchedule({
                  ...selectedSchedule!,
                  shift: e.target.value,
                })
              }
              fullWidth
              margin="normal"
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setIsEditScheduleDialogOpen(false)}>
              Cancel
            </Button>
            <Button variant="contained" onClick={handleEditSchedule}>
              Save
            </Button>
          </DialogActions>
        </Dialog>

        {/* Delete Confirmation Dialog */}
        <Dialog open={openDeleteConfirm} onClose={closeDeleteConfirm}>
          <DialogTitle>Confirm Deletion</DialogTitle>
          <DialogContent>
            <Typography>
              Are you sure you want to delete {selectedDoctor?.firstName} {selectedDoctor?.lastName}?
            </Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={closeDeleteConfirm}>Cancel</Button>
            <Button
              color="error"
              variant="contained"
              onClick={handleDeleteDoctor}
            >
              Delete
            </Button>
          </DialogActions>
        </Dialog>
      </Paper>
    </Container>
  );
};

export default Doctors;