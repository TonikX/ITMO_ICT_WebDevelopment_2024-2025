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
            console.error('Error loading distributions:', error);
        }
    };

    useEffect(() => {
        fetchDistributions();
    }, []);

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Distribution List
            </Typography>
            <Button
                variant="contained"
                component={Link}
                to="/distributions/create"
                sx={{ mb: 2 }}
            >
                Add Distribution
            </Button>
            <Paper>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Newspaper</TableCell>
                            <TableCell>PrintShop</TableCell>
                            <TableCell>PostOffice</TableCell>
                            <TableCell>Copies Printed</TableCell>
                            <TableCell>Copies Sent</TableCell>
                            <TableCell>Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {distributions.map((dist) => (
                            <TableRow key={dist.id}>
                                <TableCell>{dist.newspaper?.name}</TableCell>
                                <TableCell>{dist.printshop?.name}</TableCell>
                                <TableCell>#{dist.postoffice?.office_number}</TableCell>
                                <TableCell>{dist.copies_printed}</TableCell>
                                <TableCell>{dist.copies_sent}</TableCell>
                                <TableCell>
                                    <Button
                                        variant="outlined"
                                        component={Link}
                                        to={`/distributions/${dist.id}`}
                                        sx={{ mr: 1 }}
                                    >
                                        View
                                    </Button>
                                    <Button
                                        variant="outlined"
                                        component={Link}
                                        to={`/distributions/${dist.id}/edit`}
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

export default DistributionList;
