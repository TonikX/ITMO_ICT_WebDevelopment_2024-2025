// src/components/Flights/FlightDetails.jsx

import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchFlightById } from '../../store/slices/flightSlice';
import { useParams, useNavigate } from 'react-router-dom';
import { Paper, Title, Text, Group, Button, Loader } from '@mantine/core';
import { motion } from 'framer-motion';
import dayjs from 'dayjs';
import TransitStopManager from './TransitStopManager';
import FlightCrewManager from './FlightCrewManager';

const FlightDetails = () => {
    const { flightId } = useParams();
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { currentFlight, loading, error } = useSelector(state => state.flights);
    const { user } = useSelector(state => state.auth);

    useEffect(() => {
        const id = parseInt(flightId, 10);
        if (!isNaN(id)) {
            dispatch(fetchFlightById(id));
        }
    }, [dispatch, flightId]);

    if (loading || !currentFlight) {
        return <Loader size="xl" />;
    }

    if (error) {
        return <Text color="red">{error}</Text>;
    }

    const handleEdit = () => {
        navigate(`/flights/${flightId}/edit`);
    };

    return (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
            <Paper p="md" radius="md" withBorder style={{ maxWidth: 800, margin: '40px auto' }}>
                <Group position="apart" mb="md">
                    <Title order={2}>Flight Details #{currentFlight.flightId}</Title>
                    {user?.role === 'ADMIN' && (
                        <Button onClick={handleEdit}>Edit Flight</Button>
                    )}
                </Group>

                <Text><b>Departure Point:</b> {currentFlight.departurePoint}</Text>
                <Text><b>Destination Point:</b> {currentFlight.destinationPoint}</Text>
                <Text><b>Distance:</b> {currentFlight.distance} km</Text>
                <Text><b>Departure DateTime:</b> {dayjs(currentFlight.departureDateTime).format('YYYY-MM-DD HH:mm')}</Text>
                <Text><b>Arrival DateTime:</b> {dayjs(currentFlight.arrivalDateTime).format('YYYY-MM-DD HH:mm')}</Text>
                <Text><b>Tickets Sold:</b> {currentFlight.ticketsSold}</Text>
                <Text><b>Total Seats:</b> {currentFlight.totalSeats}</Text>
                <Text><b>Occupancy:</b> {((currentFlight.ticketsSold / currentFlight.totalSeats) * 100).toFixed(2)}%</Text>
                <Text><b>Aircraft:</b> {currentFlight.aircraft ? `${currentFlight.aircraft.aircraftType} (${currentFlight.aircraft.seats} seats)` : 'Not Assigned'}</Text>

                {/* Отображение транзитных остановок только для админов */}
                {user?.role === 'ADMIN' && (
                    <TransitStopManager flightId={currentFlight.flightId} />
                )}

                {/* Отображение управления экипажем только для админов */}
                {user?.role === 'ADMIN' && (
                    <FlightCrewManager flightId={currentFlight.flightId} />
                )}
            </Paper>
        </motion.div>
    );
};

export default FlightDetails;
