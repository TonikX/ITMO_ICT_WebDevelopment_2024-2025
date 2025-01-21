import React, { useEffect, useState } from 'react';
import { Container, Typography, Button, Table, TableBody, TableCell, TableHead, TableRow, Paper } from '@mui/material';
import { Link } from 'react-router-dom';
import api from '../../services/api';

interface PostOffice {
    id: number;
    number: string;
    address: string;
}

const PostOfficeList: React.FC = () => {
    const [offices, setOffices] = useState<PostOffice[]>([]);

    const fetchPostOffices = async () => {
        try {
            const response = await api.get<PostOffice[]>('/postoffices/');
            setOffices(response.data);
        } catch (error) {
            console.error('Ошибка при получении списка отделений:', error);
        }
    };

    useEffect(() => {
        fetchPostOffices();
    }, []);

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Почтовые отделения
            </Typography>
            <Button
                variant="contained"
                component={Link}
                to="/postoffices/create"
                sx={{ backgroundColor: '#B0B0B0', color: 'black', mr: 2 }}
            >
                Добавить отделение
            </Button>
            <Paper>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Номер отделения</TableCell>
                            <TableCell>Адрес</TableCell>
                            <TableCell>Действия</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {offices.map((office) => (
                            <TableRow key={office.id}>
                                <TableCell>{office.number}</TableCell>
                                <TableCell>{office.address}</TableCell>
                                <TableCell>
                                    <Button
                                        variant="contained"
                                        component={Link}
                                        to={`/postoffices/${office.id}`}
                                        sx={{ backgroundColor: '#B0B0B0', color: 'black', mr: 2 }}
                                    >
                                        Просмотр
                                    </Button>
                                    <Button
                                        variant="contained"
                                        component={Link}
                                        to={`/postoffices/${office.id}/edit`}
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

export default PostOfficeList;