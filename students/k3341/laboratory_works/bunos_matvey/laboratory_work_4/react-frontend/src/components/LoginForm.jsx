import React, { useState, useContext } from 'react';
import { Form, Input, Button, Typography, notification } from 'antd';
import { AuthContext } from '../context/AuthContext';

const { Title } = Typography;

function LoginForm() {
  const { login } = useContext(AuthContext);
  const [loading, setLoading] = useState(false);

  const onFinish = async (values) => {
    setLoading(true);
    try {
      await login(values.username, values.password);
      notification.success({
        message: 'Успешный вход',
        description: 'Вы успешно вошли в систему!',
      });
    } catch (error) {
      notification.error({
        message: 'Ошибка при входе',
        description:
          error.response?.data?.non_field_errors?.[0] || 
          error.response?.data?.detail ||
          'Произошла ошибка при входе. Проверьте логин/пароль.',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: '50px auto' }}>
      <Title level={2}>Вход</Title>
      <Form
        name="login-form"
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
          label="Пароль"
          name="password"
          rules={[{ required: true, message: 'Введите пароль' }]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading} block>
            Войти
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}

export default LoginForm;
