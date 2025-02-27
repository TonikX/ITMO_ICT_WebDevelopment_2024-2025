// src/components/Home/Home.jsx
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { Button, Text, Paper, Title, Group } from '@mantine/core';
import { motion } from 'framer-motion';
import { logout } from '../../store/slices/authSlice';

const Home = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const user = useSelector(state => state.auth.user);

    const handleLogout = () => {
        dispatch(logout());
        navigate('/login');
    };

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
        >
            <Paper p="xl" radius="md" withBorder style={{ maxWidth: 600, margin: '40px auto' }}>
                <Title order={2} mb="md">Добро пожаловать, {user?.username}!</Title>

                <Text mb="md">
                    Это главная страница системы. Вы можете перейти к рейсам, отчетам, профилю или выйти из системы.
                </Text>

                <Group position="center">
                    <Button variant="outline" onClick={() => navigate('/flights')}>
                        Рейсы
                    </Button>
                    <Button variant="outline" onClick={() => navigate('/reports')}>
                        Отчёты
                    </Button>
                    <Button variant="outline" onClick={() => navigate('/profile')}>
                        Профиль
                    </Button>
                    <Button color="red" onClick={handleLogout}>
                        Выйти
                    </Button>
                </Group>
            </Paper>
        </motion.div>
    );
};

export default Home;
