import React, { useEffect, useState } from 'react';
import { Container, Typography, Button, Box } from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';

interface Editor {
    id: number;
    first_name: string;
    last_name: string;
    patronymic?: string;
}

interface Newspaper {
    id: number;
    name: string;
    index: string;
    price: number;
    editor: Editor;
}

const NewspaperDetail: React.FC = () => {
    const { newspaperId } = useParams();
    const navigate = useNavigate();
    const [newspaper, setNewspaper] = useState<Newspaper | null>(null);

    useEffect(() => {
        if (newspaperId) {
            api.get<Newspaper>(`/newspapers/${newspaperId}/`)
                .then((res) => setNewspaper(res.data))
                .catch((err) => console.error('Ошибка при загрузке газеты:', err));
        }
    }, [newspaperId]);

    const handleDelete = async () => {
        if (!newspaperId) return;
        try {
            await api.delete(`/newspapers/${newspaperId}/`);
            navigate('/newspapers');
        } catch (err) {
            console.error('Ошибка при удалении газеты:', err);
        }
    };

    if (!newspaper) {
        return (
            <Container sx={{ mt: 4 }}>
                <Typography>Загрузка...</Typography>
            </Container>
        );
    }

    const getEditorFullName = (editor: Editor) => {
        return `${editor.last_name} ${editor.first_name} ${editor.patronymic || ''}`.trim();
    };

    const { editor } = newspaper;

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Детали газеты
            </Typography>
            <Box sx={{ mb: 2 }}>
                <Typography variant="body1"><b>ID:</b> {newspaper.id}</Typography>
                <Typography variant="body1"><b>Название:</b> {newspaper.name}</Typography>
                <Typography variant="body1"><b>Индекс:</b> {newspaper.index}</Typography>
                <Typography variant="body1"><b>Цена:</b> {newspaper.price.toFixed(2)}</Typography>

                {editor && (
                    <Box sx={{ mt: 2 }}>
                        <Typography variant="h6">Информация о редакторе:</Typography>
                        <Typography variant="body1"><b>Редактор ID:</b> {editor.id}</Typography>
                        <Typography variant="body1"><b>ФИО:</b> {getEditorFullName(editor)}</Typography>
                    </Box>
                )}
            </Box>
            <Button
                variant="contained"
                color="primary"
                sx={{ mr: 2 }}
                onClick={() => navigate(`/newspapers/${newspaperId}/edit`)}
            >
                Редактировать
            </Button>
            <Button variant="outlined" color="error" onClick={handleDelete}>
                Удалить
            </Button>
        </Container>
    );
};

export default NewspaperDetail;