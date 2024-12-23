import React, { useEffect, useState } from 'react';
import { Form, Input, Button, message } from 'antd';
import { useParams, useNavigate } from 'react-router-dom';
import { Expert } from '../shared/types';
import { createExpert, updateExpert, fetchExperts } from '../api/api';

const ExpertForm: React.FC = () => {
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);
    const { id } = useParams();
    const navigate = useNavigate();

    useEffect(() => {
        if (id) {
            loadExpertData(id);
        }
        // eslint-disable-next-line
    }, [id]);

    const loadExpertData = async (expertId: string) => {
        setLoading(true);
        try {
            const experts = await fetchExperts('');
            const found = experts.find((ex) => ex.id === expertId);
            if (found) {
                form.setFieldsValue(found);
            } else {
                message.error('Эксперт не найден');
            }
        } catch (error) {
            message.error('Ошибка при загрузке эксперта');
        } finally {
            setLoading(false);
        }
    };

    const onFinish = async (values: Partial<Expert>) => {
        setLoading(true);
        try {
            if (id) {
                await updateExpert(id, values);
                message.success('Эксперт обновлён');
            } else {
                await createExpert(values);
                message.success('Эксперт создан');
            }
            navigate('/experts');
        } catch (error) {
            message.error('Ошибка при сохранении');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>{id ? 'Редактировать эксперта' : 'Добавить эксперта'}</h1>
            <Form form={form} layout="vertical" onFinish={onFinish}>
                <Form.Item label="Фамилия" name="last_name" rules={[{ required: true }]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Имя" name="first_name" rules={[{ required: true }]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Клуб" name="club_name" rules={[{ required: true }]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Обслуживаемые ринги" name="rings_assigned" rules={[{ required: true }]}>
                    <Input.TextArea rows={4} />
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

export default ExpertForm;
