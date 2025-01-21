import React, { useEffect, useState } from 'react';
import { Container, Typography, Button, Table, TableBody, TableCell, TableHead, TableRow, Paper } from '@mui/material';
import { Link } from 'react-router-dom';
import api from '../../services/api';

interface Editor {
    id: number;
    first_name: string;
    last_name: string;
    patronymic?: string;
}

const EditorList: React.FC = () => {
    const [editors, setEditors] = useState<Editor[]>([]);

    const fetchEditors = async () => {
        try {
            const response = await api.get<Editor[]>('/editors/');
            setEditors(response.data);
        } catch (error) {
            console.error('Ошибка при получении списка редакторов:', error);
        }
    };

    useEffect(() => {
        fetchEditors();
    }, []);

    const getFullName = (editor: Editor) => {
        return `${editor.last_name} ${editor.first_name} ${editor.patronymic || ''}`.trim();
    };

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Редакторы
            </Typography>
            <Button variant="contained" component={Link} to="/editors/create" sx={{ backgroundColor: '#B0B0B0', color: 'black', mr: 2 }}>
                Добавить редактора
            </Button>
            <Paper>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>ФИО</TableCell>
                            <TableCell>Действия</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {editors.map((editor) => (
                            <TableRow key={editor.id}>
                                <TableCell>{getFullName(editor)}</TableCell>
                                <TableCell>
                                    <Button
                                        variant="contained"
                                        component={Link}
                                        to={`/editors/${editor.id}`}
                                        sx={{ backgroundColor: '#B0B0B0', color: 'black', mr: 1 }}
                                    >
                                        Просмотр
                                    </Button>
                                    <Button
                                        variant="contained"
                                        component={Link}
                                        to={`/editors/${editor.id}/edit`}
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

export default EditorList;
