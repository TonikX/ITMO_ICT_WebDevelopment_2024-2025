// src/components/AircraftMaintenance/AircraftMaintenanceList.jsx
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMaintenances, deleteMaintenance } from '../../store/slices/aircraftMaintenanceSlice';
import { Table, Button, Group, Text, Paper, Loader } from '@mantine/core';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import dayjs from 'dayjs';

const AircraftMaintenanceList = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { maintenances, loading, error } = useSelector(state => state.aircraftMaintenances);
    const { user } = useSelector(state => state.auth);

    useEffect(() => {
        dispatch(fetchMaintenances());
    }, [dispatch]);

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this maintenance record?')) {
            await dispatch(deleteMaintenance(id));
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
                    <Text size="xl" weight={700}>Aircraft Maintenance Records</Text>
                    {user?.role === 'ADMIN' && (
                        <Button onClick={() => navigate('/maintenance/new')} color="blue">
                            Add New Maintenance
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
                        <th>ID</th>
                        <th>Aircraft</th>
                        <th>Status</th>
                        <th>Start Date</th>
                        <th>End Date</th>
                        <th>Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    {maintenances.map((m) => (
                        <motion.tr
                            key={m.maintenanceID}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.3 }}
                        >
                            <td>{m.maintenanceID}</td>
                            <td>{m.aircraft ? m.aircraft.aircraftType : 'N/A'}</td>
                            <td>{m.maintenanceStatus}</td>
                            <td>{m.startDate ? dayjs(m.startDate).format('YYYY-MM-DD') : 'N/A'}</td>
                            <td>{m.endDate ? dayjs(m.endDate).format('YYYY-MM-DD') : 'N/A'}</td>
                            <td>
                                <Group spacing="xs">
                                    <Button
                                        size="xs"
                                        onClick={() => navigate(`/maintenance/${m.maintenanceID}/edit`)}
                                    >
                                        Edit
                                    </Button>
                                    <Button
                                        size="xs"
                                        color="red"
                                        onClick={() => handleDelete(m.maintenanceID)}
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

export default AircraftMaintenanceList;
