// src/pages/OwnerForm.tsx
import React, { useEffect, useState } from 'react';
import { Form, Input, Button, message } from 'antd';
import { useParams, useNavigate } from 'react-router-dom';
import { createOwner, updateOwner, fetchOwners } from '../api/api';
import { Owner } from '../shared/types';

const OwnerForm: React.FC = () => {
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);
    const { id } = useParams();
    const navigate = useNavigate();

    useEffect(() => {
        if (id) {
            loadOwner(id);
        }
    }, [id]);

    const loadOwner = async (ownerId: string) => {
        setLoading(true);
        try {
            const owners = await fetchOwners();
            const owner = owners.find((item) => item.id === ownerId);
            if (owner) {
                form.setFieldsValue(owner);
            }
        } catch (error) {
            message.error('Ошибка при загрузке данных владельца.');
        } finally {
            setLoading(false);
        }
    };

    const onFinish = async (values: Partial<Owner>) => {
        setLoading(true);
        try {
            if (id) {
                await updateOwner(id, values);
                message.success('Владелец обновлён.');
            } else {
                await createOwner(values);
                message.success('Владелец создан.');
            }
            navigate('/owners');
        } catch (error) {
            message.error('Ошибка при сохранении владельца.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>{id ? 'Редактировать владельца' : 'Создать владельца'}</h1>
            <Form form={form} layout="vertical" onFinish={onFinish}>
                <Form.Item label="Фамилия" name="last_name" rules={[{ required: true }]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Имя" name="first_name" rules={[{ required: true }]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Отчество" name="patronymic">
                    <Input />
                </Form.Item>
                <Form.Item label="Паспортные данные" name="passport_details" rules={[{ required: true }]}>
                    <Input.TextArea />
                </Form.Item>
                <Form.Item label="Контакты" name="contact_info" rules={[{ required: true }]}>
                    <Input.TextArea />
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

export default OwnerForm;
