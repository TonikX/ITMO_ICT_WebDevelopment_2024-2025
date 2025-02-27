// src/components/Flights/FlightList.jsx
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { Table, Button, Group, Text, Paper, Loader, Collapse, Badge } from '@mantine/core';
import { motion } from 'framer-motion';
import { fetchFlights, deleteFlight } from '../../store/slices/flightSlice';
import dayjs from 'dayjs';

const FlightList = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { flights, loading, error } = useSelector(state => state.flights);
    const { user } = useSelector(state => state.auth);

    // Состояние для отслеживания, какие рейсы развернуты
    const [expandedFlights, setExpandedFlights] = useState({});

    useEffect(() => {
        dispatch(fetchFlights());
    }, [dispatch]);

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this flight?')) {
            await dispatch(deleteFlight(id));
        }
    };

    const toggleExpand = (flightId) => {
        setExpandedFlights(prev => ({
            ...prev,
            [flightId]: !prev[flightId],
        }));
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
                    <Text size="xl" weight={700}>Flight List</Text>
                    {user?.role === 'ADMIN' && (
                        <Button onClick={() => navigate('/flights/new')} color="blue">
                            Add New Flight
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
                        <th></th> {/* Колонка для кнопки разворачивания */}
                        <th>Flight ID</th>
                        <th>Departure</th>
                        <th>Destination</th>
                        <th>Departure Date</th>
                        <th>Arrival Date</th>
                        <th>Tickets Sold</th>
                        <th>Total Seats</th>
                        <th>Occupancy (%)</th>
                        <th>Actions</th>
                        {user?.role === 'ADMIN' && <th>Manage Crew</th>}
                    </tr>
                    </thead>
                    <tbody>
                    {flights.map((flight) => {
                        if (!flight.flightId) {
                            console.warn(`Flight with ID ${flight.flightId} is missing flightId`);
                            return null;
                        }

                        const formattedDepartureDate = flight.departureDateTime && dayjs(flight.departureDateTime).isValid()
                            ? dayjs(flight.departureDateTime).format('YYYY-MM-DD HH:mm')
                            : 'Invalid date';

                        const formattedArrivalDate = flight.arrivalDateTime && dayjs(flight.arrivalDateTime).isValid()
                            ? dayjs(flight.arrivalDateTime).format('YYYY-MM-DD HH:mm')
                            : 'Invalid date';

                        const occupancy = flight.totalSeats > 0
                            ? ((flight.ticketsSold / flight.totalSeats) * 100).toFixed(2)
                            : 'N/A';

                        return (
                            <React.Fragment key={flight.flightId}>
                                <motion.tr
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ duration: 0.3 }}
                                >
                                    <td>
                                        <Button
                                            variant="subtle"
                                            size="xs"
                                            onClick={() => toggleExpand(flight.flightId)}
                                        >
                                            {expandedFlights[flight.flightId] ? '-' : '+'}
                                        </Button>
                                    </td>
                                    <td>{flight.flightId}</td>
                                    <td>{flight.departurePoint}</td>
                                    <td>{flight.destinationPoint}</td>
                                    <td>{formattedDepartureDate}</td>
                                    <td>{formattedArrivalDate}</td>
                                    <td>{flight.ticketsSold}</td>
                                    <td>{flight.totalSeats}</td>
                                    <td>{occupancy}%</td>
                                    <td>
                                        <Group spacing="xs">
                                            <Button
                                                size="xs"
                                                onClick={() => navigate(`/flights/${flight.flightId}`)}
                                            >
                                                View
                                            </Button>
                                            {user?.role === 'ADMIN' && (
                                                <>
                                                    <Button
                                                        size="xs"
                                                        color="yellow"
                                                        onClick={() => navigate(`/flights/${flight.flightId}/edit`)}
                                                    >
                                                        Edit
                                                    </Button>
                                                    <Button
                                                        size="xs"
                                                        color="red"
                                                        onClick={() => handleDelete(flight.flightId)}
                                                    >
                                                        Delete
                                                    </Button>
                                                </>
                                            )}
                                        </Group>
                                    </td>
                                    {user?.role === 'ADMIN' && (
                                        <td>
                                            <Button size="xs" onClick={() => navigate(`/flights/${flight.flightId}/crew`)}>
                                                Manage Crew
                                            </Button>
                                        </td>
                                    )}
                                </motion.tr>
                                <tr>
                                    <td colSpan={user?.role === 'ADMIN' ? 11 : 10}>
                                        <Collapse in={expandedFlights[flight.flightId]}>
                                            {flight.transitStops && flight.transitStops.length > 0 ? (
                                                <Table size="sm" striped>
                                                    <thead>
                                                    <tr>
                                                        <th>ID</th>
                                                        <th>Transit Point</th>
                                                        <th>Arrival DateTime</th>
                                                        <th>Departure DateTime</th>
                                                    </tr>
                                                    </thead>
                                                    <tbody>
                                                    {flight.transitStops.map(ts => (
                                                        <tr key={ts.transitId}>
                                                            <td>{ts.transitId}</td>
                                                            <td>{ts.transitPoint}</td>
                                                            <td>{dayjs(ts.transitArrivalDateTime).format('YYYY-MM-DD HH:mm')}</td>
                                                            <td>{dayjs(ts.transitDepartureDateTime).format('YYYY-MM-DD HH:mm')}</td>
                                                        </tr>
                                                    ))}
                                                    </tbody>
                                                </Table>
                                            ) : (
                                                <Text>No transit stops available.</Text>
                                            )}
                                        </Collapse>
                                    </td>
                                </tr>
                            </React.Fragment>
                        );
                    })}
                    </tbody>
                </Table>
            </Paper>
        </motion.div>
    );
};

export default FlightList;
