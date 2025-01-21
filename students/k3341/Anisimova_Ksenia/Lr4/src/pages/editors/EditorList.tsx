import React, { useEffect, useState } from 'react';
import { Container, Typography, Button, Table, TableBody, TableCell, TableHead, TableRow, Paper } from '@mui/material';
import { Link } from 'react-router-dom';
import api from '../../services/api';

interface Editor {
    id: string;
    name: string;
    created_at: string;
    updated_at: string;
}

const EditorList: React.FC = () => {
    const [editors, setEditors] = useState<Editor[]>([]);

    const fetchEditors = async () => {
        try {
            const response = await api.get<Editor[]>('/editors/');
            setEditors(response.data);
        } catch (error) {
            console.error('Error fetching the list of editors:', error);
        }
    };

    useEffect(() => {
        fetchEditors();
    }, []);

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Editor List
            </Typography>
            <Button variant="contained" component={Link} to="/editors/create" sx={{ mb: 2 }}>
                Add Editor
            </Button>
            <Paper>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Name</TableCell>
                            <TableCell>Date Added</TableCell>
                            <TableCell>Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {editors.map((editor) => (
                            <TableRow key={editor.id}>
                                <TableCell>{editor.name}</TableCell>
                                <TableCell>{new Date(editor.created_at).toLocaleString()}</TableCell>
                                <TableCell>
                                    <Button
                                        variant="outlined"
                                        component={Link}
                                        to={`/editors/${editor.id}`}
                                        sx={{ mr: 1 }}
                                    >
                                        View
                                    </Button>
                                    <Button
                                        variant="outlined"
                                        component={Link}
                                        to={`/editors/${editor.id}/edit`}
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

export default EditorList;
