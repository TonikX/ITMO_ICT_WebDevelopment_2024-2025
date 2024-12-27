import React, { useEffect, useState } from 'react';
import { Container, Typography, Button, Table, TableBody, TableCell, TableHead, TableRow, Paper } from '@mui/material';
import { Link } from 'react-router-dom';
import api from '../../services/api';
import { Distribution } from '../../types/types';

const DistributionList: React.FC = () => {
    const [distributions, setDistributions] = useState<Distribution[]>([]);

    const fetchDistributions = async () => {
        try {
            const response = await api.get<Distribution[]>('/distributions/');
            setDistributions(response.data);
        } catch (error) {
            console.error('Ошибка при загрузке распределений:', error);
        }
    };

    useEffect(() => {
        fetchDistributions();
    }, []);

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Список распределений
            </Typography>
            <Button
                variant="contained"
                component={Link}
                to="/distributions/create"
                sx={{ mb: 2 }}
            >
                Добавить распределение
            </Button>
            <Paper>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Газета</TableCell>
                            <TableCell>Типография</TableCell>
                            <TableCell>Почтовое отделение</TableCell>
                            <TableCell>Тираж</TableCell>
                            <TableCell>Отправлено</TableCell>
                            <TableCell>Действия</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {distributions.map((dist) => (
                            <TableRow key={dist.id}>
                                <TableCell>{dist.newspaper?.name}</TableCell>
                                <TableCell>{dist.printshop?.name}</TableCell>
                                <TableCell>№{dist.postoffice?.office_number}</TableCell>
                                <TableCell>{dist.copies_printed}</TableCell>
                                <TableCell>{dist.copies_sent}</TableCell>
                                <TableCell>
                                    <Button
                                        variant="outlined"
                                        component={Link}
                                        to={`/distributions/${dist.id}`}
                                        sx={{ mr: 1 }}
                                    >
                                        Просмотр
                                    </Button>
                                    <Button
                                        variant="outlined"
                                        component={Link}
                                        to={`/distributions/${dist.id}/edit`}
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

export default DistributionList;
