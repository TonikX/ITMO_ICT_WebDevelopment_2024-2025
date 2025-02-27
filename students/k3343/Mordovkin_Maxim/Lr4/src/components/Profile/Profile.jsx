import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Paper, Title, Text, Loader, Button } from '@mantine/core';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

import { fetchUserProfile } from '../../store/slices/authSlice';
import { fetchMyCrewApplications } from '../../store/slices/crewSlice'; // <-- новый экшен
import ApplyCrewForm from './ApplyCrewForm';

const Profile = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { user, loading, error } = useSelector((state) => state.auth);
    const { myApplications } = useSelector((state) => state.crew);

    useEffect(() => {
        if (!user) {
            dispatch(fetchUserProfile());
        }
    }, [user, dispatch]);

    // Загружаем мои заявки, если не ADMIN
    useEffect(() => {
        if (user && user.role !== 'ADMIN') {
            dispatch(fetchMyCrewApplications(user.userId));
        }
    }, [user, dispatch]);

    if (loading) {
        return <Loader size="xl" />;
    }

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
        >
            <Paper p="md" radius="md" withBorder style={{ maxWidth: 600, margin: '40px auto' }}>
                <Title order={2} mb="md">Профиль пользователя</Title>

                {error && (
                    <Text color="red" mb="md">
                        {error}
                    </Text>
                )}

                {user ? (
                    <>
                        <Text>
                            <b>Username:</b> {user.username}
                        </Text>
                        <Text>
                            <b>Role:</b> {user.role}
                        </Text>

                        {user.role !== 'ADMIN' ? (
                            <>
                                <ApplyCrewForm />

                                {/* Список моих заявок */}
                                <Title order={4} mt="lg">Мои заявки на работу</Title>
                                {myApplications.length === 0 ? (
                                    <Text>У вас пока нет заявок</Text>
                                ) : (
                                    myApplications.map((app) => (
                                        <Text key={app.crewMemberID}>
                                            Заявка #{app.crewMemberID}: должность {app.roleName}, статус {app.employmentStatus}
                                        </Text>
                                    ))
                                )}
                            </>
                        ) : (
                            <div style={{ marginTop: '1rem' }}>
                                <Text>Вы администратор.</Text>
                                <Button variant="outline" onClick={() => navigate('/crew-requests')} style={{ marginTop: '0.5rem' }}>
                                    Просмотр заявок на работу
                                </Button>
                            </div>
                        )}
                    </>
                ) : (
                    <Text>Нет данных о пользователе</Text>
                )}
            </Paper>
        </motion.div>
    );
};

export default Profile;
