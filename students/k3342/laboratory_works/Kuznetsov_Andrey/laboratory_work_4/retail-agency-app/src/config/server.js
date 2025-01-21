import express from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import bodyParser from 'body-parser';
import cors from 'cors';

const JWT_SECRET = 'SUPER-PUPER-SECRET';
import { API_BASE_URL } from './config.js';

const app = express();
app.use(bodyParser.json());
const cors = require('cors')
app.use(cors({ origin: 'http://localhost:8080' }));

function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validatePassword(password) {
    return (
        password.length >= 8 &&
        /[A-Z]/.test(password) && 
        /[a-z]/.test(password) && 
        /\d/.test(password) &&   
        /[!@#$%^&*(),.?":{}|<>]/.test(password) 
    );
}

app.post('/register', async (req, res) => {
    console.log(req.body)
    const { email, password, name, status } = req.body;

    if (!email || !password || !name || !status) {
        return res.status(400).json({ message: 'All fields are required.' });
    }

    if (!validateEmail(email)) {
        return res.status(400).json({ message: 'Invalid email format.' });
    }
    

    if (!validatePassword(password)) {
        return res.status(400).json({ 
            message: 'Password must be at least 8 characters long, include uppercase and lowercase letters, a number, and a special character.' 
        });
    }

    try {
        const usersResponse = await fetch(`${API_BASE_URL}/users?email=${encodeURIComponent(email)}`);
        const users = await usersResponse.json();

        if (users.length > 0) {
            return res.status(400).json({ message: 'Email already exists.' });
        }

        const hashedPassword = await bcrypt.hash(password, 10);

        const newUser = { email, password: hashedPassword, name, status };
        const createUserResponse = await fetch(`${API_BASE_URL}/users`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newUser)
        });

        if (!createUserResponse.ok) {
            throw new Error('Failed to create user in database.');
        }

        const createdUser = await createUserResponse.json();
        res.status(201).json({ message: 'User registered successfully.', user: createdUser });
    } catch (error) {
        console.error('Error during registration:', error);
        res.status(500).json({ message: 'Registration failed. Please try again later.' });
    }
});

app.post('/login', async (req, res) => {
    const { email, password } = req.body;
    console.log(email, password)

    if (!email || !password) {
        return res.status(400).json({ message: 'Email and password are required.' });
    }

    try {
        const usersResponse = await fetch(`${API_BASE_URL}/users?email=${encodeURIComponent(email)}`);
        const users = await usersResponse.json();

        const user = users[0]; 
        if (!user) {
            return res.status(400).json({ message: 'Invalid email or password.' });
        }

        const isPasswordValid = await bcrypt.compare(password, user.password);

        if (!isPasswordValid) {
            return res.status(400).json({ message: 'Invalid email or password.' });
        }

        const token = jwt.sign({ id: user.id, email: user.email }, JWT_SECRET, { expiresIn: '1h' });

        res.json({ token, user });
    } catch (error) {
        console.error('Error during login:', error);
        res.status(500).json({ message: 'Login failed. Please try again later.' });
    }
});

const PORT = 5000; 
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
