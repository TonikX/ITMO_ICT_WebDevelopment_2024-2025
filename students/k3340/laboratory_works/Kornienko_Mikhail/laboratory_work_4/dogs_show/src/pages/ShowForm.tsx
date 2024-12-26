import React, { useEffect, useState } from 'react';
import { Form, Input, Button, DatePicker, message } from 'antd';
import { useParams, useNavigate } from 'react-router-dom';
import dayjs from 'dayjs';
import { createShow, updateShow, fetchShows } from '../api/api';

const ShowForm: React.FC = () => {
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);
    const { id } = useParams();
    const navigate = useNavigate();

    useEffect(() => {
        if (id) {
            loadShowData(id);
        }
    }, [id]);

    const loadShowData = async (showId: string) => {
        setLoading(true);
        try {
            const shows = await fetchShows('');
            const found = shows.find((s) => s.id === showId);
            if (found) {
                form.setFieldsValue({
                    ...found,
                    date: dayjs(found.date),
                });
            } else {
                message.error('Выставка не найдена');
            }
        } catch (error) {
            message.error('Ошибка при загрузке выставки');
        } finally {
            setLoading(false);
        }
    };

    const onFinish = async (values: any) => {
        setLoading(true);
        try {
            const payload = {
                ...values,
                date: values.date.format('YYYY-MM-DD'),
            };
            if (id) {
                await updateShow(id, payload);
                message.success('Выставка обновлена');
            } else {
                await createShow(payload);
                message.success('Выставка создана');
            }
            navigate('/shows');
        } catch (error) {
            message.error('Ошибка при сохранении');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>{id ? 'Редактировать выставку' : 'Добавить выставку'}</h1>
            <Form form={form} layout="vertical" onFinish={onFinish}>
                <Form.Item label="Название" name="name" rules={[{ required: true }]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Дата" name="date" rules={[{ required: true }]}>
                    <DatePicker style={{ width: '100%' }} />
                </Form.Item>
                <Form.Item label="Тип" name="type" rules={[{ required: true }]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Локация" name="location" rules={[{ required: true }]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Спонсор" name="sponsor" rules={[{ required: true }]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Расписание рингов" name="ring_schedule">
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

export default ShowForm;
