import React, { useEffect, useState } from 'react';
import {
    Container,
    Typography,
    TextField,
    Button,
    Box,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
} from '@mui/material';
import { SelectChangeEvent } from '@mui/material/Select';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';

interface Editor {
    id: string;
    name: string;
    created_at: string;
    updated_at: string;
}

interface Newspaper {
    id?: string;
    name: string;
    index: string;
    price: string;
    price_updated_at?: string;
    editor_id?: string;
    editor?: Editor;
}

const NewspaperForm: React.FC = () => {
    const { newspaperId } = useParams();
    const navigate = useNavigate();

    const [formData, setFormData] = useState<Newspaper>({
        name: '',
        index: '',
        price: '',
        editor_id: '',
    });

    const [editors, setEditors] = useState<Editor[]>([]);

    const isEdit = !!newspaperId;

    useEffect(() => {
        fetchEditors();
        if (isEdit) {
            fetchNewspaper();
        }
    }, [isEdit, newspaperId]);

    const fetchEditors = async () => {
        try {
            const response = await api.get<Editor[]>('/editors/');
            setEditors(response.data);
        } catch (error) {
            console.error('Ошибка при загрузке редакторов:', error);
        }
    };

    const fetchNewspaper = async () => {
        try {
            if (newspaperId) {
                const res = await api.get<Newspaper>(`/newspapers/${newspaperId}/`);
                const data = res.data;
                setFormData({
                    ...data,
                    editor_id: data?.editor_id || data?.editor?.id || '',
                });
            }
        } catch (err) {
            console.error('Ошибка при загрузке газеты:', err);
        }
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSelectChange = (e: SelectChangeEvent<string>) => {
        const value = e.target.value;
        setFormData((prev) => ({ ...prev, editor_id: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            if (isEdit && newspaperId) {
                await api.put(`/newspapers/${newspaperId}/`, {
                    ...formData,
                    price_updated_at: new Date().toISOString(),
                    editor_id: formData.editor_id,
                });
            } else {
                await api.post('/newspapers/', {
                    ...formData,
                    price_updated_at: new Date().toISOString(),
                    editor_id: formData.editor_id,
                });
            }
            navigate('/newspapers');
        } catch (err) {
            console.error('Ошибка при сохранении газеты:', err);
        }
    };

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                {isEdit ? 'Редактировать газету' : 'Добавить газету'}
            </Typography>
            <Box component="form" onSubmit={handleSubmit}>
                <TextField
                    name="name"
                    label="Название газеты"
                    value={formData.name}
                    onChange={handleInputChange}
                    fullWidth
                    margin="normal"
                    required
                />

                <TextField
                    name="index"
                    label="Индекс"
                    value={formData.index}
                    onChange={handleInputChange}
                    fullWidth
                    margin="normal"
                    required
                />

                <TextField
                    name="price"
                    label="Цена"
                    value={formData.price}
                    onChange={handleInputChange}
                    fullWidth
                    margin="normal"
                    required
                />

                <FormControl fullWidth margin="normal" required>
                    <InputLabel id="editor-select-label">Редактор</InputLabel>
                    <Select
                        labelId="editor-select-label"
                        value={formData.editor_id || ''}
                        label="Редактор"
                        onChange={handleSelectChange}
                        name="editor_id"
                    >
                        <MenuItem value="">
                            <em>Не выбран</em>
                        </MenuItem>
                        {editors.map((ed) => (
                            <MenuItem key={ed.id} value={ed.id}>
                                {ed.name}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>

                <Button variant="contained" type="submit" sx={{ mt: 2 }}>
                    Сохранить
                </Button>
            </Box>
        </Container>
    );
};

export default NewspaperForm;
