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

interface FormData {
  username: string;
  email: string;
  password: string;
  re_password: string;
}

interface FormErrors {
  username?: string;
  email?: string;
  password?: string;
  re_password?: string;
  general?: string;
}

function SignUp() {
  const [formData, setFormData] = useState<FormData>({
    username: "",
    email: "",
    password: "",
    re_password: "",
  });
  const [formErrors, setFormErrors] = useState<FormErrors>({});

  if (localStorage.getItem("access")) {
    window.location.href = "/";
  }

  const validateEmail = (email: string): boolean => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    let errors: FormErrors = {};

    if (!validateEmail(formData.email)) {
      errors.email = "Please enter a valid email address.";
    }

    if (formData.password !== formData.re_password) {
      errors.re_password = "Passwords do not match.";
    }

    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }

    setFormErrors({});

    try {
      const res: AxiosResponse<{ access: string; refresh: string }> =
        await axios.post("http://localhost:8000/auth/users/", formData);
      window.location.href = "/login";
    } catch (error: any) {
      if (error.response && error.response.data) {
        const backendErrors = error.response.data;
        let newFormErrors: FormErrors = {};

        for (const key in backendErrors) {
          if (backendErrors.hasOwnProperty(key)) {
            newFormErrors[key as keyof FormErrors] = backendErrors[key][0];
          }
        }

        setFormErrors(newFormErrors);
      } else {
        setFormErrors({
          general: "An unexpected error occurred. Please try again later.",
        });
      }
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <Container maxWidth="sm" sx={{ marginTop: 8 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h5" gutterBottom>
          Sign Up
        </Typography>
        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            label="Username"
            name="username"
            margin="normal"
            fullWidth
            value={formData.username}
            onChange={handleChange}
            error={Boolean(formErrors.username)}
            helperText={formErrors.username}
          />
          <TextField
            label="Email"
            name="email"
            type="email"
            margin="normal"
            fullWidth
            value={formData.email}
            onChange={handleChange}
            error={Boolean(formErrors.email)}
            helperText={formErrors.email}
          />
          <TextField
            label="Password"
            name="password"
            type="password"
            margin="normal"
            fullWidth
            value={formData.password}
            onChange={handleChange}
            error={Boolean(formErrors.password)}
            helperText={formErrors.password}
          />
          <TextField
            label="Re-enter Password"
            name="re_password"
            type="password"
            margin="normal"
            fullWidth
            value={formData.re_password}
            onChange={handleChange}
            error={Boolean(formErrors.re_password)}
            helperText={formErrors.re_password}
          />
          <Button type="submit" variant="contained" sx={{ mt: 2 }}>
            Sign Up
          </Button>
          {formErrors.general && (
            <Typography color="error" sx={{ mt: 2 }}>
              {formErrors.general}
            </Typography>
          )}
        </Box>
      </Paper>
    </Container>
  );
}

export default SignUp;
