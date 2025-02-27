// src/components/Carriers/CarrierForm.jsx
import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { createCarrier, updateCarrier, fetchCarriers } from '../../store/slices/carrierSlice';
import { Paper, Title, TextInput, Button, Text } from '@mantine/core';
import { motion } from 'framer-motion';
import { useNavigate, useParams } from 'react-router-dom';

const CarrierForm = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { carrierId } = useParams();
    const isEdit = Boolean(carrierId);

    const { carriers, loading, error } = useSelector(state => state.carriers);
    const [name, setName] = useState('');

    useEffect(() => {
        dispatch(fetchCarriers());
    }, [dispatch]);

    useEffect(() => {
        if (isEdit && carriers.length > 0) {
            const carrier = carriers.find(c => c.carrierID === parseInt(carrierId, 10));
            if (carrier) {
                setName(carrier.carrierName);
            }
        }
    }, [isEdit, carriers, carrierId]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (isEdit) {
            await dispatch(updateCarrier({ id: parseInt(carrierId, 10), data: { carrierName: name } }));
        } else {
            await dispatch(createCarrier({ carrierName: name }));
        }
        navigate('/carriers');
    };

    return (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
            <Paper p="md" radius="md" withBorder style={{ maxWidth: 500, margin: '40px auto' }}>
                <Title order={2} mb="md">{isEdit ? 'Edit Carrier' : 'Add New Carrier'}</Title>

                <form onSubmit={handleSubmit}>
                    <TextInput
                        label="Carrier Name"
                        value={name}
                        onChange={(e) => setName(e.currentTarget.value)}
                        required
                        mb="md"
                    />

                    {error && (
                        <Text color="red" mb="md">
                            {JSON.stringify(error)}
                        </Text>
                    )}

                    <Button type="submit" color="blue" fullWidth>
                        {isEdit ? 'Update Carrier' : 'Create Carrier'}
                    </Button>
                </form>
            </Paper>
        </motion.div>
    );
};

export default CarrierForm;
