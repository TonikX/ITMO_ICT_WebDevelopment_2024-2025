import React, { useEffect, useState } from 'react';
import { Container, Typography, TextField, Button, Box } from '@mui/material';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../../services/api';

interface Editor {
    id?: string;
    name: string;
}

const EditorForm: React.FC = () => {
    const { editorId } = useParams();
    const navigate = useNavigate();

    const [editorData, setEditorData] = useState<Editor>({
        name: '',
    });

    const isEditMode = !!editorId;

    useEffect(() => {
        if (isEditMode) {
            api.get<Editor>(`/editors/${editorId}/`)
                .then((response) => setEditorData(response.data))
                .catch((error) => console.error('Ошибка при загрузке редактора:', error));
        }
    }, [isEditMode, editorId]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setEditorData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            if (isEditMode) {
                await api.put(`/editors/${editorId}/`, editorData);
            } else {
                await api.post('/editors/', editorData);
            }
            navigate('/editors');
        } catch (error) {
            console.error('Ошибка при сохранении редактора:', error);
        }
    };

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                {isEditMode ? 'Редактировать редактора' : 'Добавить редактора'}
            </Typography>
            <Box component="form" onSubmit={handleSubmit}>
                <TextField
                    name="name"
                    label="ФИО редактора"
                    value={editorData.name}
                    onChange={handleChange}
                    fullWidth
                    margin="normal"
                    required
                />
                <Button variant="contained" type="submit" sx={{ mt: 2 }}>
                    Сохранить
                </Button>
            </Box>
        </Container>
    );
};

export default EditorForm;
