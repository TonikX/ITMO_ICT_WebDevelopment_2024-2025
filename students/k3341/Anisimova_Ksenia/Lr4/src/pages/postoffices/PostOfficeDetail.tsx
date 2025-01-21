import React, { useEffect, useState } from 'react';
import { Container, Typography, Button, Box } from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';

interface PostOffice {
    id: string;
    office_number: number;
    address: string;
    created_at: string;
    updated_at: string;
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
                <Typography>Loading...</Typography>
            </Container>
        );
    }

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Post office details
            </Typography>
            <Box sx={{ mb: 2 }}>
                <Typography variant="body1"><b>ID:</b> {office.id}</Typography>
                <Typography variant="body1"><b>Post office №:</b> {office.office_number}</Typography>
                <Typography variant="body1"><b>Address:</b> {office.address}</Typography>
                <Typography variant="body1"><b>Created:</b> {new Date(office.created_at).toLocaleString()}</Typography>
                <Typography variant="body1"><b>Updated:</b> {new Date(office.updated_at).toLocaleString()}</Typography>
            </Box>
            <Button
                variant="contained"
                color="primary"
                sx={{ mr: 2 }}
                onClick={() => navigate(`/postoffices/${postofficeId}/edit`)}
            >
                Edit
            </Button>
            <Button variant="outlined" color="error" onClick={handleDelete}>
                Delete
            </Button>
        </Container>
    );
};

export default PostOfficeDetail;
