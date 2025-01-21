import React, { useContext, useState } from 'react';
import { AuthContext } from '../../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';
import {
    Container,
    TextField,
    Button,
    Typography,
    Box,
    Alert,
} from '@mui/material';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';

interface LoginFormValues {
    username: string;
    password: string;
}

const Login: React.FC = () => {
    const authContext = useContext(AuthContext);
    const navigate = useNavigate();
    const [error, setError] = useState<string | null>(null);

    if (!authContext) {
        throw new Error('AuthContext is undefined');
    }

    const initialValues: LoginFormValues = {
        username: '',
        password: '',
    };

    const validationSchema = Yup.object({
        username: Yup.string().required('Обязательно'),
        password: Yup.string().required('Обязательно'),
    });

    const handleSubmit = async (values: LoginFormValues) => {
        try {
            await authContext.login(values.username, values.password);
            navigate('/dashboard');
        } catch (err: any) {
            setError(err.message || 'Ошибка входа');
        }
    };

    return (
        <Container maxWidth="sm">
            <Box sx={{ mt: 8 }}>
                <Typography variant="h4" component="h1" gutterBottom>
                    Вход
                </Typography>
                {error && <Alert severity="error">{error}</Alert>}
                <Formik
                    initialValues={initialValues}
                    validationSchema={validationSchema}
                    onSubmit={handleSubmit}
                >
                    {({ errors, touched }) => (
                        <Form>
                            <Field
                                as={TextField}
                                name="username"
                                label="Имя пользователя"
                                variant="outlined"
                                margin="normal"
                                fullWidth
                                error={touched.username && Boolean(errors.username)}
                                helperText={touched.username && errors.username}
                            />
                            <Field
                                as={TextField}
                                name="password"
                                label="Пароль"
                                type="password"
                                variant="outlined"
                                margin="normal"
                                fullWidth
                                error={touched.password && Boolean(errors.password)}
                                helperText={touched.password && errors.password}
                            />
                            <Button type="submit" variant="contained" color="primary" fullWidth sx={{ backgroundColor: '#B0B0B0', color: 'black', mr: 2 }}>
                                Войти
                            </Button>
                        </Form>
                    )}
                </Formik>
                <Typography variant="body2" align="center" sx={{ mt: 2 }}>
                    Нет аккаунта? <Link to="/register">Зарегистрироваться</Link>
                </Typography>
            </Box>
        </Container>
    );
};

export default Login;
