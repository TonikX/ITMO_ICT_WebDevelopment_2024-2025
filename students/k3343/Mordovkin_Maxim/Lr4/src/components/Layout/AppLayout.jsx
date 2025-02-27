import React, { useState, useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { AppShell } from '@mantine/core';
import { motion } from 'framer-motion';

import AppHeader from './AppHeader';
import AppNavbar from './AppNavbar';
import { fetchUserProfile } from '../../store/slices/authSlice';

const AppLayout = () => {
    const [opened, setOpened] = useState(false);
    const dispatch = useDispatch();
    const { token, user } = useSelector(state => state.auth);

    useEffect(() => {
        // Если есть токен и user == null, подгрузим профиль
        if (token && !user) {
            dispatch(fetchUserProfile());
        }
    }, [token, user, dispatch]);

    return (
        <AppShell
            padding="md"
            header={{ height: 60 }}
            navbar={{ width: 250, breakpoint: 'sm', collapsed: { mobile: !opened } }}
        >
            <AppShell.Header>
                <AppHeader />
            </AppShell.Header>

            <AppShell.Navbar p="xs">
                <AppNavbar />
            </AppShell.Navbar>

            <AppShell.Main>
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.5 }}
                >
                    <Outlet />
                </motion.div>
            </AppShell.Main>
        </AppShell>
    );
};

export default AppLayout;
