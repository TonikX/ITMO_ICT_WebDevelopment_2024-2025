import React, { useEffect, useState } from 'react';
import { Container, Typography, Button, Table, TableBody, TableCell, TableHead, TableRow, Paper } from '@mui/material';
import { Link } from 'react-router-dom';
import api from '../../services/api';

interface PostOffice {
    id: string;
    office_number: number;
    address: string;
}

const PostOfficeList: React.FC = () => {
    const [offices, setOffices] = useState<PostOffice[]>([]);

    const fetchPostOffices = async () => {
        try {
            const response = await api.get<PostOffice[]>('/postoffices/');
            setOffices(response.data);
        } catch (error) {
            console.error('Error fetching the list of post offices:', error);
        }
    };

    useEffect(() => {
        fetchPostOffices();
    }, []);

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Post Office List
            </Typography>
            <Button
                variant="contained"
                component={Link}
                to="/postoffices/create"
                sx={{ mb: 2 }}
            >
                Add Post Office
            </Button>
            <Paper>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Office Number</TableCell>
                            <TableCell>Address</TableCell>
                            <TableCell>Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {offices.map((office) => (
                            <TableRow key={office.id}>
                                <TableCell>{office.office_number}</TableCell>
                                <TableCell>{office.address}</TableCell>
                                <TableCell>
                                    <Button
                                        variant="outlined"
                                        component={Link}
                                        to={`/postoffices/${office.id}`}
                                        sx={{ mr: 1 }}
                                    >
                                        View
                                    </Button>
                                    <Button
                                        variant="outlined"
                                        component={Link}
                                        to={`/postoffices/${office.id}/edit`}
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

export default PostOfficeList;
