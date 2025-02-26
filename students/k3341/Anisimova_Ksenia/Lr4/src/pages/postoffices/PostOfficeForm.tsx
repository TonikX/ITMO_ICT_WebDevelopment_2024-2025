import React, { useEffect, useState } from 'react';
import { Container, Typography, TextField, Button, Box } from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';

interface PostOffice {
    id?: string;
    office_number: number;
    address: string;
}

const PostOfficeForm: React.FC = () => {
    const { postofficeId } = useParams();
    const navigate = useNavigate();

    const [formData, setFormData] = useState<PostOffice>({
        office_number: 0,
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
            [e.target.name]: e.target.type === 'number'
                ? parseInt(e.target.value, 10)
                : e.target.value,
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
                {isEdit ? 'Edit Post office' : 'Add Post office'}
            </Typography>
            <Box component="form" onSubmit={handleSubmit}>
                <TextField
                    name="office_number"
                    label="Post office №"
                    type="number"
                    value={formData.office_number}
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
                <Button variant="contained" type="submit" sx={{ mt: 2 }}>
                    Save
                </Button>
            </Box>
        </Container>
    );
};

export default PostOfficeForm;
