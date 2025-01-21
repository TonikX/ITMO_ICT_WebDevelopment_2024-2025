import React, { useEffect, useState } from 'react';
import { Container, Typography, Button, Box } from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';

interface Editor {
    id: string;
    name: string;
    created_at: string;
    updated_at: string;
}

const EditorDetail: React.FC = () => {
    const { editorId } = useParams();
    const navigate = useNavigate();
    const [editor, setEditor] = useState<Editor | null>(null);

    useEffect(() => {
        if (editorId) {
            api.get<Editor>(`/editors/${editorId}/`)
                .then((response) => setEditor(response.data))
                .catch((error) => console.error('Ошибка при загрузке редактора:', error));
        }
    }, [editorId]);

    const handleDelete = async () => {
        if (!editorId) return;
        try {
            await api.delete(`/editors/${editorId}/`);
            navigate('/editors');
        } catch (error) {
            console.error('Ошибка при удалении редактора:', error);
        }
    };

    if (!editor) {
        return (
            <Container sx={{ mt: 4 }}>
                <Typography>Загрузка...</Typography>
            </Container>
        );
    }

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Детали редактора
            </Typography>
            <Box sx={{ mb: 2 }}>
                <Typography variant="body1"><b>ID:</b> {editor.id}</Typography>
                <Typography variant="body1"><b>ФИО:</b> {editor.name}</Typography>
                <Typography variant="body1"><b>Дата добавления:</b> {new Date(editor.created_at).toLocaleString()}</Typography>
                <Typography variant="body1"><b>Дата обновления:</b> {new Date(editor.updated_at).toLocaleString()}</Typography>
            </Box>
            <Button
                variant="contained"
                color="primary"
                sx={{ mr: 2 }}
                onClick={() => navigate(`/editors/${editorId}/edit`)}
            >
                Редактировать
            </Button>
            <Button variant="outlined" color="error" onClick={handleDelete}>
                Удалить
            </Button>
        </Container>
    );
};

export default EditorDetail;
