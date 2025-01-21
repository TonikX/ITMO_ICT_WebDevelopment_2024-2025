import React, { useEffect, useState } from 'react';
import { Container, Typography, Button, Table, TableBody, TableCell, TableHead, TableRow, Paper } from '@mui/material';
import { Link } from 'react-router-dom';
import api from '../../services/api';

interface PrintShop {
    id: number;
    name: string;
    address: string;
    is_open: boolean;
}

const PrintShopList: React.FC = () => {
    const [printshops, setPrintshops] = useState<PrintShop[]>([]);

    const fetchPrintShops = async () => {
        try {
            const response = await api.get<PrintShop[]>('/printshops/');
            setPrintshops(response.data);
        } catch (error) {
            console.error('Ошибка при получении списка типографий:', error);
        }
    };

    useEffect(() => {
        fetchPrintShops();
    }, []);

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Типографии
            </Typography>
            <Button
                variant="contained"
                component={Link}
                to="/printshops/create"
                sx={{ backgroundColor: '#B0B0B0', color: 'black', mr: 2 }}
            >
                Добавить типографию
            </Button>
            <Paper>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Название</TableCell>
                            <TableCell>Адрес</TableCell>
                            <TableCell>Открыта?</TableCell>
                            <TableCell>Действия</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {printshops.map((shop) => (
                            <TableRow key={shop.id}>
                                <TableCell>{shop.name}</TableCell>
                                <TableCell>{shop.address}</TableCell>
                                <TableCell>{shop.is_open ? 'Да' : 'Нет'}</TableCell>
                                <TableCell>
                                    <Button
                                        variant="contained"
                                        component={Link}
                                        to={`/printshops/${shop.id}`}
                                        sx={{ backgroundColor: '#B0B0B0', color: 'black', mr: 2 }}
                                    >
                                        Просмотр
                                    </Button>
                                    <Button
                                        variant="contained"
                                        component={Link}
                                        to={`/printshops/${shop.id}/edit`}
                                        sx={{ backgroundColor: '#B0B0B0', color: 'black', mr: 2 }}
                                    >
                                        Редактировать
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