import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
    getMostFrequentAircraftType,
    getRoutesBelowOccupancy,
    getAircraftsInRepairCount,
    getCarrierWorkersCount,
    getAircraftsReportByType
} from '../../store/slices/reportSlice';

import { Paper, Title, Text, Button, TextInput, NumberInput } from '@mantine/core';
import { motion } from 'framer-motion';

const Reports = () => {
    const dispatch = useDispatch();
    const [departure, setDeparture] = useState('');
    const [destination, setDestination] = useState('');
    const [occupancy, setOccupancy] = useState(70);
    const [carrierId, setCarrierId] = useState('');
    const [result, setResult] = useState(null);

    const { loading, error } = useSelector(state => state.reports);

    const handleMostFrequent = async () => {
        const action = await dispatch(getMostFrequentAircraftType({ departure, destination }));
        if (!action.error) {
            setResult(`Тип самолёта: ${action.payload}`);
        }
    };

    const handleBelowOccupancy = async () => {
        const action = await dispatch(getRoutesBelowOccupancy(occupancy));
        if (!action.error) {
            setResult(`Маршруты заполнены < ${occupancy}%: ${JSON.stringify(action.payload)}`);
        }
    };

    const handleInRepairCount = async () => {
        const action = await dispatch(getAircraftsInRepairCount());
        if (!action.error) {
            setResult(`Самолётов в ремонте: ${action.payload}`);
        }
    };

    const handleCarrierWorkers = async () => {
        const id = parseInt(carrierId, 10);
        const action = await dispatch(getCarrierWorkersCount(id));
        if (!action.error) {
            setResult(`Количество работников: ${action.payload}`);
        }
    };

    const handleAircraftsReport = async () => {
        const id = parseInt(carrierId, 10);
        const action = await dispatch(getAircraftsReportByType(id));
        if (!action.error) {
            setResult(JSON.stringify(action.payload, null, 2));
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
        >
            <Paper p="md" radius="md" withBorder style={{ maxWidth: 800, margin: '40px auto' }}>
                <Title order={2} mb="md">Отчёты / Специальные запросы</Title>

                {error && <Text color="red" mb="md">{JSON.stringify(error)}</Text>}
                {loading && <Text mb="md">Загрузка...</Text>}

                <TextInput
                    label="Пункт вылета (departure)"
                    value={departure}
                    onChange={(e) => setDeparture(e.currentTarget.value)}
                    mb="xs"
                />
                <TextInput
                    label="Пункт назначения (destination)"
                    value={destination}
                    onChange={(e) => setDestination(e.currentTarget.value)}
                    mb="xs"
                />
                <Button onClick={handleMostFrequent} mb="md">
                    Самолёт чаще всего летающий по маршруту
                </Button>

                <NumberInput
                    label="Заполненность (%)"
                    value={occupancy}
                    onChange={setOccupancy}
                    mb="xs"
                />
                <Button onClick={handleBelowOccupancy} mb="md">
                    Маршруты с заполненностью ниже {occupancy}%
                </Button>

                <Button onClick={handleInRepairCount} mb="md">
                    Кол-во самолётов в ремонте
                </Button>

                <TextInput
                    label="Carrier ID"
                    value={carrierId}
                    onChange={(e) => setCarrierId(e.currentTarget.value)}
                    mb="xs"
                />
                <Button onClick={handleCarrierWorkers} mb="md">
                    Кол-во работников
                </Button>
                <Button onClick={handleAircraftsReport} mb="md">
                    Отчёт по бортам (по маркам)
                </Button>

                <hr />
                <Text mt="md" style={{ whiteSpace: 'pre-wrap' }}>
                    {result || 'Результаты отобразятся здесь...'}
                </Text>
            </Paper>
        </motion.div>
    );
};

export default Reports;
