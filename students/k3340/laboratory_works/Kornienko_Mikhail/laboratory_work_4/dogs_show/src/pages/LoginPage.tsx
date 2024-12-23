import React, { useState, useContext } from 'react';
import { Button, Form, Input, message } from 'antd';
import { AuthContext } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const LoginPage: React.FC = () => {
    const [loading, setLoading] = useState(false);
    const { login } = useContext(AuthContext);
    const navigate = useNavigate();

    const onFinish = async (values: { username: string; password: string }) => {
        setLoading(true);
        try {
            await login(values.username, values.password);
            message.success('Успешный вход');
            navigate('/');
        } catch (error) {
            message.error('Ошибка при входе. Проверьте логин/пароль.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: 300, margin: '100px auto' }}>
            <h2>Вход</h2>
            <Form onFinish={onFinish} layout="vertical">
                <Form.Item
                    label="Логин"
                    name="username"
                    rules={[{ required: true, message: 'Введите логин' }]}
                >
                    <Input placeholder="Введите ваш логин" />
                </Form.Item>

                <Form.Item
                    label="Пароль"
                    name="password"
                    rules={[{ required: true, message: 'Введите пароль' }]}
                >
                    <Input.Password placeholder="Введите ваш пароль" />
                </Form.Item>

                <Form.Item>
                    <Button type="primary" htmlType="submit" loading={loading} block>
                        Войти
                    </Button>
                </Form.Item>
            </Form>
        </div>
    );
};

export default LoginPage;
