import React, { useEffect, useState } from 'react';
import { Container, Typography, Button, Table, TableBody, TableCell, TableHead, TableRow, Paper } from '@mui/material';
import { Link } from 'react-router-dom';
import api from '../../services/api';

interface Delivery {
    id: number;
    print_run: {
        newspaper: { name: string };
        printshop: { name: string };
        quantity: number;
        date: string;
    };
    post_office: {
        number: string;
        address: string;
    };
    quantity: number;
}

const DeliveryList: React.FC = () => {
    const [deliveries, setDeliveries] = useState<Delivery[]>([]);

    useEffect(() => {
        api.get<Delivery[]>('/deliveries/')
            .then((res) => setDeliveries(res.data))
            .catch((err) => console.error('Ошибка при загрузке доставок:', err));
    }, []);

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4">Доставки</Typography>
            <Button variant="contained" component={Link} to="/deliveries/create" sx={{ backgroundColor: '#B0B0B0', color: 'black', mr: 2 }}>Добавить доставку</Button>
            <Paper>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Газета</TableCell>
                            <TableCell>Типография</TableCell>
                            <TableCell>Тираж</TableCell>
                            <TableCell>Количество экземпляров</TableCell>
                            <TableCell>Почтовое отделение</TableCell>
                            <TableCell>Дата печати</TableCell>
                            <TableCell>Действия</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {deliveries.length > 0 ? (
                            deliveries.map((delivery) => (
                                <TableRow key={delivery.id}>
                                    <TableCell>{delivery.print_run.newspaper.name}</TableCell>
                                    <TableCell>{delivery.print_run.printshop.name}</TableCell>
                                    <TableCell>{delivery.print_run.quantity}</TableCell>
                                    <TableCell>{delivery.quantity}</TableCell>
                                    <TableCell>№{delivery.post_office.number} - {delivery.post_office.address}</TableCell>
                                    <TableCell>{new Date(delivery.print_run.date).toLocaleDateString()}</TableCell>
                                    <TableCell>
                                        <Button variant="contained" component={Link} to={`/deliveries/${delivery.id}/edit`} sx={{ backgroundColor: '#B0B0B0', color: 'black', mr: 2 }}>
                                            Редактировать
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            ))
                        ) : (
                            <TableRow>
                                <TableCell colSpan={7} align="center">
                                    Данных нет
                                </TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </Paper>
        </Container>
    );
};

export default DeliveryList;