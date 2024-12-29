import React, { useState, useContext } from 'react';
import { Form, Input, Button, Typography, notification } from 'antd';
import { AuthContext } from '../context/AuthContext';

const { Title } = Typography;

function RegistrationForm() {
  const { registerUser } = useContext(AuthContext);
  const [loading, setLoading] = useState(false);

  const onFinish = async (values) => {
    setLoading(true);
    try {
      await registerUser(values.username, values.password, values.email);
      notification.success({
        message: 'Регистрация успешна',
        description: 'Вы зарегистрированы и автоматически авторизованы.',
      });
    } catch (error) {
      const errorMsg = 
        error.response?.data?.username?.[0] ||
        error.response?.data?.email?.[0]   ||
        error.response?.data?.detail       ||
        'Произошла ошибка при регистрации.';
      
      notification.error({
        message: 'Ошибка при регистрации',
        description: errorMsg,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: '50px auto' }}>
      <Title level={2}>Регистрация</Title>
      <Form
        name="register-form"
        layout="vertical"
        onFinish={onFinish}
      >
        <Form.Item
          label="Имя пользователя"
          name="username"
          rules={[{ required: true, message: 'Введите имя пользователя' }]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Email"
          name="email"
          rules={[
            { required: true, message: 'Введите email' },
            { type: 'email', message: 'Некорректный email' }
          ]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Пароль"
          name="password"
          rules={[{ required: true, message: 'Введите пароль' }]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading} block>
            Зарегистрироваться
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}

export default RegistrationForm;
