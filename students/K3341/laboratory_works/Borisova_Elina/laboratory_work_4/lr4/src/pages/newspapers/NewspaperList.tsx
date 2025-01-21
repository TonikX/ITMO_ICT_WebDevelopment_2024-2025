import React, { useEffect, useState } from 'react';
import { Container, Typography, Button, Table, TableBody, TableCell, TableHead, TableRow, Paper } from '@mui/material';
import { Link } from 'react-router-dom';
import api from '../../services/api';

interface Newspaper {
    id: number;
    name: string;
    index: string;
    price: number;
    editor: {
        id: number;
        first_name: string;
        last_name: string;
        patronymic?: string;
    };
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

    const getEditorFullName = (editor: Newspaper['editor']) => {
        return `${editor.last_name} ${editor.first_name} ${editor.patronymic || ''}`.trim();
    };

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Газеты
            </Typography>
            <Button
                variant="contained"
                component={Link}
                to="/newspapers/create"
                sx={{ backgroundColor: '#B0B0B0', color: 'black', mr: 2 }}
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
                            <TableCell>Редактор</TableCell>
                            <TableCell>Действия</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {newspapers.map((paper) => (
                            <TableRow key={paper.id}>
                                <TableCell>{paper.name}</TableCell>
                                <TableCell>{paper.index}</TableCell>
                                <TableCell>{paper.price.toFixed(2)}</TableCell>
                                <TableCell>{getEditorFullName(paper.editor)}</TableCell>
                                <TableCell>
                                    <Button
                                        variant="contained"
                                        component={Link}
                                        to={`/newspapers/${paper.id}`}
                                        sx={{ backgroundColor: '#B0B0B0', color: 'black', mr: 2 }}
                                    >
                                        Просмотр
                                    </Button>
                                    <Button
                                        variant="contained"
                                        component={Link}
                                        to={`/newspapers/${paper.id}/edit`}
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

export default NewspaperList;
