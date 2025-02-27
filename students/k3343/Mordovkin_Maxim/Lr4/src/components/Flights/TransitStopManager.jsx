// src/components/Flights/TransitStopManager.jsx

import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchTransitStops, addTransitStop, removeTransitStop } from '../../store/slices/transitStopSlice';
import { TextInput, Button, Table, Text, Loader, Group } from '@mantine/core';
import { motion } from 'framer-motion';
import dayjs from 'dayjs';

const TransitStopManager = ({ flightId }) => {
    const dispatch = useDispatch();
    const { transitStops, loading, error } = useSelector(state => state.transitStops);
    const [transitPoint, setTransitPoint] = useState('');
    const [arrivalDateTime, setArrivalDateTime] = useState(dayjs().format('YYYY-MM-DDTHH:mm'));
    const [departureDateTime, setDepartureDateTime] = useState(dayjs().format('YYYY-MM-DDTHH:mm'));

    useEffect(() => {
        dispatch(fetchTransitStops(flightId));
    }, [dispatch, flightId]);

    const handleAdd = async () => {
        if (!transitPoint) {
            alert('Please enter transit point.');
            return;
        }
        if (dayjs(arrivalDateTime).isAfter(dayjs(departureDateTime))) {
            alert('Arrival time must be before departure time.');
            return;
        }
        const formattedArrival = dayjs(arrivalDateTime).format('YYYY-MM-DDTHH:mm:ss');
        const formattedDeparture = dayjs(departureDateTime).format('YYYY-MM-DDTHH:mm:ss');

        console.log('Formatted Arrival DateTime:', formattedArrival);
        console.log('Formatted Departure DateTime:', formattedDeparture);

        const result = await dispatch(addTransitStop({
            flightId,
            transitStop: {
                transitPoint,
                transitArrivalDateTime: formattedArrival,
                transitDepartureDateTime: formattedDeparture,
            },
        }));
        if (!result.error) {
            dispatch(fetchTransitStops(flightId)); // Обновить список после добавления
            setTransitPoint('');
            setArrivalDateTime(dayjs().format('YYYY-MM-DDTHH:mm'));
            setDepartureDateTime(dayjs().format('YYYY-MM-DDTHH:mm'));
        } else {
            // Если ошибка является объектом с полем error
            const errorMessage = result.payload?.error || 'Failed to add transit stop.';
            alert(errorMessage);
        }
    };

    const handleRemove = async (transitStopId) => {
        if (window.confirm('Are you sure you want to remove this transit stop?')) {
            const result = await dispatch(removeTransitStop({ transitStopId }));
            if (result.error) {
                const errorMessage = result.payload?.error || 'Remove transit stop failed.';
                alert(errorMessage);
            }
        }
    };

    if (loading) return <Loader size="xl" />;
    if (error) return <Text color="red">{error}</Text>;

    return (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
            <Text size="lg" weight={700} mb="md"></Text>

            <Group mb="md">
                <TextInput
                    label="Transit Point"
                    value={transitPoint}
                    onChange={(e) => setTransitPoint(e.currentTarget.value)}
                    required
                    style={{ flex: 1 }}
                />
                <TextInput
                    label="Arrival DateTime"
                    type="datetime-local"
                    value={arrivalDateTime}
                    onChange={(e) => setArrivalDateTime(e.target.value)}
                    required
                />
                <TextInput
                    label="Departure DateTime"
                    type="datetime-local"
                    value={departureDateTime}
                    onChange={(e) => setDepartureDateTime(e.target.value)}
                    required
                />
                <Button onClick={handleAdd}>Add</Button>
            </Group>

            <Table>
                <thead>
                <tr>
                    <th>ID</th>
                    <th>Transit Point</th>
                    <th>Arrival DateTime</th>
                    <th>Departure DateTime</th>
                    <th>Actions</th>
                </tr>
                </thead>
                <tbody>
                {transitStops.length > 0 ? (
                    transitStops.map(ts => (
                        <tr key={ts.transitStopId}>
                            <td>{ts.transitStopId}</td>
                            <td>{ts.transitPoint}</td>
                            <td>{dayjs(ts.transitArrivalDateTime).format('YYYY-MM-DD HH:mm')}</td>
                            <td>{dayjs(ts.transitDepartureDateTime).format('YYYY-MM-DD HH:mm')}</td>
                            <td>
                                <Button color="red" size="xs" onClick={() => handleRemove(ts.transitStopId)}>
                                    Remove
                                </Button>
                            </td>
                        </tr>
                    ))
                ) : (
                    <tr>
                        <td colSpan="5" align="center">
                            No transit stops available.
                        </td>
                    </tr>
                )}
                </tbody>
            </Table>
        </motion.div>
    );
};

export default TransitStopManager;
