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
            console.error('Ошибка при получении списка типографий:', error);
        }
    };

    useEffect(() => {
        fetchPrintShops();
    }, []);

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Список типографий
            </Typography>
            <Button
                variant="contained"
                component={Link}
                to="/printshops/create"
                sx={{ mb: 2 }}
            >
                Добавить типографию
            </Button>
            <Paper>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Название</TableCell>
                            <TableCell>Адрес</TableCell>
                            <TableCell>Закрыта?</TableCell>
                            <TableCell>Действия</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {printshops.map((shop) => (
                            <TableRow key={shop.id}>
                                <TableCell>{shop.name}</TableCell>
                                <TableCell>{shop.address}</TableCell>
                                <TableCell>{shop.is_closed ? 'Да' : 'Нет'}</TableCell>
                                <TableCell>
                                    <Button
                                        variant="outlined"
                                        component={Link}
                                        to={`/printshops/${shop.id}`}
                                        sx={{ mr: 1 }}
                                    >
                                        Просмотр
                                    </Button>
                                    <Button
                                        variant="outlined"
                                        component={Link}
                                        to={`/printshops/${shop.id}/edit`}
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
