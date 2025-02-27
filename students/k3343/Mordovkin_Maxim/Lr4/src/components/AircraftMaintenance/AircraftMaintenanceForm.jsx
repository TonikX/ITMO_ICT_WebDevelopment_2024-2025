// src/components/AircraftMaintenance/AircraftMaintenanceForm.jsx
import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { createMaintenance, updateMaintenance, fetchMaintenances } from '../../store/slices/aircraftMaintenanceSlice';
import { fetchAircrafts as fetchAircraftList } from '../../store/slices/aircraftSlice';
import { Paper, Title, TextInput, Select, Button, Text } from '@mantine/core';
import { motion } from 'framer-motion';
import { useNavigate, useParams } from 'react-router-dom';
import dayjs from 'dayjs';

const AircraftMaintenanceForm = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { maintenanceId } = useParams();
    const isEdit = Boolean(maintenanceId);

    const { maintenances, loading, error } = useSelector(state => state.aircraftMaintenances);
    const { aircrafts, loading: aircraftsLoading, error: aircraftsError } = useSelector(state => state.aircrafts);
    const [status, setStatus] = useState('');
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [aircraftId, setAircraftId] = useState('');

    useEffect(() => {
        // Используйте fetchAircraftList вместо fetchAircrafts
        dispatch(fetchAircraftList());
        if (isEdit) {
            dispatch(fetchMaintenances());
        }
    }, [dispatch, isEdit]);

    useEffect(() => {
        if (isEdit && maintenances.length > 0) {
            const maintenance = maintenances.find(m => m.maintenanceID === parseInt(maintenanceId, 10));
            if (maintenance) {
                setStatus(maintenance.maintenanceStatus);
                setStartDate(maintenance.startDate ? dayjs(maintenance.startDate).format('YYYY-MM-DD') : '');
                setEndDate(maintenance.endDate ? dayjs(maintenance.endDate).format('YYYY-MM-DD') : '');
                setAircraftId(maintenance.aircraft ? maintenance.aircraft.aircraftID.toString() : '');
            }
        }
    }, [isEdit, maintenances, maintenanceId]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const maintenanceData = {
            maintenanceStatus: status,
            startDate: startDate ? dayjs(startDate).format('YYYY-MM-DD') : null,
            endDate: endDate ? dayjs(endDate).format('YYYY-MM-DD') : null,
            aircraft: { aircraftID: parseInt(aircraftId, 10) },
        };

        if (isEdit) {
            await dispatch(updateMaintenance({ id: parseInt(maintenanceId, 10), data: maintenanceData }));
        } else {
            await dispatch(createMaintenance(maintenanceData));
        }
        navigate('/aircraft-maintenances');
    };

    if (aircraftsLoading || loading) return <Text>Loading...</Text>;
    if (aircraftsError) return <Text color="red">{aircraftsError}</Text>;
    if (isEdit && error) return <Text color="red">{error}</Text>;

    return (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
            <Paper p="md" radius="md" withBorder style={{ maxWidth: 500, margin: '40px auto' }}>
                <Title order={2} mb="md">{isEdit ? 'Edit Maintenance Record' : 'Add New Maintenance Record'}</Title>
                <form onSubmit={handleSubmit}>
                    <Select
                        label="Maintenance Status"
                        placeholder="Select status"
                        data={[
                            { value: 'IN_PROGRESS', label: 'In Progress' },
                            { value: 'COMPLETED', label: 'Completed' },
                            { value: 'SCHEDULED', label: 'Scheduled' },
                        ]}
                        value={status}
                        onChange={setStatus}
                        required
                        mb="md"
                    />

                    <TextInput
                        label="Start Date"
                        type="date"
                        value={startDate}
                        onChange={(e) => setStartDate(e.currentTarget.value)}
                        required
                        mb="md"
                    />

                    <TextInput
                        label="End Date"
                        type="date"
                        value={endDate}
                        onChange={(e) => setEndDate(e.currentTarget.value)}
                        mb="md"
                    />

                    <Select
                        label="Aircraft"
                        placeholder="Select aircraft"
                        data={aircrafts.map(a => ({ value: a.aircraftID.toString(), label: `${a.aircraftType} (${a.seats} seats)` }))}
                        value={aircraftId.toString()}
                        onChange={setAircraftId}
                        required
                        mb="md"
                    />

                    {error && (
                        <Text color="red" mb="md">
                            {JSON.stringify(error)}
                        </Text>
                    )}

                    <Button type="submit" color="blue" fullWidth>
                        {isEdit ? 'Update Maintenance' : 'Create Maintenance'}
                    </Button>
                </form>
            </Paper>
        </motion.div>
    );
};

export default AircraftMaintenanceForm;
