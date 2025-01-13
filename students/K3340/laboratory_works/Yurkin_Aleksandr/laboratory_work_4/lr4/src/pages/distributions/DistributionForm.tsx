import React, { useEffect, useState } from 'react';
import { Container, Typography, Button, Box, TextField, FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import { SelectChangeEvent } from '@mui/material/Select';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';

interface NewspaperOption {
    id: string;
    name: string;
}

interface PrintShopOption {
    id: string;
    name: string;
    address: string;
}

interface PostOfficeOption {
    id: string;
    office_number: number;
}

interface DistributionFormData {
    newspaper_id: string;
    printshop_id: string;
    postoffice_id: string;
    copies_printed: number;
    copies_sent: number;
}

const DistributionForm: React.FC = () => {
    const { distributionId } = useParams();
    const navigate = useNavigate();

    const [formData, setFormData] = useState<DistributionFormData>({
        newspaper_id: '',
        printshop_id: '',
        postoffice_id: '',
        copies_printed: 0,
        copies_sent: 0,
    });

    const [newspapers, setNewspapers] = useState<NewspaperOption[]>([]);
    const [printshops, setPrintshops] = useState<PrintShopOption[]>([]);
    const [postoffices, setPostoffices] = useState<PostOfficeOption[]>([]);

    const isEdit = !!distributionId;

    const fetchData = async () => {
        try {
            const [nRes, pRes, poRes] = await Promise.all([
                api.get<NewspaperOption[]>('/newspapers/'),
                api.get<PrintShopOption[]>('/printshops/'),
                api.get<PostOfficeOption[]>('/postoffices/')
            ]);
            setNewspapers(nRes.data);
            setPrintshops(pRes.data);
            setPostoffices(poRes.data);
        } catch (error) {
            console.error('Ошибка при загрузке справочных данных:', error);
        }
    };

    const fetchDistribution = async () => {
        if (!distributionId) return;
        try {
            const res = await api.get(`/distributions/${distributionId}/`);
            const data = res.data;
            setFormData({
                newspaper_id: data.newspaper?.id || '',
                printshop_id: data.printshop?.id || '',
                postoffice_id: data.postoffice?.id || '',
                copies_printed: data.copies_printed,
                copies_sent: data.copies_sent,
            });
        } catch (error) {
            console.error('Ошибка при загрузке распределения:', error);
        }
    };

    useEffect(() => {
        fetchData();
        if (isEdit) {
            fetchDistribution();
        }
    }, [isEdit, distributionId]);

    const handleSelectChange = (e: SelectChangeEvent<string>) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: name === 'copies_printed' || name === 'copies_sent'
                ? parseInt(value, 10)
                : value
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            if (isEdit && distributionId) {
                await api.put(`/distributions/${distributionId}/`, formData);
            } else {
                await api.post('/distributions/', formData);
            }
            navigate('/distributions');
        } catch (error) {
            console.error('Ошибка при сохранении распределения:', error);
        }
    };

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4">
                {isEdit ? 'Редактировать распределение' : 'Добавить распределение'}
            </Typography>
            <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
                {/* Выбор газеты */}
                <FormControl fullWidth margin="normal" required>
                    <InputLabel id="newspaper-label">Газета</InputLabel>
                    <Select
                        labelId="newspaper-label"
                        name="newspaper_id"
                        value={formData.newspaper_id}
                        label="Газета"
                        onChange={handleSelectChange}
                    >
                        {newspapers.map((n) => (
                            <MenuItem key={n.id} value={n.id}>
                                {n.name}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>

                {/* Выбор типографии */}
                <FormControl fullWidth margin="normal" required>
                    <InputLabel id="printshop-label">Типография</InputLabel>
                    <Select
                        labelId="printshop-label"
                        name="printshop_id"
                        value={formData.printshop_id}
                        label="Типография"
                        onChange={handleSelectChange}
                    >
                        {printshops.map((p) => (
                            <MenuItem key={p.id} value={p.id}>
                                {p.name} — {p.address}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>

                {/* Выбор почтового отделения */}
                <FormControl fullWidth margin="normal" required>
                    <InputLabel id="postoffice-label">Почтовое отделение</InputLabel>
                    <Select
                        labelId="postoffice-label"
                        name="postoffice_id"
                        value={formData.postoffice_id}
                        label="Почтовое отделение"
                        onChange={handleSelectChange}
                    >
                        {postoffices.map((po) => (
                            <MenuItem key={po.id} value={po.id}>
                                №{po.office_number} — {po.id}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>

                {/* Поля: copies_printed, copies_sent */}
                <TextField
                    name="copies_printed"
                    label="Тираж"
                    value={formData.copies_printed}
                    onChange={handleInputChange}
                    type="number"
                    fullWidth
                    margin="normal"
                    required
                />
                <TextField
                    name="copies_sent"
                    label="Отправлено"
                    value={formData.copies_sent}
                    onChange={handleInputChange}
                    type="number"
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

export default DistributionForm;
