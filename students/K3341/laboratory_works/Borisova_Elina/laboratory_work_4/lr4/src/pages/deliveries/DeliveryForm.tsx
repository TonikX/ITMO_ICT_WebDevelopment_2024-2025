import React, { useEffect, useState } from 'react';
import {
    Container, Typography, Button, Box, TextField,
    FormControl, InputLabel, Select, MenuItem
} from '@mui/material';
import { SelectChangeEvent } from '@mui/material/Select';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';

// Интерфейсы данных
interface PrintRunOption {
    id: string;
    newspaper: {
        name: string;
    };
    quantity: number;
}

interface PrintShopOption {
    id: string;
    name: string;
    address: string;
}

interface PostOfficeOption {
    id: string;
    number: string;
    address: string;
}

// Интерфейс формы доставки
interface DeliveryFormData {
    print_run_id: string;
    post_office_id: string;
    printshop_id: string;
    quantity: number;
}

const DeliveryForm: React.FC = () => {
    const { deliveryId } = useParams();
    const navigate = useNavigate();

    const [formData, setFormData] = useState<DeliveryFormData>({
        print_run_id: '',
        post_office_id: '',
        printshop_id: '',
        quantity: 0,
    });

    const [printRuns, setPrintRuns] = useState<PrintRunOption[]>([]);
    const [printshops, setPrintshops] = useState<PrintShopOption[]>([]);
    const [postoffices, setPostoffices] = useState<PostOfficeOption[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const isEdit = !!deliveryId;

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const [prRes, pRes, poRes] = await Promise.all([
                    api.get<PrintRunOption[]>('/printruns/'),
                    api.get<PrintShopOption[]>('/printshops/'),
                    api.get<PostOfficeOption[]>('/postoffices/')
                ]);
                setPrintRuns(prRes.data);
                setPrintshops(pRes.data);
                setPostoffices(poRes.data);

                if (isEdit) {
                    const res = await api.get<DeliveryFormData>(`/deliveries/${deliveryId}/`);
                    setFormData(res.data);
                }
            } catch (error) {
                console.error('Ошибка при загрузке данных:', error);
                setError('Не удалось загрузить данные.');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [isEdit, deliveryId]);

    // Обработчик для `TextField`
    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: name === 'quantity' ? parseInt(value, 10) || 0 : value
        }));
    };

    // Обработчик для `Select`
    const handleSelectChange = (e: SelectChangeEvent<string>) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            if (isEdit && deliveryId) {
                await api.put(`/deliveries/${deliveryId}/`, formData);
            } else {
                await api.post('/deliveries/', formData);
            }
            navigate('/deliveries');
        } catch (error) {
            console.error('Ошибка при сохранении доставки:', error);
            setError('Ошибка при сохранении доставки.');
        }
    };

    if (loading) {
        return <Typography variant="h6">Загрузка...</Typography>;
    }

    if (error) {
        return <Typography variant="h6" color="error">{error}</Typography>;
    }

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4">
                {isEdit ? 'Редактировать доставку' : 'Добавить доставку'}
            </Typography>
            <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
                {/* Выбор Тиража (PrintRun) */}
                <FormControl fullWidth margin="normal" required>
                    <InputLabel id="print_run-label">Тираж</InputLabel>
                    <Select
                        labelId="print_run-label"
                        name="print_run_id"
                        value={formData.print_run_id}
                        onChange={handleSelectChange}
                    >
                        {printRuns.map((pr) => (
                            <MenuItem key={pr.id} value={pr.id}>
                                {pr.newspaper.name} — {pr.quantity} экземпляров
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>

                <FormControl fullWidth margin="normal" required>
                    <InputLabel id="post_office-label">Почтовое отделение</InputLabel>
                    <Select
                        labelId="post_office-label"
                        name="post_office_id"
                        value={formData.post_office_id}
                        onChange={handleSelectChange}
                    >
                        {postoffices.map((po) => (
                            <MenuItem key={po.id} value={po.id}>
                                №{po.number} — {po.address}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>

                {/* Выбор Типографии */}
                <FormControl fullWidth margin="normal" required>
                    <InputLabel id="printshop-label">Типография</InputLabel>
                    <Select
                        labelId="printshop-label"
                        name="printshop_id"
                        value={formData.printshop_id}
                        onChange={handleSelectChange}
                    >
                        {printshops.map((p) => (
                            <MenuItem key={p.id} value={p.id}>
                                {p.name} — {p.address}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>

                {/* Поле Количества */}
                <TextField
                    name="quantity"
                    label="Количество экземпляров"
                    type="number"
                    value={formData.quantity}
                    onChange={handleInputChange}
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

export default DeliveryForm;