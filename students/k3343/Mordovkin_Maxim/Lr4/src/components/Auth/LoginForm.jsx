// src/components/Auth/LoginForm.jsx
import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate, Link } from 'react-router-dom';
import { TextInput, PasswordInput, Button, Paper, Title, Text, Group } from '@mantine/core';
import { motion } from 'framer-motion';
import { login } from '../../store/slices/authSlice';


const LoginForm = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { loading, error } = useSelector(state => state.auth);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const result = await dispatch(login({ username, password }));
        if (!result.error) {
            // логин успешен
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
                <Title order={2} align="center" mb="md">Welcome back</Title>

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
                        mb="xl"
                    />

                    {error && (
                        <Text color="red" size="sm" mb="md">
                            {error} {/* <-- строка, всё ок */}
                        </Text>
                    )}

                    <Group position="apart">
                        <Button
                            type="submit"
                            loading={loading}
                            fullWidth
                        >
                            Login
                        </Button>
                    </Group>

                    <Text align="center" mt="md">
                        Don't have an account?{' '}
                        <Link to="/register" style={{ textDecoration: 'none', color: 'blue' }}>
                            Register
                        </Link>
                    </Text>
                </form>
            </Paper>
        </motion.div>
    );
};

export default LoginForm;
