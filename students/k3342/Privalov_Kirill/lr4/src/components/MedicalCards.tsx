import React, {useEffect, useState} from "react";
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
} from "@mui/material";
import api from "../api/api";

interface Patient {
  patientId: number;
  firstName: string;
  lastName: string;
  middleName?: string;
  gender: string;
  dateOfBirth: string;
  phone?: string;
  address?: string;
}

interface MedicalCard {
  medicalCardId: number;
  issueDate: string;
  notes?: string;
  patientId: number;
  patient: Patient;
}

interface MedicalCardsProps {
  patientId: number;
  onClose: () => void;
}

function MedicalCards({patientId, onClose}: MedicalCardsProps) {
  const [medicalCards, setMedicalCards] = useState<MedicalCard[]>([]);
  const [createOpen, setCreateOpen] = useState(false);
  const [newIssueDate, setNewIssueDate] = useState("");
  const [newNotes, setNewNotes] = useState("");

  const [editOpen, setEditOpen] = useState(false);
  const [currentCard, setCurrentCard] = useState<MedicalCard | null>(null);
  const [editIssueDate, setEditIssueDate] = useState("");
  const [editNotes, setEditNotes] = useState("");

  const minIssueDate = (() => {
    const date = new Date();
    date.setFullYear(date.getFullYear() - 100);
    return date.toISOString().split("T")[0];
  })();

  const todayDate = new Date().toISOString().split("T")[0];

  useEffect(() => {
    fetchMedicalCards();
  }, [patientId]);

  const fetchMedicalCards = async () => {
    try {
      const res = await api.get(`/medicalcards?patientId=${patientId}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access")}`,
        },
      });
      setMedicalCards(res.data);
    } catch (error) {
      console.error("Failed to fetch medical cards:", error);
    }
  };

  const handleCreateOpen = () => setCreateOpen(true);
  const handleCreateClose = () => {
    setCreateOpen(false);
    setNewIssueDate("");
    setNewNotes("");
  };

  const handleCreate = async () => {
    if (newIssueDate && new Date(newIssueDate) > new Date()) {
      console.error("Issue Date cannot be in the future.");
      return;
    }
    try {
      await api.post(
          "/medicalcards/",
          {
            issueDate: newIssueDate,
            notes: newNotes,
            patientId: patientId,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access")}`,
            },
          }
      );
      handleCreateClose();
      fetchMedicalCards();
    } catch (error) {
      console.error("Failed to create medical card:", error);
    }
  };

  const handleEditOpen = (card: MedicalCard) => {
    setCurrentCard(card);
    setEditIssueDate(card.issueDate);
    setEditNotes(card.notes || "");
    setEditOpen(true);
  };

  const handleEditClose = () => {
    setEditOpen(false);
    setCurrentCard(null);
    setEditIssueDate("");
    setEditNotes("");
  };

  const handleEditSave = async () => {
    if (currentCard) {
      if (editIssueDate && new Date(editIssueDate) > new Date()) {
        console.error("Issue Date cannot be in the future.");
        return;
      }
      try {
        await api.put(
            `/medicalcards/${currentCard.medicalCardId}/`,
            {
              issueDate: editIssueDate,
              notes: editNotes,
              patientId: patientId,
            },
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("access")}`,
              },
            }
        );
        handleEditClose();
        fetchMedicalCards();
      } catch (error) {
        console.error("Failed to edit medical card:", error);
      }
    }
  };

  const handleDelete = async (cardId: number) => {
    if (window.confirm("Are you sure you want to delete this medical card?")) {
      try {
        await api.delete(`/medicalcards/${cardId}/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access")}`,
          },
        });
        setMedicalCards(medicalCards.filter((c) => c.medicalCardId !== cardId));
      } catch (error) {
        console.error("Failed to delete medical card:", error);
      }
    }
  };

  return (
      <Dialog open={true} onClose={onClose} fullWidth maxWidth="md">
        <DialogTitle>Medical Cards for Patient ID: {patientId}</DialogTitle>
        <DialogContent>
          <Button variant="contained" onClick={handleCreateOpen} sx={{mb: 2}}>
            Create Medical Card
          </Button>
          <Paper sx={{mt: 2}}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Issue Date</TableCell>
                  <TableCell>Notes</TableCell>
                  <TableCell>Patient Name</TableCell> {/* Changed to display patient name */}
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {medicalCards.map((c) => (
                    <TableRow key={c.medicalCardId}> {/* Changed to medicalCardId */}
                      <TableCell>{c.medicalCardId}</TableCell> {/* Changed to medicalCardId */}
                      <TableCell>{c.issueDate}</TableCell> {/* Changed to issueDate */}
                      <TableCell>{c.notes || ""}</TableCell>
                      <TableCell>
                        {c.patient
                            ? `${c.patient.firstName} ${c.patient.lastName}`
                            : "N/A"}
                      </TableCell> {/* Displaying patient name */}
                      <TableCell>
                        <Button
                            variant="outlined"
                            onClick={() => handleEditOpen(c)}
                            sx={{mr: 1}}
                        >
                          Edit
                        </Button>
                        <Button
                            variant="outlined"
                            color="error"
                            onClick={() => handleDelete(c.medicalCardId)}
                        >
                          Delete
                        </Button>
                      </TableCell>
                    </TableRow>
                ))}
              </TableBody>
            </Table>
          </Paper>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Close</Button>
        </DialogActions>

        <Dialog
            open={createOpen}
            onClose={handleCreateClose}
            fullWidth
            maxWidth="sm"
        >
          <DialogTitle>Create New Medical Card</DialogTitle>
          <DialogContent>
            <TextField
                label="Issue Date"
                type="date"
                value={newIssueDate}
                fullWidth
                onChange={(e) => setNewIssueDate(e.target.value)}
                inputProps={{min: minIssueDate, max: todayDate}}
                sx={{mb: 2}}
                InputLabelProps={{shrink: true}}
            />
            <TextField
                margin="dense"
                label="Notes"
                fullWidth
                multiline
                rows={4}
                value={newNotes}
                onChange={(e) => setNewNotes(e.target.value)}
                sx={{mb: 2}}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCreateClose}>Cancel</Button>
            <Button onClick={handleCreate} variant="contained">
              Create
            </Button>
          </DialogActions>
        </Dialog>
        <Dialog open={editOpen} onClose={handleEditClose} fullWidth maxWidth="sm">
          <DialogTitle>Edit Medical Card</DialogTitle>
          <DialogContent>
            <TextField
                label="Issue Date"
                type="date"
                value={editIssueDate}
                fullWidth
                onChange={(e) => setEditIssueDate(e.target.value)}
                inputProps={{min: minIssueDate, max: todayDate}}
                sx={{mb: 2}}
                InputLabelProps={{shrink: true}}
            />
            <TextField
                margin="dense"
                label="Notes"
                fullWidth
                multiline
                rows={4}
                value={editNotes}
                onChange={(e) => setEditNotes(e.target.value)}
                sx={{mb: 2}}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleEditClose}>Cancel</Button>
            <Button onClick={handleEditSave} variant="contained">
              Save
            </Button>
          </DialogActions>
        </Dialog>
      </Dialog>
  );
}

export default MedicalCards;