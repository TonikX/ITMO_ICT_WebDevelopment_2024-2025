import React, { useState } from 'react';
import {
    Container,
    Typography,
    TextField,
    Button,
    Box,
    Paper,
    Grid,
    List,
    ListItem,
    ListItemText,
} from '@mui/material';
import api from '../services/api';

const Dashboard: React.FC = () => {
    const [newspaperId, setNewspaperId] = useState('');
    const [totalPrints, setTotalPrints] = useState<number | null>(null);

    const [quantity, setQuantity] = useState('');
    const [lowCirculationData, setLowCirculationData] = useState<any[]>([]);

    const [price, setPrice] = useState('');
    const [expensiveOffices, setExpensiveOffices] = useState<string[]>([]);

    const [newspaperName, setNewspaperName] = useState('');
    const [printshopId, setPrintshopId] = useState('');
    const [postOfficeResults, setPostOfficeResults] = useState<any[]>([]);

    const handleTotalPrints = async () => {
        try {
            const res = await api.get(`/printruns/total_prints_for_newspaper?newspaper_id=${newspaperId}`);
            setTotalPrints(res.data.total_prints);
        } catch (error) {
            console.error('Ошибка при получении общего тиража:', error);
        }
    };

    const handleLowCirculation = async () => {
        try {
            const res = await api.get(`/deliveries/newspapers_with_low_circulation?quantity=${quantity}`);
            const chartData = (res.data.results || []).map((item: any) => ({
                newspaper: item.print_run__newspaper__name,
                office: `№${item.post_office__number}`,
                copies: item.quantity,
            }));
            setLowCirculationData(chartData);
        } catch (error) {
            console.error('Ошибка при загрузке газет с малым тиражом:', error);
        }
    };

    const handleExpensiveOffices = async () => {
        try {
            const res = await api.get(`/deliveries/post_offices_receiving_expensive_newspapers?price=${price}`);
            setExpensiveOffices(res.data.addresses || []);
        } catch (error) {
            console.error('Ошибка при загрузке почтовых отделений:', error);
        }
    };

    const handleNewspaperDistribution = async () => {
        try {
            const res = await api.get(
                `/deliveries/newspaper_distribution?newspaper_name=${newspaperName}&printshop_id=${printshopId}`
            );
            setPostOfficeResults(res.data.results || []);
        } catch (error) {
            console.error('Ошибка при загрузке распределения газет:', error);
        }
    };

    return (
        <Container sx={{ mt: 4, backgroundColor: '#b9b9b9', minHeight: '100vh', py: 4 }}>
            <Typography variant="h4" gutterBottom>
                Дашборд
            </Typography>

            <Grid container spacing={4}>
                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6">Общий тираж газеты</Typography>
                        <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                            <TextField
                                label="ID газеты"
                                type="number"
                                value={newspaperId}
                                onChange={(e) => setNewspaperId(e.target.value)}
                            />
                            <Button variant="contained"
                                sx={{ backgroundColor: '#B0B0B0', color: 'black' }}
                                onClick={handleTotalPrints}>
                                Показать
                            </Button>
                        </Box>
                        {totalPrints !== null && (
                            <Typography sx={{ mt: 2 }}>
                                <b>Общий тираж:</b> {totalPrints} экземпляров
                            </Typography>
                        )}
                    </Paper>
                </Grid>

                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6">Газеты с малым тиражом</Typography>
                        <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                            <TextField
                                label="Макс. отправлено"
                                type="number"
                                value={quantity}
                                onChange={(e) => setQuantity(e.target.value)}
                            />
                            <Button variant="contained"
                                sx={{ backgroundColor: '#B0B0B0', color: 'black' }}
                                onClick={handleLowCirculation}>
                                Показать
                            </Button>
                        </Box>

                        {lowCirculationData.length > 0 && (
                            <List sx={{ mt: 2 }}>
                                {lowCirculationData.map((item, i) => (
                                    <ListItem key={i}>
                                        <ListItemText
                                            primary={`Газета: ${item.newspaper}, Почта: ${item.office}, Экз: ${item.copies}`}
                                        />
                                    </ListItem>
                                ))}
                            </List>
                        )}
                    </Paper>
                </Grid>

                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6">Почтовые отделения, получающие газеты дороже указанной цены</Typography>
                        <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                            <TextField
                                label="Цена (руб.)"
                                type="number"
                                value={price}
                                onChange={(e) => setPrice(e.target.value)}
                            />
                            <Button variant="contained"
                                sx={{ backgroundColor: '#B0B0B0', color: 'black' }}
                                onClick={handleExpensiveOffices}>
                                Найти
                            </Button>
                        </Box>
                        {expensiveOffices.length > 0 && (
                            <List sx={{ mt: 2 }}>
                                {expensiveOffices.map((addr) => (
                                    <ListItem key={addr}>
                                        <ListItemText primary={addr} />
                                    </ListItem>
                                ))}
                            </List>
                        )}
                    </Paper>
                </Grid>

                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6">Куда отправляются газеты</Typography>
                        <Box sx={{ display: 'flex', gap: 2, mt: 2, flexWrap: 'wrap' }}>
                            <TextField
                                label="Название газеты"
                                value={newspaperName}
                                onChange={(e) => setNewspaperName(e.target.value)}
                            />
                            <TextField
                                label="ID типографии"
                                value={printshopId}
                                onChange={(e) => setPrintshopId(e.target.value)}
                            />
                            <Button variant="contained"
                                sx={{ backgroundColor: '#B0B0B0', color: 'black' }}
                                onClick={handleNewspaperDistribution}>
                                Показать
                            </Button>
                        </Box>
                        {postOfficeResults.length > 0 && (
                            <List sx={{ mt: 2 }}>
                                {postOfficeResults.map((po, i) => (
                                    <ListItem key={i}>
                                        <ListItemText
                                            primary={`Отделение №${po.post_office__number}, Адрес: ${po.post_office__address}, Экз: ${po.quantity}`}
                                        />
                                    </ListItem>
                                ))}
                            </List>
                        )}
                    </Paper>
                </Grid>
            </Grid>
        </Container>
    );
};

export default Dashboard;