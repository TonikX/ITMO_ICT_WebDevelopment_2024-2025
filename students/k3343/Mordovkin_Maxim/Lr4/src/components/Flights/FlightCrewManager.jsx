// src/components/Flights/FlightCrewManager.jsx
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchAllCrewMembers, assignCrewMember, removeCrewMember } from '../../store/slices/crewSlice';
import { Table, Button, Select, Text, Loader, Group } from '@mantine/core';
import { motion } from 'framer-motion';
import {fetchFlightById} from "../../store/slices/flightSlice";

const FlightCrewManager = ({ flightId }) => {
    const dispatch = useDispatch();
    const { currentFlight, loading: flightLoading } = useSelector(state => state.flights);
    const { members, loading: crewLoading, error } = useSelector(state => state.crew);
    const [availableCrew, setAvailableCrew] = useState([]);
    const [selectedCrew, setSelectedCrew] = useState('');

    useEffect(() => {
        dispatch(fetchAllCrewMembers());
    }, [dispatch]);

    useEffect(() => {
        if (members && currentFlight) {
            console.log('Members:', members);
            console.log('Current Flight:', currentFlight);
            // Предполагается, что currentFlight содержит массив crewMembers
            const assignedCrewIds = currentFlight.crewMembers
                ? currentFlight.crewMembers.map(cm => cm.crewMemberId)
                : [];

            const available = members.filter(cm => !assignedCrewIds.includes(cm.crewMemberId));
            setAvailableCrew(available);
        }
    }, [members, currentFlight, flightId]);

    const handleAssign = async () => {
        if (selectedCrew) {
            const resultAction = await dispatch(
                assignCrewMember({ flightId, crewMemberId: parseInt(selectedCrew) })
            );
            if (assignCrewMember.fulfilled.match(resultAction)) {
                setSelectedCrew('');
                // Важно: вместо fetchAllCrewMembers перезагружаем сам Flight
                dispatch(fetchFlightById(flightId));
            } else {
                alert('Failed to assign crew member');
            }
        }
    };





    let crewAssigned = [];
    if (currentFlight && currentFlight.crews) {
        currentFlight.crews.forEach((oneCrew) => {
            if (oneCrew.crewMembers) {
                crewAssigned.push(...oneCrew.crewMembers);
            }
        });
    }


    if (flightLoading || crewLoading) {
        return <Loader size="xl" />;
    }

    return (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
            <Text size="lg" weight={700} mb="md">Управление экипажем для рейса #{flightId}</Text>

            {error && <Text color="red" mb="md">{error}</Text>}

            <Group mb="md">
                <Select
                    label="Выберите члена экипажа"
                    placeholder="Выберите"


                    data={availableCrew.map(cm => ({
                        value: cm.crewMemberId ? cm.crewMemberId.toString() : '',
                        label: cm.fullName || 'Unknown'
                    })).filter(item => item.value)} // Убираем элементы с пустым value


                    value={selectedCrew}
                    onChange={setSelectedCrew}
                    style={{ flex: 1 }}
                />
                <Button onClick={handleAssign} disabled={!selectedCrew}>
                    Добавить
                </Button>
            </Group>

            <Table>
                <thead>
                <tr>
                    <th>ID</th>
                    <th>ФИО</th>
                    <th>Должность</th>
                </tr>
                </thead>
                <tbody>
                {crewAssigned.map(cm => (
                    cm && cm.crewMemberId && (
                        <tr key={cm.crewMemberId}>
                            <td>{cm.crewMemberId}</td>
                            <td>{cm.fullName}</td>
                            <td>{cm.roleName}</td>
                        </tr>
                    )
                ))}
                {crewAssigned.length === 0 && (
                    <tr>
                        <td colSpan="3" align="center">
                            Нет назначенных членов экипажа.
                        </td>
                    </tr>
                )}
                </tbody>
            </Table>
        </motion.div>
    );
};

export default FlightCrewManager;
