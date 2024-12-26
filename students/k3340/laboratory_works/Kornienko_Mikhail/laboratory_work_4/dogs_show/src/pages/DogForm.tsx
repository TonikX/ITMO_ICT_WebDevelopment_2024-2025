import React, { useEffect, useState } from 'react';
import { Form, Input, Button, message, Select, DatePicker, InputNumber } from 'antd';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchDogs, createDog, fetchOwners, updateOwner, createOwner } from '../api/api';
import { Dog, Owner } from '../shared/types';
import { fetchOwners as getOwners, updateDog } from '../api/api';
import dayjs from 'dayjs';

const DogForm: React.FC = () => {
    const [form] = Form.useForm();
    const [owners, setOwners] = useState<Owner[]>([]);
    const [loading, setLoading] = useState(false);
    const { id } = useParams();
    const navigate = useNavigate();

    useEffect(() => {
        loadOwners();
        if (id) {
            loadDog(id);
        }
    }, [id]);

    const loadOwners = async () => {
        try {
            const ownersData = await getOwners();
            setOwners(ownersData);
        } catch (error) {
            message.error('Не удалось загрузить владельцев.');
        }
    };

    const loadDog = async (dogId: string) => {
        setLoading(true);
        try {
            const allDogs = await fetchDogs();
            const dog = allDogs.find((d) => d.id === dogId);
            if (dog) {
                form.setFieldsValue({
                    ...dog,
                    date_of_last_vaccination: dayjs(dog.date_of_last_vaccination),
                    owner_id: dog.owner_id,
                });
            }
        } catch (error) {
            message.error('Ошибка при загрузке собаки.');
        } finally {
            setLoading(false);
        }
    };

    const onFinish = async (values: any) => {
        setLoading(true);
        try {
            const payload = {
                ...values,
                date_of_last_vaccination: values.date_of_last_vaccination.format('YYYY-MM-DD'),
            };
            if (id) {
                await updateDog(id, payload);
                message.success('Собака обновлена.');
            } else {
                await createDog(payload);
                message.success('Собака создана.');
            }
            navigate('/dogs');
        } catch (error) {
            message.error('Ошибка при сохранении собаки.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>{id ? 'Редактировать собаку' : 'Добавить собаку'}</h1>
            <Form form={form} layout="vertical" onFinish={onFinish}>
                <Form.Item label="Кличка" name="name" rules={[{ required: true }]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Порода" name="breed" rules={[{ required: true }]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Возраст" name="age" rules={[{ required: true }]}>
                    <InputNumber min={0} style={{ width: '100%' }} />
                </Form.Item>
                <Form.Item label="Классность" name="class_name" rules={[{ required: true }]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Клуб" name="club_name" rules={[{ required: true }]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Владелец" name="owner_id" rules={[{ required: true }]}>
                    <Select placeholder="Выберите владельца">
                        {owners.map((owner) => (
                            <Select.Option key={owner.id} value={owner.id}>
                                {owner.last_name} {owner.first_name}
                            </Select.Option>
                        ))}
                    </Select>
                </Form.Item>
                <Form.Item label="№ родословной" name="pedigree_document_number" rules={[{ required: true }]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Кличка отца" name="sire_name" rules={[{ required: true }]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Кличка матери" name="dam_name" rules={[{ required: true }]}>
                    <Input />
                </Form.Item>
                <Form.Item
                    label="Дата последней прививки"
                    name="date_of_last_vaccination"
                    rules={[{ required: true }]}
                >
                    <DatePicker format="YYYY-MM-DD" style={{ width: '100%' }} />
                </Form.Item>

                <Form.Item>
                    <Button type="primary" htmlType="submit" loading={loading}>
                        Сохранить
                    </Button>
                </Form.Item>
            </Form>
        </div>
    );
};

export default DogForm;
