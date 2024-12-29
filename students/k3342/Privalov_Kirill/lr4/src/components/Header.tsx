import React from "react";
import { AppBar, Toolbar, Typography, Button, Box } from "@mui/material";
import { Link } from "react-router-dom";
import PeopleIcon from "@mui/icons-material/People";
import PersonIcon from "@mui/icons-material/Person";
import PaymentIcon from "@mui/icons-material/Payment";
import EventNoteIcon from "@mui/icons-material/EventNote";
import LocalHospitalIcon from "@mui/icons-material/LocalHospital";

export default function Header() {
    return (
        <>
            <AppBar position="static" color="primary">
                <Toolbar>
                    <Typography variant="h6" style={{ flexGrow: 1 }}>
                        Clinic Administration
                    </Typography>
                    <Button color="inherit" startIcon={<PeopleIcon />} component={Link} to="/patients">Patients</Button>
                    <Button color="inherit" startIcon={<PersonIcon />} component={Link} to="/doctors">Doctors</Button>
                    <Button color="inherit" startIcon={<PaymentIcon />} component={Link} to="/accounting">Accounting</Button>
                    <Button color="inherit" startIcon={<EventNoteIcon />} component={Link} to="/schedule">Schedule</Button>
                    <Button color="inherit" startIcon={<LocalHospitalIcon />} component={Link} to="/visits">Visits</Button>
                </Toolbar>
            </AppBar>
            <Box mb={2} />
        </>
    );
}