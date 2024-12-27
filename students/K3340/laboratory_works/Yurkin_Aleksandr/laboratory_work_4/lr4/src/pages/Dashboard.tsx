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

import {
    BarChart,
    Bar,
    PieChart,
    Pie,
    Cell,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid,
    ResponsiveContainer,
    Legend,
} from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#C71585', '#6A5ACD'];

const Dashboard: React.FC = () => {
    const [newspaperName, setNewspaperName] = useState('');
    const [addresses, setAddresses] = useState<string[]>([]);

    const [quantity, setQuantity] = useState('');
    const [lowCirculationData, setLowCirculationData] = useState<any[]>([]);

    const [price, setPrice] = useState('');
    const [expensiveOffices, setExpensiveOffices] = useState<string[]>([]);

    const [printshopId, setPrintshopId] = useState('');
    const [largestEditorSurname, setLargestEditorSurname] = useState<string | null>(null);

    const [ndName, setNdName] = useState('');
    const [ndAddress, setNdAddress] = useState('');
    const [postOfficesResults, setPostOfficesResults] = useState<any[]>([]);

    const handleCheckAddresses = async () => {
        try {
            const res = await api.get(`/distributions/newspapers_printed_at_address?newspaper_name=${newspaperName}`);

            setAddresses(res.data.addresses || []);
        } catch (error) {
            console.error('Ошибка при запросе newspapers_printed_at_address:', error);
        }
    };

    const handleLowCirculation = async () => {
        try {
            const res = await api.get(`/distributions/newspapers_with_low_circulation?quantity=${quantity}`);
            const chartData = (res.data.results || []).map((item: any) => ({
                newspaper: item.newspaper__name,
                office: `№${item.postoffice__office_number}`,
                copies: item.copies_sent,
            }));
            setLowCirculationData(chartData);
        } catch (error) {
            console.error('Ошибка при запросе newspapers_with_low_circulation:', error);
        }
    };

    const handleExpensiveOffices = async () => {
        try {
            const res = await api.get(`/distributions/post_offices_receiving_expensive_newspapers?price=${price}`);
            setExpensiveOffices(res.data.addresses || []);
        } catch (error) {
            console.error('Ошибка при запросе expensive_newspapers:', error);
        }
    };

    const handleLargestEditor = async () => {
        try {
            const res = await api.get(`/distributions/editor_with_largest_circulation?printshop_id=${printshopId}`);

            if (res.data.editor_surname) {
                setLargestEditorSurname(res.data.editor_surname);
            } else if (res.data.error) {
                setLargestEditorSurname(null);
                alert(res.data.error);
            }
        } catch (error) {
            console.error('Ошибка при запросе editor_with_largest_circulation:', error);
        }
    };

    const handleDistributionAtAddress = async () => {
        try {
            const res = await api.get(
                `/distributions/newspaper_distribution_at_address?newspaper_name=${ndName}&printshop_address=${ndAddress}`
            );

            setPostOfficesResults(res.data.post_offices || []);
        } catch (error) {
            console.error('Ошибка при запросе newspaper_distribution_at_address:', error);
        }
    };

    const pieData = lowCirculationData.map((item) => ({
        name: item.newspaper,
        value: item.copies,
    }));

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Dashboard (Статистика Распределения)
            </Typography>

            <Grid container spacing={4}>
                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6">Адреса типографий, печатающих газету</Typography>
                        <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                            <TextField
                                label="Название газеты"
                                value={newspaperName}
                                onChange={(e) => setNewspaperName(e.target.value)}
                            />
                            <Button variant="contained" onClick={handleCheckAddresses}>
                                Проверить
                            </Button>
                        </Box>
                        {addresses.length > 0 && (
                            <Box sx={{ mt: 2 }}>
                                <Typography>Результат (типографии):</Typography>
                                <List>
                                    {addresses.map((addr) => (
                                        <ListItem key={addr}>
                                            <ListItemText primary={addr} />
                                        </ListItem>
                                    ))}
                                </List>
                            </Box>
                        )}
                    </Paper>
                </Grid>

                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6">Газеты с малым тиражом (quantity)</Typography>
                        <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                            <TextField
                                label="Макс. отправлено"
                                type="number"
                                value={quantity}
                                onChange={(e) => setQuantity(e.target.value)}
                            />
                            <Button variant="contained" onClick={handleLowCirculation}>
                                Показать
                            </Button>
                        </Box>

                        {lowCirculationData.length > 0 && (
                            <React.Fragment>
                                <Typography variant="body1" sx={{ mt: 2 }}>
                                    Результаты: (Газета / Почтовое отделение / copies)
                                </Typography>

                                <List>
                                    {lowCirculationData.map((item, i) => (
                                        <ListItem key={i}>
                                            <ListItemText
                                                primary={`Газета: ${item.newspaper}, Отделение: ${item.office}, copies: ${item.copies}`}
                                            />
                                        </ListItem>
                                    ))}
                                </List>

                                <Box sx={{ mt: 2, height: 250 }}>
                                    <ResponsiveContainer width="100%" height="100%">
                                        <BarChart data={lowCirculationData}>
                                            <CartesianGrid strokeDasharray="3 3" />
                                            <XAxis dataKey="newspaper" />
                                            <YAxis />
                                            <Tooltip />
                                            <Legend />
                                            <Bar dataKey="copies" fill="#8884d8" />
                                        </BarChart>
                                    </ResponsiveContainer>
                                </Box>

                                <Box sx={{ mt: 2, height: 250 }}>
                                    <ResponsiveContainer width="100%" height="100%">
                                        <PieChart>
                                            <Pie
                                                data={pieData}
                                                dataKey="value"
                                                nameKey="name"
                                                cx="50%"
                                                cy="50%"
                                                outerRadius={80}
                                                label
                                            >
                                                {pieData.map((entry, index) => (
                                                    <Cell
                                                        key={`cell-${index}`}
                                                        fill={COLORS[index % COLORS.length]}
                                                    />
                                                ))}
                                            </Pie>
                                            <Tooltip />
                                            <Legend />
                                        </PieChart>
                                    </ResponsiveContainer>
                                </Box>
                            </React.Fragment>
                        )}
                    </Paper>
                </Grid>

                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6">Почтовые отделения, получающие газеты дороже price</Typography>
                        <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                            <TextField
                                label="Цена (price)"
                                type="number"
                                value={price}
                                onChange={(e) => setPrice(e.target.value)}
                            />
                            <Button variant="contained" onClick={handleExpensiveOffices}>
                                Найти
                            </Button>
                        </Box>
                        {expensiveOffices.length > 0 && (
                            <Box sx={{ mt: 2 }}>
                                <Typography>Результат (почтовые адреса):</Typography>
                                <List>
                                    {expensiveOffices.map((addr) => (
                                        <ListItem key={addr}>
                                            <ListItemText primary={addr} />
                                        </ListItem>
                                    ))}
                                </List>
                            </Box>
                        )}
                    </Paper>
                </Grid>

                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6">Редактор с максимальным тиражом (printshop_id)</Typography>
                        <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                            <TextField
                                label="PrintShop ID"
                                value={printshopId}
                                onChange={(e) => setPrintshopId(e.target.value)}
                            />
                            <Button variant="contained" onClick={handleLargestEditor}>
                                Найти
                            </Button>
                        </Box>
                        {largestEditorSurname && (
                            <Box sx={{ mt: 2 }}>
                                <Typography>
                                    Редактор с максимальным тиражом: <b>{largestEditorSurname}</b>
                                </Typography>
                            </Box>
                        )}
                    </Paper>
                </Grid>

                <Grid item xs={12} md={12}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6">Куда уходит газета "X" из типографии "Y"</Typography>
                        <Box sx={{ display: 'flex', gap: 2, mt: 2, flexWrap: 'wrap' }}>
                            <TextField
                                label="Название газеты (newspaper_name)"
                                value={ndName}
                                onChange={(e) => setNdName(e.target.value)}
                            />
                            <TextField
                                label="Адрес типографии (printshop_address)"
                                value={ndAddress}
                                onChange={(e) => setNdAddress(e.target.value)}
                            />
                            <Button variant="contained" onClick={handleDistributionAtAddress}>
                                Показать
                            </Button>
                        </Box>
                        {postOfficesResults.length > 0 && (
                            <Box sx={{ mt: 2 }}>
                                <Typography>Список почтовых отделений:</Typography>
                                <List>
                                    {postOfficesResults.map((po, i) => (
                                        <ListItem key={i}>
                                            <ListItemText
                                                primary={`Отделение №${po.postoffice__office_number}, Адрес: ${po.postoffice__address}`}
                                            />
                                        </ListItem>
                                    ))}
                                </List>
                            </Box>
                        )}
                    </Paper>
                </Grid>
            </Grid>
        </Container>
    );
};

export default Dashboard;
