// src/components/Flights/FlightForm.jsx
import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { createFlight, updateFlight, fetchFlightById } from '../../store/slices/flightSlice';
import { fetchAircrafts } from '../../store/slices/aircraftSlice';
import { fetchCarriers } from '../../store/slices/carrierSlice';
import { Paper, Title, NumberInput, Button, TextInput, Select, Text } from '@mantine/core';
import { DateTimePicker } from '@mantine/dates';
import dayjs from 'dayjs';
import { motion } from 'framer-motion';
import { useNavigate, useParams } from 'react-router-dom';

const FlightForm = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { flightId } = useParams();
    const isEdit = Boolean(flightId);

    const { aircrafts, loading: aircraftsLoading, error: aircraftsError } = useSelector(state => state.aircrafts);
    const { carriers, loading: carriersLoading, error: carriersError } = useSelector(state => state.carriers);
    const { currentFlight, loading, error } = useSelector(state => state.flights);

    const [departurePoint, setDeparturePoint] = useState('');
    const [destinationPoint, setDestinationPoint] = useState('');
    const [distance, setDistance] = useState(0);
    const [ticketsSold, setTicketsSold] = useState(0);

    const [departureDate, setDepartureDate] = useState('');
    const [arrivalDate, setArrivalDate] = useState('');

    const [aircraftId, setAircraftId] = useState('');
    const [carrierId, setCarrierId] = useState('');
    const [totalSeats, setTotalSeats] = useState(0);

    useEffect(() => {
        dispatch(fetchAircrafts());
        dispatch(fetchCarriers());
        if (isEdit) {
            dispatch(fetchFlightById(parseInt(flightId, 10)));
        }
    }, [dispatch, isEdit, flightId]);

    useEffect(() => {
        if (isEdit && currentFlight) {
            setDeparturePoint(currentFlight.departurePoint);
            setDestinationPoint(currentFlight.destinationPoint);
            setDistance(currentFlight.distance);
            setTicketsSold(currentFlight.ticketsSold);
            setDepartureDate(currentFlight.departureDateTime ? dayjs(currentFlight.departureDateTime).format('YYYY-MM-DDTHH:mm') : '');
            setArrivalDate(currentFlight.arrivalDateTime ? dayjs(currentFlight.arrivalDateTime).format('YYYY-MM-DDTHH:mm') : '');
            setAircraftId(currentFlight.aircraft ? currentFlight.aircraft.aircraftID.toString() : '');
            setCarrierId(currentFlight.aircraft ? currentFlight.aircraft.carrier.carrierID.toString() : '');
            setTotalSeats(currentFlight.totalSeats);
        }
    }, [isEdit, currentFlight]);

    useEffect(() => {
        const selectedAircraft = aircrafts.find(a => a.aircraftID === parseInt(aircraftId, 10));
        if (selectedAircraft) {
            setTotalSeats(selectedAircraft.seats);
        } else {
            setTotalSeats(0);
        }
    }, [aircraftId, aircrafts]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Форматирование дат как строк
        const departureDateTime = departureDate ? dayjs(departureDate).format('YYYY-MM-DDTHH:mm:ss') : null;
        const arrivalDateTime = arrivalDate ? dayjs(arrivalDate).format('YYYY-MM-DDTHH:mm:ss') : null;

        if (ticketsSold > totalSeats) {
            alert('Tickets sold cannot exceed total seats.');
            return;
        }

        const flightData = {
            departurePoint,
            destinationPoint,
            distance,
            ticketsSold,
            departureDateTime,
            arrivalDateTime,
            aircraft: { aircraftID: parseInt(aircraftId, 10) },
            totalSeats,
        };

        if (isEdit) {
            const result = await dispatch(updateFlight({ id: parseInt(flightId, 10), data: flightData }));
            if (!result.error) {
                navigate('/flights');
            }
        } else {
            const result = await dispatch(createFlight(flightData));
            if (!result.error) {
                navigate('/flights');
            }
        }
    };

    if (aircraftsLoading || carriersLoading || (isEdit && loading)) {
        return <Text>Loading...</Text>;
    }

    if (aircraftsError) return <Text color="red">{aircraftsError}</Text>;
    if (carriersError) return <Text color="red">{carriersError}</Text>;
    if (isEdit && error) return <Text color="red">{error}</Text>;

    return (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
            <Paper p="md" radius="md" withBorder style={{ maxWidth: 600, margin: '40px auto' }}>
                <Title order={2} mb="md">{isEdit ? 'Edit Flight' : 'Add New Flight'}</Title>
                <form onSubmit={handleSubmit}>
                    <TextInput
                        label="Departure Point"
                        value={departurePoint}
                        onChange={(e) => setDeparturePoint(e.currentTarget.value)}
                        required
                        mb="md"
                    />

                    <TextInput
                        label="Destination Point"
                        value={destinationPoint}
                        onChange={(e) => setDestinationPoint(e.currentTarget.value)}
                        required
                        mb="md"
                    />

                    <NumberInput
                        label="Distance"
                        value={distance}
                        onChange={setDistance}
                        required
                        min={0}
                        mb="md"
                    />

                    <NumberInput
                        label="Tickets Sold"
                        value={ticketsSold}
                        onChange={setTicketsSold}
                        min={0}
                        max={totalSeats}
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

                    <Select
                        label="Carrier"
                        placeholder="Select carrier"
                        data={carriers.map(c => ({ value: c.carrierID.toString(), label: c.carrierName }))}
                        value={carrierId.toString()}
                        onChange={setCarrierId}
                        required
                        mb="md"
                    />

                    <TextInput
                        label="Total Seats"
                        value={totalSeats}
                        disabled
                        mb="md"
                    />

                    <DateTimePicker
                        label="Departure DateTime"
                        value={departureDate ? new Date(departureDate) : null}
                        onChange={(date) => setDepartureDate(date ? dayjs(date).format('YYYY-MM-DDTHH:mm') : '')}
                        required
                        mb="md"
                    />
                    <DateTimePicker
                        label="Arrival DateTime"
                        value={arrivalDate ? new Date(arrivalDate) : null}
                        onChange={(date) => setArrivalDate(date ? dayjs(date).format('YYYY-MM-DDTHH:mm') : '')}
                        required
                        mb="md"
                    />

                    {error && (
                        <Text color="red" mb="md">
                            {JSON.stringify(error)}
                        </Text>
                    )}

                    <Button type="submit" color="blue" fullWidth>
                        {isEdit ? 'Update Flight' : 'Create Flight'}
                    </Button>
                </form>
            </Paper>
        </motion.div>
    );

};

export default FlightForm;
