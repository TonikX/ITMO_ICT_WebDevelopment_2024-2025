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
            console.error('Error fetching newspapers printed at address:', error);
        }
    };

    const handleLowCirculation = async () => {
        try {
            const res = await api.get(`/distributions/newspapers_with_low_circulation?quantity=${quantity}`);
            const chartData = (res.data.results || []).map((item: any) => ({
                newspaper: item.newspaper__name,
                office: `No.${item.postoffice__office_number}`,
                copies: item.copies_sent,
            }));
            setLowCirculationData(chartData);
        } catch (error) {
            console.error('Error fetching newspapers with low circulation:', error);
        }
    };

    const handleExpensiveOffices = async () => {
        try {
            const res = await api.get(`/distributions/post_offices_receiving_expensive_newspapers?price=${price}`);
            setExpensiveOffices(res.data.addresses || []);
        } catch (error) {
            console.error('Error fetching expensive newspapers:', error);
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
            console.error('Error fetching editor with largest circulation:', error);
        }
    };

    const handleDistributionAtAddress = async () => {
        try {
            const res = await api.get(
                `/distributions/newspaper_distribution_at_address?newspaper_name=${ndName}&printshop_address=${ndAddress}`
            );

            setPostOfficesResults(res.data.post_offices || []);
        } catch (error) {
            console.error('Error fetching newspaper distribution at address:', error);
        }
    };

    const pieData = lowCirculationData.map((item) => ({
        name: item.newspaper,
        value: item.copies,
    }));

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Dashboard (Distribution Statistics)
            </Typography>

            <Grid container spacing={4}>
                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6">Addresses of print shops printing the newspaper</Typography>
                        <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                            <TextField
                                label="Newspaper Name"
                                value={newspaperName}
                                onChange={(e) => setNewspaperName(e.target.value)}
                            />
                            <Button variant="contained" onClick={handleCheckAddresses}>
                                Check
                            </Button>
                        </Box>
                        {addresses.length > 0 && (
                            <Box sx={{ mt: 2 }}>
                                <Typography>Result (Print Shops):</Typography>
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
                        <Typography variant="h6">Newspapers with low circulation (quantity)</Typography>
                        <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                            <TextField
                                label="Max Sent Copies"
                                type="number"
                                value={quantity}
                                onChange={(e) => setQuantity(e.target.value)}
                            />
                            <Button variant="contained" onClick={handleLowCirculation}>
                                Show
                            </Button>
                        </Box>

                        {lowCirculationData.length > 0 && (
                            <React.Fragment>
                                <Typography variant="body1" sx={{ mt: 2 }}>
                                    Results: (Newspaper / Post Office / Copies)
                                </Typography>

                                <List>
                                    {lowCirculationData.map((item, i) => (
                                        <ListItem key={i}>
                                            <ListItemText
                                                primary={`Newspaper: ${item.newspaper}, Office: ${item.office}, Copies: ${item.copies}`}
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
                        <Typography variant="h6">Post offices receiving newspapers priced above</Typography>
                        <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                            <TextField
                                label="Price"
                                type="number"
                                value={price}
                                onChange={(e) => setPrice(e.target.value)}
                            />
                            <Button variant="contained" onClick={handleExpensiveOffices}>
                                Find
                            </Button>
                        </Box>
                        {expensiveOffices.length > 0 && (
                            <Box sx={{ mt: 2 }}>
                                <Typography>Addresses of Post offices:</Typography>
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
                        <Typography variant="h6">Editor with the largest circulation</Typography>
                        <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                            <TextField
                                label="PrintShop ID"
                                value={printshopId}
                                onChange={(e) => setPrintshopId(e.target.value)}
                            />
                            <Button variant="contained" onClick={handleLargestEditor}>
                                Find
                            </Button>
                        </Box>
                        {largestEditorSurname && (
                            <Box sx={{ mt: 2 }}>
                                <Typography>
                                    Editor with the largest circulation: <b>{largestEditorSurname}</b>
                                </Typography>
                            </Box>
                        )}
                    </Paper>
                </Grid>

                <Grid item xs={12} md={12}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6">Where the newspaper goes from the print shop</Typography>
                        <Box sx={{ display: 'flex', gap: 2, mt: 2, flexWrap: 'wrap' }}>
                            <TextField
                                label="Name of the newspaper"
                                value={ndName}
                                onChange={(e) => setNdName(e.target.value)}
                            />
                            <TextField
                                label="Address of the printshop"
                                value={ndAddress}
                                onChange={(e) => setNdAddress(e.target.value)}
                            />
                            <Button variant="contained" onClick={handleDistributionAtAddress}>
                                Show
                            </Button>
                        </Box>
                        {postOfficesResults.length > 0 && (
                            <Box sx={{ mt: 2 }}>
                                <Typography>List of Post offices:</Typography>
                                <List>
                                    {postOfficesResults.map((po, i) => (
                                        <ListItem key={i}>
                                            <ListItemText
                                                primary={`Post Office №${po.postoffice__office_number}, Address: ${po.postoffice__address}`}
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
