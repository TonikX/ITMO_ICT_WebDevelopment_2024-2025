// src/components/Auth/RegisterForm.jsx
import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate, Link } from 'react-router-dom';
import { TextInput, PasswordInput, Button, Paper, Title, Text, Group, Select } from '@mantine/core';
import { motion } from 'framer-motion';
import { register } from '../../store/slices/authSlice';

const RegisterForm = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('USER');
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { loading, error } = useSelector(state => state.auth);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const result = await dispatch(register({ username, password, role }));
        if (!result.error) {
            // регистрация успешна, идём на flights
            navigate('/flights');
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
        >
            <Paper radius="md" p="xl" withBorder style={{ maxWidth: 400, margin: '100px auto' }}>
                <Title order={2} align="center" mb="md">Create Account</Title>

                <form onSubmit={handleSubmit}>
                    <TextInput
                        label="Username"
                        placeholder="Your username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                        mb="md"
                    />

                    <PasswordInput
                        label="Password"
                        placeholder="Your password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        mb="md"
                    />

                    <Select
                        label="Role"
                        placeholder="Select your role"
                        value={role}
                        onChange={setRole}
                        data={[
                            { value: 'USER', label: 'User' },
                            { value: 'ADMIN', label: 'Admin' }
                        ]}
                        mb="xl"
                    />

                    {error && (
                        <Text color="red" size="sm" mb="md">
                            {error} {/* Теперь это строка, проблем с рендером не будет */}
                        </Text>
                    )}

                    <Group position="apart">
                        <Button
                            type="submit"
                            loading={loading}
                            fullWidth
                        >
                            Register
                        </Button>
                    </Group>

                    <Text align="center" mt="md">
                        Already have an account?{' '}
                        <Link to="/login" style={{ textDecoration: 'none', color: 'blue' }}>
                            Login
                        </Link>
                    </Text>
                </form>
            </Paper>
        </motion.div>
    );
};

export default RegisterForm;
