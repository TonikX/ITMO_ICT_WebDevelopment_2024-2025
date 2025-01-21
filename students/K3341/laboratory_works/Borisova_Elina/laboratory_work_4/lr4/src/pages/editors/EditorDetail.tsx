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

    const getFullName = (editor: Editor) => {
        return `${editor.last_name} ${editor.first_name} ${editor.patronymic || ''}`.trim();
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
                <Typography variant="body1"><b>ФИО:</b> {getFullName(editor)}</Typography>
            </Box>
            <Button
                variant="contained"
                color="primary"
                sx={{ backgroundColor: '#B0B0B0', color: 'black', mr: 2 }}
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