import React, { useEffect, useState } from 'react';
import { Container, Typography, Button, Box } from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';

interface PrintShop {
    id: string;
    name: string;
    address: string;
    is_open: boolean;
}

const PrintShopDetail: React.FC = () => {
    const { printshopId } = useParams();
    const navigate = useNavigate();
    const [printshop, setPrintshop] = useState<PrintShop | null>(null);

    useEffect(() => {
        if (printshopId) {
            api.get<PrintShop>(`/printshops/${printshopId}/`)
                .then((res) => setPrintshop(res.data))
                .catch((err) => console.error('Ошибка при загрузке типографии:', err));
        }
    }, [printshopId]);

    const handleDelete = async () => {
        if (!printshopId) return;
        try {
            await api.delete(`/printshops/${printshopId}/`);
            navigate('/printshops');
        } catch (err) {
            console.error('Ошибка при удалении типографии:', err);
        }
    };

    if (!printshop) {
        return (
            <Container sx={{ mt: 4 }}>
                <Typography>Загрузка...</Typography>
            </Container>
        );
    }

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Детали типографии
            </Typography>
            <Box sx={{ mb: 2 }}>
                <Typography variant="body1"><b>ID:</b> {printshop.id}</Typography>
                <Typography variant="body1"><b>Название:</b> {printshop.name}</Typography>
                <Typography variant="body1"><b>Адрес:</b> {printshop.address}</Typography>
                <Typography variant="body1"><b>Статус:</b> {printshop.is_open ? 'Открыта' : 'Закрыта'}</Typography>
            </Box>
            <Button
                variant="contained"
                color="primary"
                sx={{ mr: 2 }}
                onClick={() => navigate(`/printshops/${printshopId}/edit`)}
            >
                Редактировать
            </Button>
            <Button variant="outlined" color="error" onClick={handleDelete}>
                Удалить
            </Button>
        </Container>
    );
};

export default PrintShopDetail;