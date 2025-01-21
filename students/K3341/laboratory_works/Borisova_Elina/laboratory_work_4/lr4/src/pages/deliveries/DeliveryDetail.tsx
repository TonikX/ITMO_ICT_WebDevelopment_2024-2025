import React, { useEffect, useState } from 'react';
import { Container, Typography, Button, Box } from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';

interface Delivery {
    id: number;
    print_run: {
        id: number;
        newspaper: {
            name: string;
        };
        printshop: {
            name: string;
        };
        quantity: number;
        date: string;
    };
    post_office: {
        number: string;
        address: string;
    };
    printshop: {
        name: string;
    };
    quantity: number;
}

const DeliveryDetail: React.FC = () => {
    const { deliveryId } = useParams();
    const navigate = useNavigate();
    const [delivery, setDelivery] = useState<Delivery | null>(null);

    useEffect(() => {
        if (deliveryId) {
            api.get<Delivery>(`/deliveries/${deliveryId}/`)
                .then((res) => setDelivery(res.data))
                .catch((err) => console.error('Ошибка при загрузке доставки:', err));
        }
    }, [deliveryId]);

    const handleDelete = async () => {
        if (!deliveryId) return;
        try {
            await api.delete(`/deliveries/${deliveryId}/`);
            navigate('/deliveries');
        } catch (err) {
            console.error('Ошибка при удалении доставки:', err);
        }
    };

    if (!delivery) {
        return (
            <Container sx={{ mt: 4 }}>
                <Typography>Загрузка...</Typography>
            </Container>
        );
    }

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Детали доставки
            </Typography>
            <Box sx={{ mb: 2 }}>
                <Typography variant="body1"><b>Газета:</b> {delivery.print_run.newspaper.name}</Typography>
                <Typography variant="body1"><b>Типография:</b> {delivery.printshop.name}</Typography>
                <Typography variant="body1"><b>Почтовое отделение:</b> №{delivery.post_office.number} - {delivery.post_office.address}</Typography>
                <Typography variant="body1"><b>Тираж:</b> {delivery.print_run.quantity}</Typography>
                <Typography variant="body1"><b>Доставлено:</b> {delivery.quantity}</Typography>
                <Typography variant="body1"><b>Дата печати:</b> {new Date(delivery.print_run.date).toLocaleDateString()}</Typography>
            </Box>
            <Button variant="contained" color="primary"sx={{ backgroundColor: '#B0B0B0', color: 'black', mr: 2 }} onClick={() => navigate(`/deliveries/${deliveryId}/edit`)}>
                Редактировать
            </Button>
            <Button variant="outlined" color="error" onClick={handleDelete}>
                Удалить
            </Button>
        </Container>
    );
};

export default DeliveryDetail;