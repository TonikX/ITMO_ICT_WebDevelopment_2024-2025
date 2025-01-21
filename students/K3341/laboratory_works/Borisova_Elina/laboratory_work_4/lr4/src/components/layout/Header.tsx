import React, { useContext } from 'react';
import {
    AppBar,
    Toolbar,
    Typography,
    Box,
    Button,
    Divider
} from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';

const Header: React.FC = () => {
    const authContext = useContext(AuthContext);
    const navigate = useNavigate();

    const username = localStorage.getItem('username');

    const handleLogout = () => {
        authContext.logout();
        navigate('/login');
    };

    return (
        <AppBar position="static" sx={{ backgroundColor: '#161616' }}>
            <Toolbar>
                <Typography variant="h6" sx={{ flexGrow: 1 }}>
                    Распределение газет
                </Typography>

                <Divider
                    orientation="vertical"
                    flexItem
                    sx={{
                        borderColor: 'rgba(255,255,255,0.5)',
                        mx: 2,
                    }}
                />

                <Box sx={{ display: 'flex', gap: 1 }}>
                    <Button
                        component={Link}
                        to="/dashboard"
                        color="inherit"
                        sx={{ textTransform: 'none' }}
                    >
                        Дашборд
                    </Button>
                    <Button
                        component={Link}
                        to="/editors"
                        color="inherit"
                        sx={{ textTransform: 'none' }}
                    >
                        Редакторы
                    </Button>
                    <Button
                        component={Link}
                        to="/newspapers"
                        color="inherit"
                        sx={{ textTransform: 'none' }}
                    >
                        Газеты
                    </Button>
                    <Button
                        component={Link}
                        to="/printshops"
                        color="inherit"
                        sx={{ textTransform: 'none' }}
                    >
                        Типографии
                    </Button>
                    <Button
                        component={Link}
                        to="/postoffices"
                        color="inherit"
                        sx={{ textTransform: 'none' }}
                    >
                        Почтовые отделения
                    </Button>
                    <Button
                        component={Link}
                        to="/deliveries"
                        color="inherit"
                        sx={{ textTransform: 'none' }}
                    >
                        Доставки
                    </Button>
                </Box>

                <Divider
                    orientation="vertical"
                    flexItem
                    sx={{
                        borderColor: 'rgba(255,255,255,0.5)',
                        mx: 2,
                    }}
                />

                {username ? (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        <Typography variant="body1" color="textPrimary" sx={{ fontWeight: 600 }}>
                            {username}
                        </Typography>
                        <Button
                            onClick={handleLogout}
                            variant="outlined"
                            color="error"
                            sx={{ textTransform: 'none', fontWeight: 'bold' }}
                        >
                            Выйти
                        </Button>
                    </Box>
                ) : (
                    <Box sx={{ display: 'flex', gap: 1 }}>
                        <Button
                            component={Link}
                            to="/login"
                            color="inherit"
                            sx={{ textTransform: 'none' }}
                        >
                            Войти
                        </Button>
                        <Button
                            component={Link}
                            to="/register"
                            color="inherit"
                            sx={{ textTransform: 'none' }}
                        >
                            Регистрация
                        </Button>
                    </Box>
                )}
            </Toolbar>
        </AppBar>
    );
};

export default Header;
