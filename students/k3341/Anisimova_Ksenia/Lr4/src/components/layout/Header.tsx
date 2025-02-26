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
        <AppBar position="static">
            <Toolbar>
                <Typography variant="h6" sx={{ flexGrow: 1 }}>
                    Ksyusha's Newspaper App
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
                        Dashboard
                    </Button>
                    <Button
                        component={Link}
                        to="/editors"
                        color="inherit"
                        sx={{ textTransform: 'none' }}
                    >
                        Editors
                    </Button>
                    <Button
                        component={Link}
                        to="/newspapers"
                        color="inherit"
                        sx={{ textTransform: 'none' }}
                    >
                        Newspapers
                    </Button>
                    <Button
                        component={Link}
                        to="/printshops"
                        color="inherit"
                        sx={{ textTransform: 'none' }}
                    >
                        Print Shops
                    </Button>
                    <Button
                        component={Link}
                        to="/postoffices"
                        color="inherit"
                        sx={{ textTransform: 'none' }}
                    >
                        Post Offices
                    </Button>
                    <Button
                        component={Link}
                        to="/distributions"
                        color="inherit"
                        sx={{ textTransform: 'none' }}
                    >
                        Distributions
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
                            sx={{
                                textTransform: 'none',
                                fontWeight: 'bold',
                                borderColor: '#ff5a57',  // Change border color
                                color: '#ff5a57',  // Change text color
                                '&:hover': {
                                    borderColor: '#ff5a57',  // Change border color on hover
                                    backgroundColor: 'rgba(214, 74, 4, 0.1)',  // Optional: Change background on hover
                                },
                            }}
                        >
                            Logout
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
                            Login
                        </Button>
                        <Button
                            component={Link}
                            to="/register"
                            color="inherit"
                            sx={{ textTransform: 'none' }}
                        >
                            Register
                        </Button>
                    </Box>
                )}
            </Toolbar>
        </AppBar>
    );
};

export default Header;
