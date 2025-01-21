import React, { useEffect, useState } from 'react';
import { Container, Typography, TextField, Button, Box, FormControlLabel, Checkbox } from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';

interface PrintShop {
    id?: string;
    name: string;
    address: string;
    is_open: boolean;
}

const PrintShopForm: React.FC = () => {
    const { printshopId } = useParams();
    const navigate = useNavigate();

    const [formData, setFormData] = useState<PrintShop>({
        name: '',
        address: '',
        is_open: true,
    });

    const isEdit = !!printshopId;

    useEffect(() => {
        if (isEdit) {
            api.get<PrintShop>(`/printshops/${printshopId}/`)
                .then((res) => setFormData(res.data))
                .catch((err) => console.error('Ошибка при загрузке типографии:', err));
        }
    }, [isEdit, printshopId]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value, type, checked } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value,
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            if (isEdit) {
                await api.put(`/printshops/${printshopId}/`, formData);
            } else {
                await api.post('/printshops/', formData);
            }
            navigate('/printshops');
        } catch (err) {
            console.error('Ошибка при сохранении типографии:', err);
        }
    };

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                {isEdit ? 'Редактировать типографию' : 'Добавить типографию'}
            </Typography>
            <Box component="form" onSubmit={handleSubmit}>
                <TextField
                    name="name"
                    label="Название"
                    value={formData.name}
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
                <FormControlLabel
                    control={
                        <Checkbox
                            name="is_open"
                            checked={formData.is_open}
                            onChange={handleChange}
                            sx={{
                                color: '#B0B0B0',
                                '&.Mui-checked': {
                                    color: '#808080',
                                },
                            }}
                        />
                    }
                    label="Открыта?"
                />
                <Button variant="contained" type="submit"  sx={{ backgroundColor: '#B0B0B0', color: 'black', mr: 2 }}>
                    Сохранить
                </Button>
            </Box>
        </Container>
    );
};

export default PrintShopForm;