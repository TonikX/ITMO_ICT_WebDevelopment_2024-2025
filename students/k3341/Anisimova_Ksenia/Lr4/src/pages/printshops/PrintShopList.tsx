import React, { useEffect, useState } from 'react';
import { Container, Typography, Button, Table, TableBody, TableCell, TableHead, TableRow, Paper } from '@mui/material';
import { Link } from 'react-router-dom';
import api from '../../services/api';

interface PrintShop {
    id: string;
    name: string;
    address: string;
    is_closed: boolean;
}

const PrintShopList: React.FC = () => {
    const [printshops, setPrintshops] = useState<PrintShop[]>([]);

    const fetchPrintShops = async () => {
        try {
            const response = await api.get<PrintShop[]>('/printshops/');
            setPrintshops(response.data);
        } catch (error) {
            console.error('Error fetching the list of print shops:', error);
        }
    };

    useEffect(() => {
        fetchPrintShops();
    }, []);

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Print Shop List
            </Typography>
            <Button
                variant="contained"
                component={Link}
                to="/printshops/create"
                sx={{ mb: 2 }}
            >
                Add Print Shop
            </Button>
            <Paper>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Name</TableCell>
                            <TableCell>Address</TableCell>
                            <TableCell>Closed?</TableCell>
                            <TableCell>Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {printshops.map((shop) => (
                            <TableRow key={shop.id}>
                                <TableCell>{shop.name}</TableCell>
                                <TableCell>{shop.address}</TableCell>
                                <TableCell>{shop.is_closed ? 'Yes' : 'No'}</TableCell>
                                <TableCell>
                                    <Button
                                        variant="outlined"
                                        component={Link}
                                        to={`/printshops/${shop.id}`}
                                        sx={{ mr: 1 }}
                                    >
                                        View
                                    </Button>
                                    <Button
                                        variant="outlined"
                                        component={Link}
                                        to={`/printshops/${shop.id}/edit`}
                                    >
                                        Edit
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </Paper>
        </Container>
    );
};

export default PrintShopList;
