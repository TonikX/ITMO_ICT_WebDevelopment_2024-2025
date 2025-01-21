import React, { useEffect, useState } from 'react';
import { Container, Typography, TextField, Button, Box } from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';

interface PostOffice {
    id?: number;
    number: string;
    address: string;
}

const PostOfficeForm: React.FC = () => {
    const { postofficeId } = useParams();
    const navigate = useNavigate();

    const [formData, setFormData] = useState<PostOffice>({
        number: '',
        address: '',
    });

    const isEdit = !!postofficeId;

    useEffect(() => {
        if (isEdit) {
            api.get<PostOffice>(`/postoffices/${postofficeId}/`)
                .then((res) => setFormData(res.data))
                .catch((err) => console.error('Ошибка при загрузке отделения:', err));
        }
    }, [isEdit, postofficeId]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData((prev) => ({
            ...prev,
            [e.target.name]: e.target.value,
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            if (isEdit) {
                await api.put(`/postoffices/${postofficeId}/`, formData);
            } else {
                await api.post('/postoffices/', formData);
            }
            navigate('/postoffices');
        } catch (err) {
            console.error('Ошибка при сохранении отделения:', err);
        }
    };

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                {isEdit ? 'Редактировать отделение' : 'Добавить отделение'}
            </Typography>
            <Box component="form" onSubmit={handleSubmit}>
                <TextField
                    name="number"
                    label="Номер отделения"
                    value={formData.number}
                    onChange={handleChange}
                    fullWidth
                    margin="normal"
                    required
                />
                <TextField
                    name="address"
                    label="Адрес"
                    value={formData.address}
                    onChange={handleChange}
                    fullWidth
                    margin="normal"
                    required
                />
                <Button variant="contained" type="submit" sx={{ backgroundColor: '#B0B0B0', color: 'black', mr: 2 }}>
                    Сохранить
                </Button>
            </Box>
        </Container>
    );
};

export default PostOfficeForm;