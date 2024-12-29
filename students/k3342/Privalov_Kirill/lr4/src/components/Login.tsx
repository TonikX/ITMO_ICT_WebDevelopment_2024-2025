import React, { useState } from "react";
import {
  Button,
  Container,
  TextField,
  Box,
  Typography,
  Paper,
} from "@mui/material";
import axios, { AxiosResponse } from "axios";

function Login() {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  if (localStorage.getItem("access")) {
    window.location.href = "/";
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      axios
        .post("http://localhost:8000/auth/jwt/create/", formData)
        .then((res: AxiosResponse<{ access: string; refresh: string }>) => {
          localStorage.setItem("refresh", res.data.refresh);
          localStorage.setItem("access", res.data.access);
          window.location.href = "/";
        });
    } catch (error) {
      console.error(error);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <Container maxWidth="sm" sx={{ marginTop: 8 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h5" gutterBottom>
          Login
        </Typography>
        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            label="Username"
            name="username"
            margin="normal"
            fullWidth
            onChange={handleChange}
          />
          <TextField
            label="Password"
            name="password"
            type="password"
            margin="normal"
            fullWidth
            onChange={handleChange}
          />
          <Button type="submit" variant="contained" sx={{ mt: 2 }}>
            Login
          </Button>
        </Box>
        <Typography variant="body2" sx={{ mt: 2 }}>
          Don't have an account? <a href="/signup">Sign Up</a>
        </Typography>
      </Paper>
    </Container>
  );
}

export default Login;
