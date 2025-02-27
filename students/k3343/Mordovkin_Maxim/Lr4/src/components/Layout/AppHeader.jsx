import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { Group, Text, Button } from '@mantine/core';
import { logout } from '../../store/slices/authSlice';

const AppHeader = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const user = useSelector(state => state.auth.user);

    const handleLogout = () => {
        dispatch(logout());
        navigate('/login');
    };

    return (
        <div style={{ height: 60, padding: '0 1rem', borderBottom: '1px solid #eee' }}>
            <Group position="apart" style={{ height: '100%' }}>
                <Text size="xl" weight={700}>Airport Management System</Text>

                {user && (
                    <Button color="red" onClick={handleLogout}>
                        Logout
                    </Button>
                )}
            </Group>
        </div>
    );
};

export default AppHeader;
