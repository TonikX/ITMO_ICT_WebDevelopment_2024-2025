import React, { useEffect, useState } from 'react';
import { Container, Typography, Button, Table, TableBody, TableCell, TableHead, TableRow, Paper } from '@mui/material';
import { Link } from 'react-router-dom';
import api from '../../services/api';

interface Newspaper {
    id: string;
    name: string;
    index: string;
    price: string;
    price_updated_at: string;
    created_at: string;
    updated_at: string;
}

const NewspaperList: React.FC = () => {
    const [newspapers, setNewspapers] = useState<Newspaper[]>([]);

    const fetchNewspapers = async () => {
        try {
            const response = await api.get<Newspaper[]>('/newspapers/');
            setNewspapers(response.data);
        } catch (error) {
            console.error('Ошибка при получении списка газет:', error);
        }
    };

    useEffect(() => {
        fetchNewspapers();
    }, []);

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Список газет
            </Typography>
            <Button
                variant="contained"
                component={Link}
                to="/newspapers/create"
                sx={{ mb: 2 }}
            >
                Добавить газету
            </Button>
            <Paper>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Название</TableCell>
                            <TableCell>Индекс</TableCell>
                            <TableCell>Цена</TableCell>
                            <TableCell>Дата изменения цены</TableCell>
                            <TableCell>Действия</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {newspapers.map((paper) => (
                            <TableRow key={paper.id}>
                                <TableCell>{paper.name}</TableCell>
                                <TableCell>{paper.index}</TableCell>
                                <TableCell>{paper.price}</TableCell>
                                <TableCell>{new Date(paper.price_updated_at).toLocaleString()}</TableCell>
                                <TableCell>
                                    <Button
                                        variant="outlined"
                                        component={Link}
                                        to={`/newspapers/${paper.id}`}
                                        sx={{ mr: 1 }}
                                    >
                                        Просмотр
                                    </Button>
                                    <Button
                                        variant="outlined"
                                        component={Link}
                                        to={`/newspapers/${paper.id}/edit`}
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

export default NewspaperList;
