import React, { useEffect, useState } from 'react';
import { Container, Typography, Button, Box } from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';

interface PostOffice {
    id: number;
    number: string;
    address: string;
}

const PostOfficeDetail: React.FC = () => {
    const { postofficeId } = useParams();
    const navigate = useNavigate();
    const [office, setOffice] = useState<PostOffice | null>(null);

    useEffect(() => {
        if (postofficeId) {
            api.get<PostOffice>(`/postoffices/${postofficeId}/`)
                .then((res) => setOffice(res.data))
                .catch((err) => console.error('Ошибка при загрузке отделения:', err));
        }
    }, [postofficeId]);

    const handleDelete = async () => {
        if (!postofficeId) return;
        try {
            await api.delete(`/postoffices/${postofficeId}/`);
            navigate('/postoffices');
        } catch (err) {
            console.error('Ошибка при удалении отделения:', err);
        }
    };

    if (!office) {
        return (
            <Container sx={{ mt: 4 }}>
                <Typography>Загрузка...</Typography>
            </Container>
        );
    }

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Детали отделения
            </Typography>
            <Box sx={{ mb: 2 }}>
                <Typography variant="body1"><b>ID:</b> {office.id}</Typography>
                <Typography variant="body1"><b>Номер почтового отделения:</b> {office.number}</Typography>
                <Typography variant="body1"><b>Адрес:</b> {office.address}</Typography>
            </Box>
            <Button
                variant="contained"
                color="primary"
                sx={{ mr: 2 }}
                onClick={() => navigate(`/postoffices/${postofficeId}/edit`)}
            >
                Редактировать
            </Button>
            <Button variant="outlined" color="error" onClick={handleDelete}>
                Удалить
            </Button>
        </Container>
    );
};

export default PostOfficeDetail;