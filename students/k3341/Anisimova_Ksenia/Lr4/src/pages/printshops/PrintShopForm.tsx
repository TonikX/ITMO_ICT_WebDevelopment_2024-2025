import React, { useEffect, useState } from 'react';
import { Container, Typography, TextField, Button, Box, FormControlLabel, Checkbox } from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';

interface PrintShop {
    id?: string;
    name: string;
    address: string;
    is_closed: boolean;
}

const PrintShopForm: React.FC = () => {
    const { printshopId } = useParams();
    const navigate = useNavigate();

    const [formData, setFormData] = useState<PrintShop>({
        name: '',
        address: '',
        is_closed: false,
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
                {isEdit ? 'Edit Print shop' : 'Add Print shop'}
            </Typography>
            <Box component="form" onSubmit={handleSubmit}>
                <TextField
                    name="name"
                    label="Name"
                    value={formData.name}
                    onChange={handleChange}
                    fullWidth
                    margin="normal"
                    required
                />
                <TextField
                    name="address"
                    label="Address"
                    value={formData.address}
                    onChange={handleChange}
                    fullWidth
                    margin="normal"
                    required
                />
                <FormControlLabel
                    control={
                        <Checkbox
                            name="is_closed"
                            checked={formData.is_closed}
                            onChange={handleChange}
                        />
                    }
                    label="Closed?"
                />
                <Button variant="contained" type="submit" sx={{ mt: 2 }}>
                    Save
                </Button>
            </Box>
        </Container>
    );
};

export default PrintShopForm;
