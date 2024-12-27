import React, { useEffect, useState } from 'react';
import { Container, Typography, Button, Box } from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { Distribution } from '../../types/types';

const DistributionDetail: React.FC = () => {
    const { distributionId } = useParams();
    const navigate = useNavigate();
    const [dist, setDist] = useState<Distribution | null>(null);

    useEffect(() => {
        if (distributionId) {
            api.get<Distribution>(`/distributions/${distributionId}/`)
                .then((res) => setDist(res.data))
                .catch((err) => console.error('Ошибка при загрузке распределения:', err));
        }
    }, [distributionId]);

    const handleDelete = async () => {
        if (!distributionId) return;
        try {
            await api.delete(`/distributions/${distributionId}/`);
            navigate('/distributions');
        } catch (err) {
            console.error('Ошибка при удалении распределения:', err);
        }
    };

    if (!dist) {
        return (
            <Container sx={{ mt: 4 }}>
                <Typography>Загрузка...</Typography>
            </Container>
        );
    }

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Детали распределения
            </Typography>
            <Box sx={{ mb: 2 }}>
                <Typography>
                    <b>Газета:</b> {dist.newspaper?.name}
                </Typography>
                <Typography>
                    <b>Типография:</b> {dist.printshop?.name} ({dist.printshop?.address})
                </Typography>
                <Typography>
                    <b>Почтовое отделение №:</b> {dist.postoffice?.office_number} ({dist.postoffice?.address})
                </Typography>
                <Typography>
                    <b>Тираж:</b> {dist.copies_printed}
                </Typography>
                <Typography>
                    <b>Отправлено:</b> {dist.copies_sent}
                </Typography>
            </Box>
            <Button
                variant="contained"
                color="primary"
                sx={{ mr: 2 }}
                onClick={() => navigate(`/distributions/${distributionId}/edit`)}
            >
                Редактировать
            </Button>
            <Button variant="outlined" color="error" onClick={handleDelete}>
                Удалить
            </Button>
        </Container>
    );
};

export default DistributionDetail;
