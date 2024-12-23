import React from 'react';
import {Layout, Avatar, Dropdown, Menu, Typography} from 'antd';
import { UserOutlined, MenuOutlined } from '@ant-design/icons';
import {Navigate, NavLink, useNavigate} from "react-router-dom";

const { Header } = Layout;
const { Text } = Typography;

const AppHeader: React.FC = () => {
    const navigate = useNavigate();

    const username = localStorage.getItem('username');
    if (!username) {
        return null;
    }

    const handleLogout = () => {
        localStorage.clear();
        navigate('/login');
    };

    const mainMenu = (
        <Menu theme="dark" mode="horizontal">

            <Menu.Item key="1">
                <NavLink to="/owners">Владельцы</NavLink>
            </Menu.Item>
            <Menu.Item key="2">
                <NavLink to="/dogs">Собаки</NavLink>
            </Menu.Item>
            <Menu.Item key="3">
                <NavLink to="/shows">Выставки</NavLink>
            </Menu.Item>
            <Menu.Item key="4">
                <NavLink to="/experts">Эксперты</NavLink>
            </Menu.Item>
        </Menu>
    );

    const userMenu = (
        <Menu>
            <Menu.Item key="1" onClick={handleLogout}>
                <a>Logout</a>
            </Menu.Item>
        </Menu>
    );

    return (
        <Header
            style={{
                background: 'linear-gradient(90deg, #001F3F 0%, #005C97 100%)',
                height: '100px',
                padding: '0 40px',
            }}
        >
            <div style={{
                display: 'flex',
                alignItems: 'center',
                height: '100%',
            }}>

                <div style={{ flex: 1 }}>
                    <Dropdown overlay={mainMenu} trigger={['click']}>
                        <div style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                            <Avatar icon={<MenuOutlined />} style={{ marginRight: '8px' }} />
                            <Text style={{ color: 'white' }}>Меню</Text>
                        </div>
                    </Dropdown>
                </div>

                <div style={{ flex: 1, display: 'flex', justifyContent: 'center' }}>
                    <Text
                        onClick={() => navigate('/')}
                        style={{
                            color: 'white',
                            fontSize: '28px',
                            fontWeight: 'bold',
                            cursor: 'pointer',
                        }}
                    >
                        DOGS SHOW
                    </Text>
                </div>

                <div style={{ flex: 1, display: 'flex', justifyContent: 'flex-end' }}>
                    <Dropdown overlay={userMenu} trigger={['click']}>
                        <div style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                            <Avatar icon={<UserOutlined />} style={{ marginRight: '8px' }} />
                            <Text style={{ color: 'white' }}>{username}</Text>
                        </div>
                    </Dropdown>
                </div>
            </div>
        </Header>
    );
};

export default AppHeader;
