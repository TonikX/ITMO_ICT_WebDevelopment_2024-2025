import React, { useContext, useEffect, useState } from 'react';
import { Button, Spin } from 'antd';
import { AuthContext } from '../context/AuthContext';

const ProtectedPage: React.FC = () => {
    const { token, logout } = useContext(AuthContext);
    const [username, setUsername] = useState<string>('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchUser = async () => {
            if (!token) return;

            try {
                const response = await fetch('http://127.0.0.1:8000/auth/users/me/', {
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Token ${token}`,
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    setUsername(data.username);
                }
            } catch (error) {
                console.error('Ошибка при получении данных пользователя:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchUser();
    }, [token]);

    const handleLogout = () => {
        logout();
    };

    if (loading) {
        return <Spin style={{ display: 'block', margin: '100px auto' }} />;
    }

    return (
        <div style={{ maxWidth: 300, margin: '100px auto', textAlign: 'center' }}>
            <h1>Закрытая страница</h1>
            <p>Добро пожаловать, <strong>{username}</strong>!</p>
            <Button type="primary" onClick={handleLogout}>
                Выйти
            </Button>
        </div>
    );
};

export default ProtectedPage;
