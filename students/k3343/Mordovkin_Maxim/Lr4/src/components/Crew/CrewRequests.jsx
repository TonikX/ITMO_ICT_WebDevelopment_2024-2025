// src/components/Crew/CrewRequests.jsx
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Table, Button, Text, Loader } from '@mantine/core';
import { motion } from 'framer-motion';

// Импортируем
import { fetchPendingCrew, approveCrew, rejectCrew } from '../../store/slices/crewSlice';

const CrewRequests = () => {
    const dispatch = useDispatch();
    const { members, loading, error } = useSelector((state) => state.crew);

    useEffect(() => {
        dispatch(fetchPendingCrew());
    }, [dispatch]);

    if (loading) return <Loader size="xl" />;
    if (error) return <Text color="red">{error}</Text>;

    return (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
            <Text size="xl" mb="md">
                Заявки на работу (PENDING)
            </Text>
            <Table>
                <thead>
                <tr>
                    <th>ID</th>
                    <th>FullName</th>
                    <th>Age</th>
                    <th>Education</th>
                    <th>WorkExp</th>
                    <th>Passport</th>
                    <th>Role</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
                </thead>
                <tbody>
                {members.map((m) => (
                    <tr key={m.crewMemberId}> {/* Исправлено на crewMemberId */}
                        <td>{m.crewMemberId}</td> {/* Исправлено на crewMemberId */}
                        <td>{m.fullName}</td>
                        <td>{m.age}</td>
                        <td>{m.education}</td>
                        <td>{m.workExperience}</td>
                        <td>{m.passportData}</td>
                        <td>{m.roleName}</td>
                        <td>{m.employmentStatus}</td>
                        <td>
                            <Button onClick={() => dispatch(approveCrew(m.crewMemberId))} color="green" size="xs">
                                Approve
                            </Button>
                            <Button onClick={() => dispatch(rejectCrew(m.crewMemberId))} color="red" size="xs">
                                Reject
                            </Button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </Table>
        </motion.div>
    );
};

export default CrewRequests;
