// src/components/Carriers/CarrierList.jsx
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchCarriers, deleteCarrier } from '../../store/slices/carrierSlice';
import { Table, Button, Group, Text, Paper, Loader } from '@mantine/core';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

const CarrierList = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { carriers, loading, error } = useSelector(state => state.carriers);
    const { user } = useSelector(state => state.auth);

    useEffect(() => {
        dispatch(fetchCarriers());
    }, [dispatch]);

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this carrier?')) {
            await dispatch(deleteCarrier(id));
        }
    };

    if (loading) {
        return <Loader size="xl" />;
    }

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
        >
            <Paper p="md" radius="md" withBorder>
                <Group position="apart" mb="md">
                    <Text size="xl" weight={700}>Carrier List</Text>
                    {user?.role === 'ADMIN' && (
                        <Button onClick={() => navigate('/carriers/new')} color="blue">
                            Add New Carrier
                        </Button>
                    )}
                </Group>

                {error && (
                    <Text color="red" mb="md">
                        {JSON.stringify(error)}
                    </Text>
                )}

                <Table highlightOnHover>
                    <thead>
                    <tr>
                        <th>Carrier ID</th>
                        <th>Name</th>
                        <th>Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    {carriers.map((carrier) => (
                        <motion.tr
                            key={carrier.carrierID}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.3 }}
                        >
                            <td>{carrier.carrierID}</td>
                            <td>{carrier.carrierName}</td>
                            <td>
                                <Group spacing="xs">
                                    <Button
                                        size="xs"
                                        onClick={() => navigate(`/carriers/${carrier.carrierID}/edit`)}
                                    >
                                        Edit
                                    </Button>
                                    <Button
                                        size="xs"
                                        color="red"
                                        onClick={() => handleDelete(carrier.carrierID)}
                                    >
                                        Delete
                                    </Button>
                                </Group>
                            </td>
                        </motion.tr>
                    ))}
                    </tbody>
                </Table>
            </Paper>
        </motion.div>
    );
};

export default CarrierList;
