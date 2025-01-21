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

interface RegisterFormValues {
    username: string;
    password: string;
    re_password: string;
}

const Register: React.FC = () => {
    const authContext = useContext(AuthContext);
    const navigate = useNavigate();
    const [error, setError] = useState<string | null>(null);

    if (!authContext) {
        throw new Error('AuthContext is undefined');
    }

    const initialValues: RegisterFormValues = {
        username: '',
        password: '',
        re_password: '',
    };

    const validationSchema = Yup.object({
        username: Yup.string().required('Обязательно'),
        password: Yup.string()
            .min(6, 'Пароль должен содержать минимум 6 символов')
            .required('Обязательно'),
        re_password: Yup.string()
            .oneOf([Yup.ref('password')], 'Пароли должны совпадать')
            .required('Обязательно'),
    });

    const handleSubmit = async (values: RegisterFormValues) => {
        try {
            await authContext.register(values.username, values.password);
            navigate('/dashboard');
        } catch (err: any) {
            setError(err.message || 'Ошибка регистрации');
        }
    };

    return (
        <Container maxWidth="sm">
            <Box sx={{ mt: 8 }}>
                <Typography variant="h4" component="h1" gutterBottom>
                    Регистрация
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
                            <Field
                                as={TextField}
                                name="re_password"
                                label="Повторите пароль"
                                type="password"
                                variant="outlined"
                                margin="normal"
                                fullWidth
                                error={touched.re_password && Boolean(errors.re_password)}
                                helperText={touched.re_password && errors.re_password}
                            />
                            <Button type="submit" variant="contained" color="primary" fullWidth sx={{ backgroundColor: '#B0B0B0', color: 'black', mr: 2 }}>
                                Зарегистрироваться
                            </Button>
                        </Form>
                    )}
                </Formik>
                <Typography variant="body2" align="center" sx={{ mt: 2 }}>
                    Уже есть аккаунт? <Link to="/login">Войти</Link>
                </Typography>
            </Box>
        </Container>
    );
};

export default Register;
