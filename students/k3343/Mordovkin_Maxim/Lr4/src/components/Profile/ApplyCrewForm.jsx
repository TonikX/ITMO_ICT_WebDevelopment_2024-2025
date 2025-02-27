// src/components/Profile/ApplyCrewForm.jsx
import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Paper, Title, Text, TextInput, NumberInput, Select, Button, Group } from '@mantine/core';
import { applyForCrew } from '../../store/slices/crewSlice';

const ApplyCrewForm = () => {
    const dispatch = useDispatch();
    const { user } = useSelector((state) => state.auth);
    const { loading, error } = useSelector((state) => state.crew);

    const [fullName, setFullName] = useState(user.username);
    const [age, setAge] = useState(18);
    const [education, setEducation] = useState('');
    const [workExperience, setWorkExperience] = useState(0);
    const [passportData, setPassportData] = useState('');
    const [role, setRole] = useState('NAVIGATOR');

    const handleApply = async () => {
        const payload = {
            userId: user.userId,
            fullName,
            age,
            education,
            workExperience,
            passportData,
            role,
        };
        const result = await dispatch(applyForCrew(payload));
        if (!result.error) {
            alert('Заявка подана успешно!');
        }
    };

    return (
        <Paper p="md" radius="md" withBorder style={{ marginTop: '2rem' }}>
            <Title order={3} mb="md">
                Подать заявку на должность
            </Title>

            <TextInput
                label="ФИО"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
                mb="md"
            />

            <NumberInput
                label="Возраст"
                value={age}
                onChange={setAge}
                min={18}
                mb="md"
            />

            <TextInput
                label="Образование"
                value={education}
                onChange={(e) => setEducation(e.target.value)}
                required
                mb="md"
            />

            <NumberInput
                label="Стаж (лет)"
                value={workExperience}
                onChange={setWorkExperience}
                min={0}
                mb="md"
            />

            <TextInput
                label="Паспортные данные"
                value={passportData}
                onChange={(e) => setPassportData(e.target.value)}
                required
                mb="md"
            />

            <Select
                label="Должность"
                value={role}
                onChange={setRole}
                data={[
                    { value: 'COMMANDER', label: 'Командир корабля' },
                    { value: 'SECOND_PILOT', label: 'Второй пилот' },
                    { value: 'NAVIGATOR', label: 'Штурман' },
                    { value: 'STEWARD', label: 'Стюард(есса)' },
                ]}
                mb="md"
            />

            {error && (
                <Text color="red" mb="md">
                    {error}
                </Text>
            )}

            <Group position="center">
                <Button onClick={handleApply} loading={loading}>
                    Отправить заявку
                </Button>
            </Group>
        </Paper>
    );
};

export default ApplyCrewForm;
